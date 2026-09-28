#!/usr/bin/env python3
"""Arcadia Outreach CRM Dashboard - live server.

Reads canonical files on every request so the dashboard
always reflects the current state of the pipeline.

Usage:
    python3 dashboard/server.py          # starts on port 3333
    python3 dashboard/server.py 8080     # custom port
"""

import http.server
import json
import os
import re
import sys
from pathlib import Path
from typing import Optional, List, Dict

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3333
AGENT_ROOT = Path(__file__).resolve().parent.parent

SCAN_DIRS = [
    ("stages/05-send/output", "phase-0"),
    ("phase-0.1-youtube-discovery/output", "phase-0.1"),
    ("stages/04-personalization/output", "loom"),
    ("stages/02-qualification/output/_disqualified", "disqualified"),
    ("stages/02-qualification/output/parked", "parked"),
]


def parse_frontmatter(filepath: Path, batch: str) -> Optional[dict]:
    text = filepath.read_text(errors="replace")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm, body = parts[1], parts[2]

    def get(key):
        m = re.search(rf"^{key}:\s*\"?([^\"\n]*)\"?", fm, re.MULTILINE)
        return m.group(1).strip().strip('"') if m else ""

    log_rows = re.findall(r"\|\s*\d{4}-\d{2}-\d{2}\s*\|", body)

    return {
        "name": get("name"),
        "slug": get("slug"),
        "segment": get("segment"),
        "source": get("source") or batch,
        "sent_channel": get("sent_channel"),
        "failed_channels": get("failed_channels"),
        "sent_at": get("sent_at"),
        "email": get("business_email"),
        "instagram": get("instagram"),
        "twitter": get("twitter"),
        "linkedin": get("linkedin"),
        "website": get("website"),
        "youtube": get("youtube_handle"),
        "community_platform": get("community_platform"),
        "batch": batch,
        "log_entries": len(log_rows),
    }


def scan_contacts() -> List[dict]:
    contacts = []
    for rel_dir, batch in SCAN_DIRS:
        d = AGENT_ROOT / rel_dir
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            c = parse_frontmatter(f, batch)
            if c and c["name"]:
                contacts.append(c)
    contacts.sort(key=lambda x: x["name"])
    return contacts


def build_stats(contacts: List[dict]) -> dict:
    channels = ["email", "instagram-dm", "twitter-dm", "linkedin-dm", "skool-dm"]
    total = len(contacts)
    touched = sum(1 for c in contacts if c["sent_channel"])
    total_touches = 0
    total_fails = 0
    channel_stats = {}

    for ch in channels:
        sent = sum(1 for c in contacts if ch in c["sent_channel"])
        failed = sum(1 for c in contacts if ch in c["failed_channels"])
        channel_stats[ch] = {"sent": sent, "failed": failed}
        total_touches += sent
        total_fails += failed

    segments = {}
    batches = {}
    for c in contacts:
        seg = c["segment"] or "unknown"
        segments[seg] = segments.get(seg, 0) + 1
        b = c["batch"]
        batches[b] = batches.get(b, 0) + 1

    return {
        "total": total,
        "touched": touched,
        "untouched": total - touched,
        "total_touches": total_touches,
        "total_fails": total_fails,
        "channels": channel_stats,
        "segments": segments,
        "batches": batches,
    }


DASHBOARD_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Arcadia Outreach CRM</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --bg: #f8f9fc;
  --card: #ffffff;
  --border: #e8ecf1;
  --text: #1a1d26;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --accent: #6366f1;
  --accent-light: #e0e7ff;
  --green: #10b981;
  --green-light: #d1fae5;
  --red: #ef4444;
  --red-light: #fee2e2;
  --orange: #f59e0b;
  --orange-light: #fef3c7;
  --blue: #3b82f6;
  --blue-light: #dbeafe;
  --purple: #8b5cf6;
  --purple-light: #ede9fe;
  --pink: #ec4899;
  --pink-light: #fce7f3;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.06), 0 2px 4px -2px rgba(0,0,0,0.04);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.06), 0 4px 6px -4px rgba(0,0,0,0.04);
  --radius: 12px;
  --radius-sm: 8px;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
  min-height: 100vh;
}

.app {
  max-width: 1440px;
  margin: 0 auto;
  padding: 24px 32px;
}

/* Header */
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 32px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

.header-left { display: flex; align-items: center; gap: 16px; }

.logo {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, var(--accent), var(--purple));
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 800;
  font-size: 18px;
}

.header h1 {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.3px;
}

.header h1 span {
  font-weight: 400;
  color: var(--text-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.live-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--green);
  font-weight: 500;
}

.live-dot {
  width: 8px;
  height: 8px;
  background: var(--green);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.last-updated {
  font-size: 12px;
  color: var(--text-muted);
}

/* Metric Cards */
.metrics {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.metric-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 20px 24px;
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.2s, transform 0.2s;
}

.metric-card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.metric-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.metric-value {
  font-size: 32px;
  font-weight: 800;
  letter-spacing: -1px;
  line-height: 1;
}

.metric-sub {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 6px;
}

.metric-card.accent .metric-value { color: var(--accent); }
.metric-card.green .metric-value { color: var(--green); }
.metric-card.blue .metric-value { color: var(--blue); }
.metric-card.orange .metric-value { color: var(--orange); }
.metric-card.red .metric-value { color: var(--red); }

/* Two-column layout */
.grid-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 28px;
}

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}

.card-title {
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.card-title .icon {
  width: 20px;
  height: 20px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
}

/* Channel bars */
.channel-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.channel-row:last-child { margin-bottom: 0; }

.channel-name {
  width: 110px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  flex-shrink: 0;
}

.channel-bar-wrap {
  flex: 1;
  height: 28px;
  background: var(--bg);
  border-radius: 6px;
  overflow: hidden;
  display: flex;
  position: relative;
}

.channel-bar {
  height: 100%;
  border-radius: 6px;
  transition: width 0.8s cubic-bezier(0.22, 1, 0.36, 1);
  display: flex;
  align-items: center;
  padding: 0 10px;
  font-size: 11px;
  font-weight: 600;
  color: white;
  white-space: nowrap;
  min-width: 0;
}

.channel-bar.sent { background: linear-gradient(90deg, var(--green), #34d399); }
.channel-bar.failed { background: var(--red); opacity: 0.7; border-radius: 0; }

.channel-count {
  width: 60px;
  text-align: right;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
  margin-left: 12px;
}

/* Segment pills */
.segment-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.segment-pill {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-weight: 500;
  flex: 1;
  min-width: 160px;
}

.segment-pill .count {
  font-size: 20px;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.segment-pill.mega { background: var(--purple-light); color: #6d28d9; }
.segment-pill.established { background: var(--blue-light); color: #1d4ed8; }
.segment-pill.mid { background: var(--green-light); color: #047857; }
.segment-pill.consultant { background: var(--orange-light); color: #b45309; }
.segment-pill.niche { background: var(--pink-light); color: #be185d; }
.segment-pill.other { background: #f3f4f6; color: var(--text-secondary); }

/* Table section */
.table-section {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.table-header {
  padding: 20px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border);
}

.table-header h2 {
  font-size: 14px;
  font-weight: 700;
}

.table-controls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-box {
  padding: 7px 12px 7px 34px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 13px;
  font-family: inherit;
  outline: none;
  width: 240px;
  background: var(--bg) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%239ca3af' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Ccircle cx='11' cy='11' r='8'%3E%3C/circle%3E%3Cline x1='21' y1='21' x2='16.65' y2='16.65'%3E%3C/line%3E%3C/svg%3E") 10px center no-repeat;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.search-box:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-light);
}

.filter-btn {
  padding: 7px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 500;
  font-family: inherit;
  background: var(--bg);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
}

.filter-btn:hover { border-color: var(--accent); color: var(--accent); }
.filter-btn.active { background: var(--accent); color: white; border-color: var(--accent); }

.table-wrap { overflow-x: auto; }

table {
  width: 100%;
  border-collapse: collapse;
}

th {
  text-align: left;
  padding: 10px 16px;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--text-muted);
  background: var(--bg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
}

th:hover { color: var(--text); }

th .sort-arrow {
  font-size: 10px;
  margin-left: 4px;
  opacity: 0.3;
}

th.sorted .sort-arrow { opacity: 1; color: var(--accent); }

td {
  padding: 12px 16px;
  font-size: 13px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}

tr:last-child td { border-bottom: none; }

tr:hover td { background: #f9fafb; }

.name-cell {
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
}

.segment-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.segment-tag.mega-creator { background: var(--purple-light); color: #6d28d9; }
.segment-tag.established-creator { background: var(--blue-light); color: #1d4ed8; }
.segment-tag.mid-tier-creator { background: var(--green-light); color: #047857; }
.segment-tag.consultant-operator { background: var(--orange-light); color: #b45309; }
.segment-tag.niche-builder { background: var(--pink-light); color: #be185d; }
.segment-tag.disqualified { background: var(--red-light); color: #b91c1c; }

.batch-tag {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 500;
  background: #f3f4f6;
  color: var(--text-secondary);
}

/* Channel status dots */
.channel-dots {
  display: flex;
  gap: 6px;
  align-items: center;
}

.ch-dot {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  position: relative;
  cursor: default;
}

.ch-dot.sent {
  background: var(--green-light);
  color: var(--green);
}

.ch-dot.failed {
  background: var(--red-light);
  color: var(--red);
}

.ch-dot.none {
  background: #f3f4f6;
  color: #d1d5db;
}

.ch-dot::after {
  content: attr(data-tip);
  position: absolute;
  bottom: calc(100% + 6px);
  left: 50%;
  transform: translateX(-50%);
  background: var(--text);
  color: white;
  font-size: 11px;
  font-weight: 500;
  padding: 4px 8px;
  border-radius: 6px;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.15s;
}

.ch-dot:hover::after { opacity: 1; }

.touches-cell {
  font-weight: 700;
  font-size: 15px;
  text-align: center;
}

.table-footer {
  padding: 12px 24px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-muted);
  display: flex;
  justify-content: space-between;
}

/* Responsive */
@media (max-width: 1100px) {
  .metrics { grid-template-columns: repeat(3, 1fr); }
  .grid-2 { grid-template-columns: 1fr; }
}

@media (max-width: 700px) {
  .app { padding: 16px; }
  .metrics { grid-template-columns: repeat(2, 1fr); }
  .header { flex-direction: column; align-items: flex-start; gap: 12px; }
}

/* Fade-in animation */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in {
  animation: fadeUp 0.4s ease-out both;
}

.fade-in:nth-child(2) { animation-delay: 0.05s; }
.fade-in:nth-child(3) { animation-delay: 0.1s; }
.fade-in:nth-child(4) { animation-delay: 0.15s; }
.fade-in:nth-child(5) { animation-delay: 0.2s; }
</style>
</head>
<body>
<div class="app" id="app">
  <div class="header">
    <div class="header-left">
      <div class="logo">A</div>
      <h1>Arcadia Outreach <span>CRM</span></h1>
    </div>
    <div class="header-right">
      <div class="live-badge"><div class="live-dot"></div> Live</div>
      <div class="last-updated" id="lastUpdated">Loading...</div>
    </div>
  </div>
  <div id="dashboard">Loading dashboard...</div>
</div>

<script>
const REFRESH_INTERVAL = 30000;
let allContacts = [];
let currentFilter = 'all';
let currentSearch = '';
let sortCol = 'name';
let sortDir = 'asc';

async function fetchData() {
  const res = await fetch('/api/contacts');
  return await res.json();
}

function channelStatus(contact, channel) {
  const sent = (contact.sent_channel || '').split(',').map(s => s.trim());
  const failed = (contact.failed_channels || '').split(',').map(s => s.trim().split(':')[0].trim());
  if (sent.includes(channel)) return 'sent';
  if (failed.some(f => f === channel)) return 'failed';
  return 'none';
}

function countTouches(contact) {
  if (!contact.sent_channel) return 0;
  return contact.sent_channel.split(',').map(s => s.trim()).filter(Boolean).length;
}

function renderMetrics(stats) {
  return `
    <div class="metrics">
      <div class="metric-card accent fade-in">
        <div class="metric-label">Total Pipeline</div>
        <div class="metric-value">${stats.total}</div>
        <div class="metric-sub">${Object.entries(stats.batches).map(([k,v]) => `${v} ${k}`).join(' / ')}</div>
      </div>
      <div class="metric-card green fade-in">
        <div class="metric-label">People Touched</div>
        <div class="metric-value">${stats.touched}</div>
        <div class="metric-sub">${stats.untouched} untouched</div>
      </div>
      <div class="metric-card blue fade-in">
        <div class="metric-label">Channel Touches</div>
        <div class="metric-value">${stats.total_touches}</div>
        <div class="metric-sub">${(stats.total_touches / Math.max(stats.touched, 1)).toFixed(1)} avg per person</div>
      </div>
      <div class="metric-card orange fade-in">
        <div class="metric-label">Failed Channels</div>
        <div class="metric-value">${stats.total_fails}</div>
        <div class="metric-sub">${stats.total_touches > 0 ? ((stats.total_fails / (stats.total_touches + stats.total_fails)) * 100).toFixed(0) : 0}% failure rate</div>
      </div>
      <div class="metric-card red fade-in">
        <div class="metric-label">Replies</div>
        <div class="metric-value">0</div>
        <div class="metric-sub">Bumps due May 1</div>
      </div>
    </div>
  `;
}

function renderChannelBars(stats) {
  const channels = [
    { key: 'email', label: 'Email', max: stats.total },
    { key: 'instagram-dm', label: 'Instagram', max: stats.total },
    { key: 'linkedin-dm', label: 'LinkedIn', max: stats.total },
    { key: 'twitter-dm', label: 'Twitter', max: stats.total },
    { key: 'skool-dm', label: 'Skool', max: stats.total },
  ];

  return channels.map(ch => {
    const s = stats.channels[ch.key] || { sent: 0, failed: 0 };
    const sentPct = (s.sent / ch.max) * 100;
    const failPct = (s.failed / ch.max) * 100;
    return `
      <div class="channel-row">
        <div class="channel-name">${ch.label}</div>
        <div class="channel-bar-wrap">
          <div class="channel-bar sent" style="width:${sentPct}%">${s.sent > 0 ? s.sent : ''}</div>
          <div class="channel-bar failed" style="width:${failPct}%">${s.failed > 3 ? s.failed : ''}</div>
        </div>
        <div class="channel-count">${s.sent}/${s.sent + s.failed}</div>
      </div>
    `;
  }).join('');
}

function renderSegments(stats) {
  const order = [
    { key: 'mega-creator', cls: 'mega', label: 'Mega' },
    { key: 'established-creator', cls: 'established', label: 'Established' },
    { key: 'mid-tier-creator', cls: 'mid', label: 'Mid-tier' },
    { key: 'consultant-operator', cls: 'consultant', label: 'Consultant' },
    { key: 'niche-builder', cls: 'niche', label: 'Niche' },
  ];
  return order
    .filter(s => stats.segments[s.key])
    .map(s => `
      <div class="segment-pill ${s.cls}">
        <span class="count">${stats.segments[s.key]}</span>
        <span>${s.label}</span>
      </div>
    `).join('');
}

function getFiltered() {
  let list = allContacts;
  if (currentFilter !== 'all') {
    list = list.filter(c => c.batch === currentFilter);
  }
  if (currentSearch) {
    const q = currentSearch.toLowerCase();
    list = list.filter(c =>
      c.name.toLowerCase().includes(q) ||
      (c.segment || '').toLowerCase().includes(q) ||
      (c.community_platform || '').toLowerCase().includes(q)
    );
  }
  list.sort((a, b) => {
    let va, vb;
    if (sortCol === 'name') { va = a.name; vb = b.name; }
    else if (sortCol === 'segment') { va = a.segment; vb = b.segment; }
    else if (sortCol === 'batch') { va = a.batch; vb = b.batch; }
    else if (sortCol === 'touches') { va = countTouches(a); vb = countTouches(b); }
    else if (sortCol === 'sent_at') { va = a.sent_at || 'z'; vb = b.sent_at || 'z'; }
    else { va = a.name; vb = b.name; }
    if (typeof va === 'number') return sortDir === 'asc' ? va - vb : vb - va;
    return sortDir === 'asc' ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va));
  });
  return list;
}

function arrow(col) {
  if (sortCol !== col) return '<span class="sort-arrow">↕</span>';
  return `<span class="sort-arrow">${sortDir === 'asc' ? '↑' : '↓'}</span>`;
}

function renderTable() {
  const list = getFiltered();
  const batches = [...new Set(allContacts.map(c => c.batch))];
  const chCols = [
    { key: 'email', icon: '✉', label: 'Email' },
    { key: 'instagram-dm', icon: '📷', label: 'Instagram' },
    { key: 'linkedin-dm', icon: '🔗', label: 'LinkedIn' },
    { key: 'twitter-dm', icon: '𝕏', label: 'Twitter' },
    { key: 'skool-dm', icon: 'S', label: 'Skool' },
  ];

  return `
    <div class="table-section">
      <div class="table-header">
        <h2>All Contacts (${list.length})</h2>
        <div class="table-controls">
          <input class="search-box" type="text" placeholder="Search name, segment..." value="${currentSearch}" oninput="handleSearch(this.value)">
          <button class="filter-btn ${currentFilter === 'all' ? 'active' : ''}" onclick="setFilter('all')">All</button>
          ${batches.map(b => `<button class="filter-btn ${currentFilter === b ? 'active' : ''}" onclick="setFilter('${b}')">${b}</button>`).join('')}
        </div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th onclick="toggleSort('name')" class="${sortCol === 'name' ? 'sorted' : ''}">Name ${arrow('name')}</th>
              <th onclick="toggleSort('segment')" class="${sortCol === 'segment' ? 'sorted' : ''}">Segment ${arrow('segment')}</th>
              <th onclick="toggleSort('batch')" class="${sortCol === 'batch' ? 'sorted' : ''}">Batch ${arrow('batch')}</th>
              <th>Channels</th>
              <th onclick="toggleSort('touches')" class="${sortCol === 'touches' ? 'sorted' : ''}">Touches ${arrow('touches')}</th>
              <th onclick="toggleSort('sent_at')" class="${sortCol === 'sent_at' ? 'sorted' : ''}">Sent ${arrow('sent_at')}</th>
              <th>Platform</th>
            </tr>
          </thead>
          <tbody>
            ${list.map(c => {
              const touches = countTouches(c);
              return `
                <tr>
                  <td class="name-cell">${c.name}</td>
                  <td><span class="segment-tag ${c.segment}">${c.segment || '-'}</span></td>
                  <td><span class="batch-tag">${c.batch}</span></td>
                  <td>
                    <div class="channel-dots">
                      ${chCols.map(ch => {
                        const st = channelStatus(c, ch.key);
                        return `<div class="ch-dot ${st}" data-tip="${ch.label}: ${st}">${ch.icon}</div>`;
                      }).join('')}
                    </div>
                  </td>
                  <td class="touches-cell">${touches || '<span style="color:#d1d5db">-</span>'}</td>
                  <td style="font-size:12px;color:var(--text-secondary)">${c.sent_at || '-'}</td>
                  <td style="font-size:12px;color:var(--text-secondary);max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="${(c.community_platform || '').replace(/"/g, '&quot;')}">${c.community_platform || '-'}</td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      </div>
      <div class="table-footer">
        <span>Showing ${list.length} of ${allContacts.length} contacts</span>
        <span>Auto-refreshes every 30s</span>
      </div>
    </div>
  `;
}

function render(data) {
  const { contacts, stats } = data;
  allContacts = contacts;

  document.getElementById('dashboard').innerHTML = `
    ${renderMetrics(stats)}
    <div class="grid-2">
      <div class="card fade-in">
        <div class="card-title"><span class="icon">📡</span> Channel Performance</div>
        ${renderChannelBars(stats)}
      </div>
      <div class="card fade-in">
        <div class="card-title"><span class="icon">🎯</span> Segments</div>
        <div class="segment-grid">${renderSegments(stats)}</div>
      </div>
    </div>
    ${renderTable()}
  `;
  document.getElementById('lastUpdated').textContent = 'Updated ' + new Date().toLocaleTimeString();
}

function handleSearch(val) {
  currentSearch = val;
  document.getElementById('dashboard').querySelector('.table-section').outerHTML = renderTable();
}

function setFilter(f) {
  currentFilter = f;
  document.getElementById('dashboard').querySelector('.table-section').outerHTML = renderTable();
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.classList.toggle('active', b.textContent.trim() === f || (f === 'all' && b.textContent.trim() === 'All'));
  });
}

function toggleSort(col) {
  if (sortCol === col) { sortDir = sortDir === 'asc' ? 'desc' : 'asc'; }
  else { sortCol = col; sortDir = 'asc'; }
  document.getElementById('dashboard').querySelector('.table-section').outerHTML = renderTable();
}

async function refresh() {
  try {
    const data = await fetchData();
    render(data);
  } catch (e) {
    console.error('Refresh failed:', e);
  }
}

refresh();
setInterval(refresh, REFRESH_INTERVAL);
</script>
</body>
</html>
"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/contacts":
            contacts = scan_contacts()
            stats = build_stats(contacts)
            payload = json.dumps({"contacts": contacts, "stats": stats})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            self.wfile.write(payload.encode())
        elif self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode())
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        pass  # silence request logs


if __name__ == "__main__":
    server = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"\n  Arcadia Outreach CRM Dashboard")
    print(f"  http://localhost:{PORT}\n")
    print(f"  Scanning: {AGENT_ROOT}")
    print(f"  Auto-refresh: every 30s\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
