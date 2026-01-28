# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

PyMOL-MCP integrates PyMOL (molecular visualization software) with Claude AI through the Model Context Protocol (MCP). It enables Claude to control PyMOL via natural language commands for structural biology and molecular visualization tasks.

## Architecture

**Two-component system:**

1. **MCP Server** (`pymol_mcp_server.py`) - FastMCP-based server that Claude Desktop connects to
   - Defines 100+ PyMOL commands with regex patterns for validation
   - `PyMOLConnection` class handles TCP socket communication (port 9876)
   - `parse_pymol_input()` matches user text against `PYMOL_COMMANDS` patterns
   - `build_pymol_code()` converts matched commands to `cmd.*` Python calls
   - Single MCP tool exposed: `parse_and_execute(user_input)`

2. **PyMOL Plugin** (`pymol-mcp-socket-plugin/__init__.py`) - Socket listener running inside PyMOL
   - `SocketServer` class accepts connections and executes received Python code
   - Uses PyQt5 for UI (start/stop listening toggle)
   - Runs on localhost:9876 by default
   - Commands executed via Python `exec()` with output capture

**Communication flow:** Claude Desktop → MCP Server → TCP Socket → PyMOL Plugin → `cmd.*` execution

## Development Commands

```bash
# Setup
python -m venv venv
source venv/bin/activate  # macOS/Linux
pip install mcp

# Linting (ruff configured for E, F, I rules)
ruff check .
ruff format .

# Type checking
pyright
```

## Configuration

Claude Desktop config (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "pymol": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/pymol_mcp_server.py"]
    }
  }
}
```

## Development Goals

A main goal of this project is to build out a good set of skills for Claude to interact with PyMOL. When you learn something important about PyMOL commands, common workflows, or useful patterns, consider adding it as a skill.

## Key Code Patterns

- Command definitions in `PYMOL_COMMANDS` dict include: description, regex pattern, parameters (with required/optional/default/options), and `check_selection` flag
- Error patterns defined in `ERROR_PATTERNS` for output analysis
- Global connection singleton via `get_pymol_connection()` with auto-reconnect
- Plugin handles multiple clients but only one active connection at a time
