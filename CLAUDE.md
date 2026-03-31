# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`claudemol` is a **skills-only** repository providing structural biology and molecular visualization expertise for Claude Code. It depends on `pymol-agent-bridge` for all infrastructure and connectivity.

## Repository Structure

```
claudemol/
├── claude-plugin/        # Claude Code plugin (distributed)
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── hooks/
│   │   └── hooks.json    # SessionStart hooks
│   └── skills/           # All visualization skills (the core of this repo)
└── .claude/skills/       # Local skills (used by Claude when working in this repo)
```

## Architecture

```
Claude Code → claudemol-skills (Expertise) → pymol-agent-bridge (Infrastructure) → PyMOL
```

- **Expertise**: The skills in `claude-plugin/skills/` define *how* to perform complex structural biology tasks (antibody viz, binding sites, etc.).
- **Infrastructure**: All "plumbing" is handled by the `pymol-agent-bridge` package.

## Dependency: `pymol-agent-bridge`

All commands are executed via the `pymol-agent-bridge` CLI. 

- **Wrapper Path**: `~/.pymol-agent-bridge/bin/pymol-agent-bridge`
- **Commands**: `setup`, `status`, `test`, `info`, `launch`, `exec`
- **PyMOL Commands**: `bridge_status`, `bridge_stop`, `bridge_start`
- **Socket**: localhost:9880

## Distribution

**Claude Code plugin:**
```bash
/plugin marketplace add ANaka/claudemol
/plugin install claudemol-skills
```

**Prerequisite:**
```bash
pip install pymol-agent-bridge
pymol-agent-bridge setup
```

## Maintenance Rules

1. **Skills First**: This repo is for developing and maintaining structural biology skills. Do not add core infrastructure code here.
2. **Canonical Patterns**:
   - Use `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "..."` for all PyMOL commands.
   - Use heredocs for multi-line Python code.
   - Use `bridge_status` to check connection from within PyMOL.
3. **Syncing Skills**: Keep `claude-plugin/skills/` (distributed) and `.claude/skills/` (local dev) in sync. 
4. **No `claudemol` Package**: The `src/claudemol/` directory has been removed. All references to the `claudemol` binary must be updated to `pymol-agent-bridge`.

## Development Commands

Since this is now a skills-only repo, traditional Python tests are mostly deprecated, but the following are useful for development:

```bash
# Check for remaining claudemol references
grep -r "claudemol" . --exclude-dir=.git

# Verify all skill files are present
ls -R claude-plugin/skills/
```

## Key Code Patterns

- `~/.pymol-agent-bridge/bin/pymol-agent-bridge exec "cmd.fetch('1ubq')"`
- `~/.pymol-agent-bridge/bin/pymol-agent-bridge launch`
- `~/.pymol-agent-bridge/bin/pymol-agent-bridge status`
