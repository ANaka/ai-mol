# claudemol - PyMOL Integration

claudemol connects Claude to a running PyMOL instance over TCP socket (localhost:9880).

## Connection Rules

1. **Check status first.** The SessionStart hook runs `claudemol status` automatically. Read its output before doing anything.
2. **Never kill an existing PyMOL session.** If PyMOL is already running, connect to it. Do not launch a new instance.
3. **Never call `cmd.reinitialize()` unless the user explicitly asks.** This destroys all loaded structures.
4. **Use `PyMOLConnection`, not `PyMOLSession`.** PyMOLSession's auto-recovery is too aggressive and kills existing sessions.

## Canonical Connection Pattern

```python
from claudemol import PyMOLConnection
conn = PyMOLConnection()
conn.connect()
conn.execute("fetch 1ubq")
```

Reuse the `conn` object across commands. If connection drops, `conn.execute()` auto-reconnects (3 attempts).

If PyMOL is not running: tell the user, or use `from claudemol import launch_pymol; launch_pymol()`.

## Image Capture

Always use: `cmd.ray(width, height)` then `cmd.png(path)`.
Never use: `cmd.png(path, width, height)` — causes view corruption.

## Skills

Use pymol-* skills for specific visualization workflows (protein structures, binding sites, antibodies, publication figures, etc.).
