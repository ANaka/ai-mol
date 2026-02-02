# ai-mol Distribution Design

## Decision

Monorepo with two distribution paths:
- **pip package** (`ai-mol`) for PyMOL plugin + connection code
- **Claude Code plugin** (`ai-mol-skills`) for skills, distributed from same repo

## Target Users

Both:
- Claude Code users who want PyMOL integration
- PyMOL users who want AI assistance

## Repository Structure

```
ai-mol/
├── pyproject.toml              # pip package config
├── src/
│   └── ai_mol/
│       ├── __init__.py
│       ├── connection.py       # PyMOLConnection class
│       ├── session.py          # Session management
│       ├── view.py             # View utilities
│       ├── plugin.py           # Socket plugin (copied to PyMOL)
│       └── cli.py              # Entry point for `ai-mol setup`
├── claude-plugin/              # Claude Code plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       ├── pymol-fundamentals/
│       ├── binding-site-visualization/
│       ├── antibody-visualization/
│       └── ... (all skills)
└── README.md
```

## Distribution

### pip package

```bash
pip install ai-mol
ai-mol setup  # Installs PyMOL plugin, configures ~/.pymolrc
```

Package includes:
- `ai_mol.connection` - Socket communication with PyMOL
- `ai_mol.session` - Session management utilities
- CLI command `ai-mol setup` to configure PyMOL

### Claude Code plugin

```bash
/plugin marketplace add your-org/ai-mol?path=claude-plugin
/plugin install ai-mol-skills
```

Plugin includes:
- All visualization skills (pymol-fundamentals, binding-site, antibody, etc.)
- README pointing to pip package for setup

## User Flows

**PyMOL user discovers pip package:**
1. `pip install ai-mol`
2. `ai-mol setup`
3. README mentions: "For Claude Code users, install the skills plugin"

**Claude Code user discovers skills plugin:**
1. `/plugin marketplace add ...`
2. `/plugin install ai-mol-skills`
3. Plugin README says: "Requires `pip install ai-mol && ai-mol setup`"

## Versioning

Single version in pyproject.toml applies to pip package. Plugin has its own version in plugin.json. They can diverge but should stay roughly aligned.

## Trade-offs Accepted

- Coupled git history (skills + code together)
- Plugin install URL slightly longer due to path parameter
- Need to coordinate if versions diverge significantly

## Next Steps

1. Rename pyproject.toml from `mcp-rosetta` to `ai-mol`
2. Restructure into `src/ai_mol/` layout
3. Add CLI entry point for `ai-mol setup`
4. Move skills to `claude-plugin/skills/`
5. Create `claude-plugin/.claude-plugin/plugin.json`
6. Write READMEs for both distribution paths
7. Test both install paths
