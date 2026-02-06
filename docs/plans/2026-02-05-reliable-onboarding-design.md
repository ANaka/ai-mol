# Reliable Onboarding Design

**Problem:** When claudemol is installed in another project (pip package + Claude Code plugin), Claude doesn't have enough context to reliably connect to PyMOL. It makes multiple connection attempts and calls functions that kill existing PyMOL sessions.

**Root causes:**
1. No CLAUDE.md ships with the plugin — Claude has no persistent baseline context
2. The pymol-connect skill shows disconnected code snippets instead of a prescriptive flow
3. Claude doesn't know PyMOL's install/run status until it tries and fails

**Scope:** Plugin CLAUDE.md + rewritten skill + SessionStart hook. No changes to connection.py or session.py.

## Design

### 1. SessionStart Hook

**File:** `claude-plugin/hooks/hooks.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "claudemol status 2>/dev/null || echo 'claudemol not installed or PyMOL not running'",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Runs `claudemol status` on every session start. Claude sees PyMOL install location + connection status automatically. No caching needed — always fresh, ~1 second.

### 2. Plugin CLAUDE.md

**File:** `claude-plugin/CLAUDE.md`

Persistent baseline context (~30 lines). Contains:

- What claudemol is (TCP socket on localhost:9880)
- Connection rules:
  - Check status first (hook output)
  - Never kill existing PyMOL sessions
  - Never call `cmd.reinitialize()` unless user asks
  - Use `PyMOLConnection`, not `PyMOLSession`
- Canonical 3-line connection pattern
- Image capture rule (`cmd.ray()` then `cmd.png()`, never `cmd.png(path, w, h)`)
- Pointer to pymol-* skills for workflows

### 3. Rewritten pymol-connect Skill

**File:** `claude-plugin/skills/pymol-connect/SKILL.md` (replaces existing)

Changes from current version:
- Single linear decision tree instead of disconnected snippets
- Step 1: Read hook output to determine state
- Step 2: Launch only if nothing is running
- Step 3: Connect and verify, reuse connection object
- Explicit rules: never use PyMOLSession, never reinitialize, never relaunch on connection drop

## Files Changed

| File | Action |
|------|--------|
| `claude-plugin/hooks/hooks.json` | Create |
| `claude-plugin/CLAUDE.md` | Create |
| `claude-plugin/skills/pymol-connect/SKILL.md` | Rewrite |

## Not in Scope

- Changes to `session.py` (recover() aggressiveness)
- Changes to `connection.py`
- New CLI commands
