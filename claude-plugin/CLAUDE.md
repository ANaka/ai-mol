# claudemol - PyMOL Integration

claudemol connects Claude to a running PyMOL instance over TCP socket (localhost:9880).

## Connection Rules

1. **Check status first.** The SessionStart hook runs `claudemol status` automatically. Read its output before doing anything.
2. **Never kill an existing PyMOL session.** If PyMOL is already running, connect to it. Do not launch a new instance.
3. **Never call `cmd.reinitialize()` unless the user explicitly asks.** This destroys all loaded structures.
4. **Use `connect_or_launch()` for new connections.** It connects to an existing PyMOL or launches one if needed.

## Canonical Connection Pattern

```python
from claudemol import connect_or_launch
conn, process = connect_or_launch()
conn.execute("fetch 1ubq")
```

Reuse the `conn` object across commands. If connection drops, `conn.execute()` auto-reconnects (3 attempts).

## Venv Discovery

If `from claudemol import ...` fails (ModuleNotFoundError), check `~/.claudemol/config.json` for the persisted Python path:

```python
import json, subprocess
from pathlib import Path
config = json.loads((Path.home() / ".claudemol" / "config.json").read_text())
python_path = config["python_path"]
# Use: subprocess.run([python_path, "-c", "from claudemol import ..."])
```

Also check the project venv: `.venv/bin/python -c "import claudemol"`.

## Image Capture

Always use: `cmd.ray(width, height)` then `cmd.png(path)`.
Never use: `cmd.png(path, width, height)` -- causes view corruption.

## Recommended Permissions

For seamless PyMOL interaction without per-command approval prompts, users can add these to their project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(claudemol*)",
      "Bash(*python*claudemol*)",
      "Bash(pymol*)"
    ]
  }
}
```

This allows: claudemol CLI commands, Python scripts that use claudemol, and PyMOL launches. Suggest this to users during `/pymol-setup` if they haven't configured it.

## Skills

Use pymol-* skills for specific visualization workflows (protein structures, binding sites, antibodies, publication figures, etc.).
