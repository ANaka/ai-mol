# claudemol - PyMOL Integration

claudemol connects Claude to a running PyMOL instance over TCP socket (localhost:9880).

## Connection Rules

1. **Check status first.** The SessionStart hook runs `claudemol status` automatically. Read its output before doing anything.
2. **Never kill an existing PyMOL session.** If PyMOL is already running, connect to it. Do not launch a new instance.
3. **Never call `cmd.reinitialize()` unless the user explicitly asks.** This destroys all loaded structures.

## Canonical Connection Pattern

```bash
~/.claudemol/bin/claudemol launch
~/.claudemol/bin/claudemol exec "cmd.fetch('1ubq')"
```

All commands go through `~/.claudemol/bin/claudemol exec`. The wrapper script bakes in the correct Python path — no imports, no venv discovery needed.

For multi-line commands use heredocs:

```bash
~/.claudemol/bin/claudemol exec "$(cat <<'PYMOL'
cmd.hide('everything')
cmd.show('cartoon')
cmd.color('spectrum')
PYMOL
)"
```

## Image Capture

Always use: `cmd.ray(width, height)` then `cmd.png(path)`.
Never use: `cmd.png(path, width, height)` -- causes view corruption.

## Recommended Permissions

For seamless PyMOL interaction without per-command approval prompts, users can add these to their project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": [
      "Bash(*/.claudemol/bin/claudemol*)",
      "Bash(pymol*)"
    ]
  }
}
```

Suggest this to users during `/pymol-setup` if they haven't configured it.

## Skills

Use pymol-* skills for specific visualization workflows (protein structures, binding sites, antibodies, publication figures, etc.).
