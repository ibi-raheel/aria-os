// Aria Agent OS — Localhost Dashboard Server
// Reads directly from the OS file system. NO cached data layer.
// If a number on the dashboard looks weird, click through — the source file
// is the one source of truth.

const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');

const OS_ROOT = path.resolve(__dirname, '..');
const VAULT_NAME = 'Aria Agent OS';
const PORT = process.env.PORT || 4321;

const app = express();
app.use(express.static(path.join(__dirname, 'public')));

// ── helpers ───────────────────────────────────────────────────────────

function todayStr() {
  // Local-date YYYY-MM-DD
  const now = new Date();
  const tz = now.getTimezoneOffset() * 60000;
  return new Date(now - tz).toISOString().slice(0, 10);
}

async function readFileSafe(p) {
  try {
    return await fs.readFile(p, 'utf8');
  } catch {
    return null;
  }
}

async function listDirSafe(p) {
  try {
    return await fs.readdir(p);
  } catch {
    return [];
  }
}

async function statSafe(p) {
  try {
    return await fs.stat(p);
  } catch {
    return null;
  }
}

// ── API: today's pipeline summary ────────────────────────────────────

app.get('/api/pipeline/today', async (req, res) => {
  const today = todayStr();
  const out = { date: today, news: {}, networking: {}, integrity: {} };

  // News briefings + anchors
  const briefDir = path.join(OS_ROOT, 'news-agent/briefings', today);
  const briefFiles = await listDirSafe(briefDir);
  out.news.briefingsCount = briefFiles.filter(f => f.endsWith('.md') && !f.includes('-anchors')).length;
  out.news.anchorsCount = briefFiles.filter(f => f.endsWith('-anchors.md')).length;
  out.news.sourcePath = `news-agent/briefings/${today}/`;
  out.news.exists = briefFiles.length > 0;

  // Networking discovery
  const discDir = path.join(OS_ROOT, 'networking-agent/02-discovery/output', today);
  const discBuckets = await listDirSafe(discDir);
  let discTotal = 0;
  let discBuckets_data = [];
  for (const bucket of discBuckets) {
    const candFile = await readFileSafe(path.join(discDir, bucket, 'candidates.md'));
    if (candFile) {
      const matches = candFile.match(/^## Candidate /gm);
      const n = matches ? matches.length : 0;
      discTotal += n;
      discBuckets_data.push({ bucket, count: n });
    }
  }
  out.networking.discoveryCount = discTotal;
  out.networking.discoveryByBucket = discBuckets_data;
  out.networking.discoveryPath = `networking-agent/02-discovery/output/${today}/`;

  // Networking qualify
  const qDir = path.join(OS_ROOT, 'networking-agent/03-qualify/output', today);
  const qBuckets = await listDirSafe(qDir);
  let qTotal = 0;
  for (const bucket of qBuckets) {
    const rankedFile = await readFileSafe(path.join(qDir, bucket, 'ranked.md'));
    if (rankedFile) {
      const matches = rankedFile.match(/^## \d+\./gm);
      qTotal += matches ? matches.length : 0;
    }
  }
  out.networking.qualifiedCount = qTotal;
  out.networking.qualifyPath = `networking-agent/03-qualify/output/${today}/`;

  // Networking sent today (files mtime today in 06-send/output)
  const sendDir = path.join(OS_ROOT, 'networking-agent/06-send/output');
  const sendFiles = await listDirSafe(sendDir);
  let sentToday = 0;
  for (const f of sendFiles) {
    if (!f.endsWith('.md') || f.startsWith('README')) continue;
    const st = await statSafe(path.join(sendDir, f));
    if (st && st.mtime.toISOString().slice(0, 10) === today) sentToday++;
  }
  out.networking.sentToday = sentToday;
  out.networking.sentTotal = sendFiles.filter(f => f.endsWith('.md') && !f.startsWith('README')).length;
  out.networking.sendPath = 'networking-agent/06-send/output/';

  // Integrity — latest validate-* report
  const intDir = path.join(OS_ROOT, 'memory/integrity');
  const intFiles = await listDirSafe(intDir);
  const validateFiles = intFiles.filter(f => f.startsWith('validate-')).sort();
  const latest = validateFiles[validateFiles.length - 1];
  if (latest) {
    const content = await readFileSafe(path.join(intDir, latest));
    const verdictMatch = content && content.match(/^verdict:\s*([^\n]+)/m);
    const filesMatch = content && content.match(/files_scanned:\s*(\d+)/);
    const fixesMatch = content && content.match(/fixes_applied:\s*(\d+)/);
    out.integrity.latestVerdict = verdictMatch ? verdictMatch[1].trim() : 'unknown';
    out.integrity.filesScanned = filesMatch ? parseInt(filesMatch[1], 10) : 0;
    out.integrity.fixesApplied = fixesMatch ? parseInt(fixesMatch[1], 10) : 0;
    out.integrity.latestReport = latest;
    out.integrity.sourcePath = `memory/integrity/${latest}`;
  }

  res.json(out);
});

// ── API: scheduled tasks (with last-run inferred from daily log) ─────

const KNOWN_TASKS = [
  { id: 'news-agent-daily-run', name: 'News fetch + categorize + anchors', schedule: '02:00 weekdays', cron: '0 2 * * 1-5', matchAgent: 'news-agent' },
  { id: 'networking-agent-discovery', name: 'Networking discovery (LinkedIn)', schedule: '02:30 weekdays', cron: '30 2 * * 1-5', matchAgent: 'networking-agent.*discover' },
  { id: 'networking-agent-qualify', name: 'Networking qualify + rank', schedule: '02:50 weekdays', cron: '50 2 * * 1-5', matchAgent: 'networking-agent.*qualif' },
  { id: 'networking-agent-daily-run', name: 'Networking send (20 invites)', schedule: '05:00 weekdays', cron: '0 5 * * 1-5', matchAgent: 'networking-agent.*send' },
  { id: 'hygiene-integrity-check', name: 'Daily integrity audit', schedule: '22:00 weekdays', cron: '0 22 * * 1-5', matchAgent: 'hygiene-agent.*integrity|hygiene-agent.*validate' },
  { id: 'hygiene-memory-consolidate', name: 'Weekly consolidation', schedule: '22:00 Sunday', cron: '0 22 * * 0', matchAgent: 'hygiene-agent.*consolidate' },
];

app.get('/api/scheduled-tasks', async (req, res) => {
  const today = todayStr();
  const dailyContent = await readFileSafe(path.join(OS_ROOT, 'memory/daily', `${today}.md`));

  const tasks = KNOWN_TASKS.map(t => {
    let ranToday = false;
    let lastSeenInLog = null;
    if (dailyContent) {
      const re = new RegExp(t.matchAgent, 'i');
      const blockRe = /^##\s+(\d{1,2}:\d{2})\s+—\s+([^\n]+)$/gm;
      let m;
      while ((m = blockRe.exec(dailyContent)) !== null) {
        if (re.test(m[2])) {
          ranToday = true;
          lastSeenInLog = m[1];
        }
      }
    }
    return {
      id: t.id,
      name: t.name,
      schedule: t.schedule,
      cron: t.cron,
      ranToday,
      lastSeenInLog,
      sourcePath: ranToday ? `memory/daily/${today}.md` : null,
    };
  });

  res.json({ tasks, sourcePath: `memory/daily/${today}.md` });
});

// ── API: memory stats ─────────────────────────────────────────────────

app.get('/api/memory-stats', async (req, res) => {
  const counts = {};
  for (const folder of ['people', 'companies', 'decisions', 'integrity', 'inbox']) {
    const files = await listDirSafe(path.join(OS_ROOT, 'memory', folder));
    counts[folder] = files.filter(f => f.endsWith('.md') && !f.startsWith('_') && !f.startsWith('.')).length;
  }
  // Daily log count includes today
  const dailyFiles = await listDirSafe(path.join(OS_ROOT, 'memory/daily'));
  counts.dailyLogs = dailyFiles.filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f)).length;

  // _INDEX.md last modified
  const idxStat = await statSafe(path.join(OS_ROOT, 'memory/_INDEX.md'));
  counts.indexLastModified = idxStat ? idxStat.mtime.toISOString() : null;
  counts.indexAgeHours = idxStat ? Math.floor((Date.now() - idxStat.mtime.getTime()) / 3600000) : null;
  counts.indexSourcePath = 'memory/_INDEX.md';

  res.json(counts);
});

// ── API: recent activity (parsed from today's daily log) ─────────────

app.get('/api/activity/recent', async (req, res) => {
  const today = todayStr();
  const filePath = `memory/daily/${today}.md`;
  const content = await readFileSafe(path.join(OS_ROOT, filePath));
  if (!content) {
    return res.json({ entries: [], sourcePath: filePath, exists: false });
  }
  // Parse "## HH:MM — agent — title" blocks
  // Capture body too (until next ##)
  const blockRegex = /^##\s+(\d{1,2}:\d{2})\s+—\s+([^—\n]+)\s+—\s+([^\n]+)$([\s\S]*?)(?=^##|\Z)/gm;
  const entries = [];
  let m;
  while ((m = blockRegex.exec(content)) !== null) {
    const body = (m[4] || '').trim();
    const firstLine = body.split('\n').filter(l => l.trim()).slice(0, 1)[0] || '';
    entries.push({
      time: m[1].trim(),
      agent: m[2].trim(),
      title: m[3].trim(),
      excerpt: firstLine.length > 200 ? firstLine.slice(0, 200) + '…' : firstLine,
    });
  }
  // Most recent first
  entries.reverse();
  res.json({ entries, sourcePath: filePath, exists: true });
});

// ── API: token usage ──────────────────────────────────────────────────
// Reads `tokens: ~N` or `tokens_used: N` patterns in today's daily log entries.
// Empty until scheduled tasks are instrumented to write token counts.

app.get('/api/tokens', async (req, res) => {
  const today = todayStr();
  const filePath = `memory/daily/${today}.md`;
  const content = await readFileSafe(path.join(OS_ROOT, filePath));
  let total = 0;
  const perAgent = {};
  let entries = 0;
  if (content) {
    const blockRe = /^##\s+\d{1,2}:\d{2}\s+—\s+([^—\n]+?)\s+—.*$([\s\S]*?)(?=^##|\Z)/gm;
    let m;
    while ((m = blockRe.exec(content)) !== null) {
      const agent = m[1].trim();
      const body = m[2];
      const tokenMatch = body.match(/\btokens(?:_used)?:\s*~?([\d,]+)/i);
      if (tokenMatch) {
        const n = parseInt(tokenMatch[1].replace(/,/g, ''), 10);
        total += n;
        perAgent[agent] = (perAgent[agent] || 0) + n;
        entries++;
      }
    }
  }
  res.json({
    today: total,
    perAgent,
    instrumentedRuns: entries,
    note: entries === 0
      ? 'No token-instrumented runs yet. Each scheduled task should append `tokens: ~N` to its daily log entry.'
      : null,
    sourcePath: filePath,
  });
});

// ── API: CRM — aggregate dossiers + engagement records ──────────────

// Parse frontmatter into { ...keys, _body }
function parseFrontmatter(content) {
  if (!content) return { _body: '' };
  const m = content.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { _body: content };
  const fm = {};
  const lines = m[1].split('\n');
  for (const line of lines) {
    const kv = line.match(/^([a-z_][a-z0-9_-]*)\s*:\s*(.*)$/i);
    if (kv) fm[kv[1].trim()] = kv[2].trim().replace(/^['"]|['"]$/g, '');
  }
  fm._body = m[2];
  return fm;
}

// Pull Platform from dossier body. Handles both:
//   **Platform:** [[memory/companies/skool|Skool]]
//   **Platform:** Plain text description
function extractPlatform(body) {
  if (!body) return null;
  const m = body.match(/\*?\*?Platform:?\*?\*?\s*([^\n]+)/i);
  if (!m) return null;
  let v = m[1].trim().replace(/^\*+|\*+$/g, '').trim();
  // wikilink with display text
  const wl = v.match(/\[\[(?:[^\|\]]+)\|([^\]]+)\]\]/);
  if (wl) return wl[1].trim();
  // bare wikilink
  const wlBare = v.match(/\[\[([^\]]+)\]\]/);
  if (wlBare) return wlBare[1].split('/').pop().trim();
  return v.length > 80 ? v.slice(0, 80) + '…' : v;
}

// Prefer frontmatter `name:`, then body H1, then humanized slug
function extractName(fm, body, slug) {
  if (fm && fm.name && fm.name.length > 0) return fm.name;
  if (body) {
    const m = body.match(/^#\s+(.+)$/m);
    if (m) return m[1].trim();
  }
  return slugToName(slug);
}

function slugToName(slug) {
  return slug
    .split('-')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
}

// Engagement-status priority: highest wins
const STATUS_RANK = {
  'replied': 5,
  'closed-won': 5,
  'warm': 4,
  'sent': 3,
  'drafted': 2,
  'enriched': 1,
  'qualified': 1,
  'identified': 0,
  'skipped': -1,
  'closed-lost': -1,
  'declined': -1,
  'dormant': -1,
};

function statusRank(s) {
  if (!s) return 0;
  return STATUS_RANK[s.toLowerCase()] ?? 0;
}

const ENGAGEMENT_LOCATIONS = [
  // outreach-agent-arcadia stages
  { agent: 'outreach-arcadia', path: 'outreach-agent-arcadia/stages/01-discovery/output' },
  { agent: 'outreach-arcadia', path: 'outreach-agent-arcadia/stages/02-qualification/output' },
  { agent: 'outreach-arcadia', path: 'outreach-agent-arcadia/stages/03-enrichment/output' },
  { agent: 'outreach-arcadia', path: 'outreach-agent-arcadia/stages/04-personalization/output' },
  { agent: 'outreach-arcadia', path: 'outreach-agent-arcadia/stages/05-send/output' },
  { agent: 'outreach-arcadia', path: 'outreach-agent-arcadia/stages/06-followup/output' },
  // networking-agent
  { agent: 'networking', path: 'networking-agent/06-send/output' },
  { agent: 'networking', path: 'networking-agent/07-track/accepted' },
  { agent: 'networking', path: 'networking-agent/07-track/ignored' },
  { agent: 'networking', path: 'networking-agent/07-track/job-pipeline' },
];

app.get('/api/crm/people', async (req, res) => {
  const peopleDir = path.join(OS_ROOT, 'memory/people');
  const files = await listDirSafe(peopleDir);
  const dossierSlugs = files
    .filter(f => f.endsWith('.md') && !f.startsWith('_') && !f.startsWith('.'))
    .map(f => f.replace(/\.md$/, ''));

  // Build engagement index: slug → [engagements]
  const engagementsBySlug = {};
  for (const loc of ENGAGEMENT_LOCATIONS) {
    const dir = path.join(OS_ROOT, loc.path);
    const stageFiles = await listDirSafe(dir);
    for (const f of stageFiles) {
      if (!f.endsWith('.md') || f.startsWith('README') || f.startsWith('_')) continue;
      const slug = f.replace(/\.md$/, '');
      const content = await readFileSafe(path.join(dir, f));
      const fm = parseFrontmatter(content);
      const stage = loc.path.match(/(\d{2}-[a-z-]+)/);
      engagementsBySlug[slug] = engagementsBySlug[slug] || [];
      engagementsBySlug[slug].push({
        agent: loc.agent,
        stage: stage ? stage[1] : null,
        status: fm.status || null,
        sent_at: fm.sent_at || null,
        sent_channel: fm.sent_channel || null,
        failed_channels: fm.failed_channels || null,
        segment: fm.segment || null,
        path: `${loc.path}/${f}`,
      });
    }
  }

  // Build people array
  const people = [];
  for (const slug of dossierSlugs) {
    const dossierContent = await readFileSafe(path.join(peopleDir, `${slug}.md`));
    const fm = parseFrontmatter(dossierContent);
    const body = fm._body || '';
    const engagements = engagementsBySlug[slug] || [];

    // Top status (highest rank)
    let topStatus = null;
    let topRank = -Infinity;
    for (const e of engagements) {
      const r = statusRank(e.status);
      if (r > topRank) { topRank = r; topStatus = e.status; }
    }
    if (!topStatus && engagements.length === 0) topStatus = 'no-engagement';
    if (!topStatus) topStatus = 'identified';

    // Latest sent_at
    let lastTouchedAt = null;
    for (const e of engagements) {
      if (e.sent_at && (!lastTouchedAt || e.sent_at > lastTouchedAt)) lastTouchedAt = e.sent_at;
    }

    people.push({
      slug,
      name: extractName(fm, body, slug),
      platform: extractPlatform(body),
      segment: fm.segment || (engagements[0] && engagements[0].segment) || null,
      topStatus,
      lastTouchedAt,
      engagements: engagements.map(e => ({ agent: e.agent, status: e.status, sent_at: e.sent_at, path: e.path, stage: e.stage })),
      engagementCount: engagements.length,
      dossierPath: `memory/people/${slug}.md`,
    });
  }

  // Also surface engagement records without a dossier (data integrity issue)
  const orphanEngagements = [];
  for (const slug of Object.keys(engagementsBySlug)) {
    if (!dossierSlugs.includes(slug)) {
      orphanEngagements.push({
        slug,
        name: slugToName(slug),
        platform: null,
        segment: null,
        topStatus: 'orphan',
        lastTouchedAt: null,
        engagements: engagementsBySlug[slug].map(e => ({ agent: e.agent, status: e.status, sent_at: e.sent_at, path: e.path, stage: e.stage })),
        engagementCount: engagementsBySlug[slug].length,
        dossierPath: null,
        orphan: true,
      });
    }
  }

  // Sort: most recently touched first, then alphabetical
  const all = [...people, ...orphanEngagements].sort((a, b) => {
    if (a.lastTouchedAt && b.lastTouchedAt) return b.lastTouchedAt.localeCompare(a.lastTouchedAt);
    if (a.lastTouchedAt) return -1;
    if (b.lastTouchedAt) return 1;
    return a.name.localeCompare(b.name);
  });

  // Aggregate counts
  const summary = {
    total: all.length,
    withDossier: people.length,
    orphans: orphanEngagements.length,
    byStatus: {},
  };
  for (const p of all) {
    summary.byStatus[p.topStatus] = (summary.byStatus[p.topStatus] || 0) + 1;
  }

  res.json({ people: all, summary });
});

// ── API: open file in Obsidian ───────────────────────────────────────

app.get('/api/open', (req, res) => {
  const relPath = req.query.path;
  if (!relPath) return res.status(400).json({ error: 'missing path' });
  const safe = path.normalize(path.join(OS_ROOT, relPath));
  if (!safe.startsWith(OS_ROOT)) return res.status(403).json({ error: 'forbidden' });

  // Trim trailing slash if it's a folder — open in Finder instead
  const isDir = relPath.endsWith('/');
  if (isDir) {
    exec(`open "${safe}"`, () => {});
    return res.json({ ok: true, opened: 'finder', path: relPath });
  }

  // Strip .md extension for Obsidian (it figures out the file)
  const fileForObsidian = relPath.replace(/\.md$/, '');
  const url = `obsidian://open?vault=${encodeURIComponent(VAULT_NAME)}&file=${encodeURIComponent(fileForObsidian)}`;
  exec(`open "${url}"`, (err) => {
    if (err) {
      // Fallback to system open
      exec(`open "${safe}"`, () => {});
    }
  });
  res.json({ ok: true, opened: 'obsidian', path: relPath });
});

// ── Start ─────────────────────────────────────────────────────────────

app.listen(PORT, () => {
  console.log('');
  console.log('  ╭──────────────────────────────────────────────╮');
  console.log('  │  Aria Agent OS — Dashboard                   │');
  console.log(`  │  http://localhost:${PORT}                          │`.padEnd(50) + '│');
  console.log('  ╰──────────────────────────────────────────────╯');
  console.log('');
  console.log(`  Reading from: ${OS_ROOT}`);
  console.log('  No cached data — every request reads source files.');
  console.log('  Click any card or row to open the file in Obsidian.');
  console.log('');
});
