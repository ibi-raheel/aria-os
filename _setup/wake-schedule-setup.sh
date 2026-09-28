#!/bin/bash
# ============================================================================
#  Aria Agent OS — Mac wake-schedule setup
# ============================================================================
#  Run once with sudo. Sets a daily macOS wake at 01:55 local so the early
#  agent chain (02:00 news → 02:30 discovery → 02:50 qualify → 05:00 send)
#  fires into a live Chrome environment instead of a sleeping Mac.
#
#  Without this: scheduled tasks fire at 02:00, Mac is asleep, Chrome MCP
#  has no live extension to talk to, every Chrome tool call hangs until
#  timeout. The agent reports cryptic "MCP server not connected" errors.
#
#  With this: Mac wakes at 01:55, Chrome auto-relaunches (provided macOS
#  "Reopen apps on relaunch" is on — the default), extension reconnects
#  within ~10s, scheduled tasks fire into a working environment.
#
#  Usage:
#      sudo bash wake-schedule-setup.sh
#
#  Undo:
#      sudo pmset repeat cancel
#
#  Note: macOS only supports ONE pmset repeat schedule. If you ever need
#  multiple recurring wakes, switch to a launchd daemon that issues
#  one-shot `pmset schedule` commands daily.
# ============================================================================

set -euo pipefail

if [[ $EUID -ne 0 ]]; then
   echo "ERROR: This script must be run with sudo."
   echo "Usage: sudo bash $0"
   exit 1
fi

echo "=== Aria Agent OS — wake schedule setup ==="
echo
echo "Current pmset schedule (before):"
pmset -g sched || true
echo
echo "Setting daily wake at 01:55 (every day, MTWRFSU)..."
echo "This wakes the Mac so the 02:00-05:00 agent chain on Mon/Wed/Fri can run."
echo

# pmset repeat — one schedule entry, recurring on specified weekdays.
# wakeorpoweron: wake from sleep OR power on if Mac is shut down (with auto-on enabled).
# MTWRFSU: every day of the week.
pmset repeat wakeorpoweron MTWRFSU 01:55:00

echo
echo "✓ Schedule applied. Verifying:"
pmset -g sched
echo
echo "============================================================"
echo "Done. The Mac will wake at 01:55 every day."
echo
echo "Three things to verify on your end:"
echo
echo "  1. Chrome 'Continue where you left off' is on:"
echo "     Chrome → Settings → On startup → Continue where you left off"
echo
echo "  2. macOS 'Reopen windows when logging back in' is on:"
echo "     Should be on by default. Verify on the next wake by checking"
echo "     that Chrome relaunches with your tabs."
echo
echo "  3. The Claude in Chrome extension is connected to your account."
echo "     Open the extension popup → confirm 'Connected'."
echo
echo "If a scheduled task still fails to find Chrome MCP, the agent will"
echo "now post a clear failure message to its Slack channel instead of"
echo "silently timing out (per the pre-flight check added 2026-05-06)."
echo
echo "Decision record:"
echo "  memory/decisions/2026-05-06-chrome-mcp-reliability-fixes.md"
echo "============================================================"
