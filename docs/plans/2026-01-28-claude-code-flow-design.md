# Claude Code Flow Design

## Overview

Redesign PyMOL-MCP for a Claude Code-centric workflow, replacing the Claude Desktop + MCP server architecture with direct socket communication.

## Architecture

```
┌─────────────────┐          TCP Socket          ┌─────────────────┐
│   Claude Code   │────────────────────────────►│     PyMOL       │
│   (terminal)    │         port 9876            │   (separate)    │
└─────────────────┘                              └─────────────────┘
```

**Direct socket communication, no MCP layer.**

Claude Code sends Python/PyMOL commands directly over a TCP socket to PyMOL. No intermediate MCP server.

**Why this works:**
- Claude Code can write PyMOL Python code natively
- Skills provide discoverability and patterns (replacing MCP command definitions)
- Simpler architecture = fewer failure points
- One less process to manage

**What gets removed:**
- `pymol_mcp_server.py` - no longer needed
- MCP configuration in Claude Desktop config
- Regex-based command parsing

**What stays:**
- Socket plugin in PyMOL (modified)
- Skills for PyMOL knowledge
- COOKBOOK.md for user reference

## Plugin Redesign

**Current plugin:** Pop-out window with start/stop toggle, PyQt5-based UI.

**New plugin:** Headless socket listener, no window.

**Behavior:**
- Starts automatically when PyMOL launches (via pymolrc)
- Prints one-time message: `"Claude socket listener active on port 9876"`
- Runs in background, no visible UI
- User can check status with `bridge_status` command

**Commands exposed to user:**
- `bridge_status` - prints connection state and port
- `bridge_stop` - stops the listener (for debugging/troubleshooting)
- `bridge_start` - restarts the listener

**Technical changes:**
- Remove PyQt5 dependency and window code
- Socket listener runs in a background thread
- Auto-starts on plugin load (no manual toggle)
- Simpler codebase overall

**Output handling:**
- Command output still captured and returned over socket
- Errors returned with clear messages
- Same exec-based execution model, just without the UI wrapper

## Bootstrapping & Setup

**Two entry points, same logic:**

1. **Explicit:** User runs `/pymol-setup` skill
2. **Automatic:** User asks to open PyMOL, I detect missing setup and run it

**What setup does:**

1. **Verify PyMOL installation**
   - Check `pymol` command exists and runs
   - Report version, confirm it works

2. **Install/update plugin**
   - Copy plugin file to PyMOL's plugin directory (or a known location)
   - Plugin is a single `.py` file, no complex installation

3. **Configure pymolrc**
   - Add `run /path/to/claude_socket_plugin.py` to user's pymolrc
   - Create pymolrc if it doesn't exist
   - Ensures plugin auto-loads on every PyMOL launch

4. **Test connection**
   - Launch PyMOL
   - Attempt socket connection
   - Send a simple command, verify response
   - Report success or diagnose failure

**After setup:** User can say "open PyMOL" anytime and it launches ready to go. Or they can launch PyMOL themselves and Claude connects to the existing instance.

## Session Management

**Launching PyMOL:**

When user asks to open PyMOL (or load a structure, etc.):
1. Check if PyMOL is already running with socket listener
2. If yes → connect to existing instance
3. If no → spawn `pymol` (or `pymol file.pdb`), wait for socket to be ready, connect

**Connecting to existing:**

If PyMOL is already open:
- Attempt connection on port 9876
- If plugin is running, connected
- If not (plugin not loaded), inform user and suggest restarting PyMOL or running `bridge_start`

**Reconnection:**

If connection drops mid-session:
- Silently attempt to reconnect (a few retries with short delays)
- If reconnect succeeds, continue normally - user doesn't notice
- If reconnect fails, inform user: "Lost connection to PyMOL. Want me to relaunch it?"

**Closing:**

No special handling needed. User can:
- Close PyMOL normally, or
- Leave it open for next time

## Deliverables

**In scope:**

1. **New plugin** (`claude_socket_plugin.py`)
   - Headless socket listener
   - Auto-start, no window
   - `bridge_status`, `bridge_stop`, `bridge_start` commands

2. **Setup skill** (`/pymol-setup`)
   - Verifies PyMOL, installs plugin, configures pymolrc, tests connection

3. **Connection skill** (`/pymol-connect` or similar)
   - Handles launching PyMOL or connecting to existing
   - Could also be automatic when user asks to work with PyMOL

4. **Socket communication module**
   - Python code for sending commands and receiving responses
   - Handles connection, reconnection, error handling

**Out of scope (future work):**

- Adapting existing skills for new flow
- Removing old MCP server code (can coexist for now)
- Claude Desktop support
- Bidirectional PyMOL→Claude communication

## Files Affected

- New: `claude_socket_plugin.py` (replacing or alongside current plugin)
- New: `.claude/skills/pymol-setup/`
- New: Connection helper (skill or utility module)
- Unchanged for now: `pymol_mcp_server.py`, existing skills
