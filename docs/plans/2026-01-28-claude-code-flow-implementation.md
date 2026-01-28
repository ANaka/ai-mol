# Claude Code Flow Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace Claude Desktop + MCP architecture with direct socket communication from Claude Code to PyMOL.

**Architecture:** Claude Code sends PyMOL Python commands over TCP socket (port 9876) to a headless plugin in PyMOL. No MCP server, no Qt UI. Skills provide PyMOL knowledge. A `/pymol-setup` skill handles first-time configuration.

**Tech Stack:** Python 3, TCP sockets, PyMOL API, Claude Code skills

---

## Task 1: Create Headless Socket Plugin

**Files:**
- Create: `claude_socket_plugin.py` (new standalone plugin, replaces `pymol-mcp-socket-plugin/__init__.py`)

**Step 1: Write the plugin file**

Create `claude_socket_plugin.py` at the project root. This is a headless socket listener that auto-starts when loaded into PyMOL.

```python
"""
Claude Socket Plugin for PyMOL

Headless socket listener that receives Python commands from Claude Code.
Auto-starts on load, no UI required.

Usage:
    run /path/to/claude_socket_plugin.py    # Start listening
    claude_status                            # Check connection status
    claude_stop                              # Stop listener
    claude_start                             # Restart listener
"""

import socket
import json
import threading
import traceback
import io
from contextlib import redirect_stdout

from pymol import cmd

# Global state
_server = None
_port = 9876


class SocketServer:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.socket = None
        self.client = None
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return False
        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        return True

    def _run_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.socket.settimeout(1.0)

            print(f"Claude socket listener active on port {self.port}")

            while self.running:
                try:
                    new_client, address = self.socket.accept()
                    if self.client:
                        try:
                            self.client.close()
                        except:
                            pass
                    self.client = new_client
                    self.client.settimeout(1.0)
                    self._handle_client(address)
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        print(f"Connection error: {e}")
        except Exception as e:
            print(f"Socket server error: {e}")
            traceback.print_exc()
        finally:
            self._cleanup()

    def _handle_client(self, address):
        buffer = b''
        while self.running and self.client:
            try:
                data = self.client.recv(4096)
                if not data:
                    break
                buffer += data
                try:
                    command = json.loads(buffer.decode('utf-8'))
                    buffer = b''
                    result = self._execute_command(command)
                    response = json.dumps(result)
                    self.client.sendall(response.encode('utf-8'))
                except json.JSONDecodeError:
                    continue
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Client error: {e}")
                break
        if self.client:
            try:
                self.client.close()
            except:
                pass
            self.client = None

    def _execute_command(self, command):
        code = command.get("code", "")
        if not code:
            return {"status": "error", "error": "No code provided"}
        try:
            exec_globals = {"cmd": cmd, "__builtins__": __builtins__}
            output_buffer = io.StringIO()
            with redirect_stdout(output_buffer):
                exec(code, exec_globals)
            output = output_buffer.getvalue()
            if '_result' in exec_globals:
                output = str(exec_globals['_result'])
            return {"status": "success", "output": output or "OK"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _cleanup(self):
        if self.client:
            try:
                self.client.close()
            except:
                pass
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        self.socket = None
        self.client = None
        self.running = False

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(2.0)
        self._cleanup()

    @property
    def is_running(self):
        return self.running and self.thread and self.thread.is_alive()


def claude_status():
    """Print Claude socket listener status."""
    global _server
    if _server and _server.is_running:
        connected = "connected" if _server.client else "waiting"
        print(f"Claude socket listener: running on port {_port} ({connected})")
    else:
        print("Claude socket listener: not running")


def claude_stop():
    """Stop the Claude socket listener."""
    global _server
    if _server:
        _server.stop()
        _server = None
        print("Claude socket listener stopped")
    else:
        print("Claude socket listener was not running")


def claude_start(port=9876):
    """Start the Claude socket listener."""
    global _server, _port
    if _server and _server.is_running:
        print(f"Claude socket listener already running on port {_port}")
        return
    _port = port
    _server = SocketServer(port=port)
    _server.start()


# Register commands with PyMOL
cmd.extend("claude_status", claude_status)
cmd.extend("claude_stop", claude_stop)
cmd.extend("claude_start", claude_start)

# Auto-start on load
claude_start()
```

**Step 2: Test plugin manually**

Launch PyMOL and run:
```
run /path/to/pymol-mcp/claude_socket_plugin.py
```

Expected: See message `Claude socket listener active on port 9876`

Test commands:
```
claude_status
claude_stop
claude_start
```

**Step 3: Commit**

```bash
git add claude_socket_plugin.py
git commit -m "feat: add headless Claude socket plugin

Replaces Qt-based plugin with headless socket listener.
- Auto-starts on load
- No UI dependencies
- Exposes claude_status, claude_stop, claude_start commands"
```

---

## Task 2: Create PyMOL Connection Module

**Files:**
- Create: `pymol_connection.py`

**Step 1: Write the connection module**

This module provides functions for Claude Code to communicate with PyMOL.

```python
"""
PyMOL Connection Module

Provides functions for Claude Code to communicate with PyMOL via socket.
"""

import socket
import json
import subprocess
import time
import shutil
from pathlib import Path

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9876
CONNECT_TIMEOUT = 5.0
RECV_TIMEOUT = 30.0


class PyMOLConnection:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self, timeout=CONNECT_TIMEOUT):
        """Connect to PyMOL socket server."""
        if self.socket:
            return True
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(RECV_TIMEOUT)
            return True
        except Exception as e:
            self.socket = None
            raise ConnectionError(f"Cannot connect to PyMOL on {self.host}:{self.port}: {e}")

    def disconnect(self):
        """Disconnect from PyMOL."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

    def is_connected(self):
        """Check if connected to PyMOL."""
        if not self.socket:
            return False
        try:
            self.socket.setblocking(False)
            try:
                data = self.socket.recv(1, socket.MSG_PEEK)
                if data == b'':
                    self.disconnect()
                    return False
            except BlockingIOError:
                pass
            finally:
                self.socket.setblocking(True)
                self.socket.settimeout(RECV_TIMEOUT)
            return True
        except:
            self.disconnect()
            return False

    def send_command(self, code):
        """Send Python code to PyMOL and return result."""
        if not self.socket:
            raise ConnectionError("Not connected to PyMOL")
        try:
            message = json.dumps({"type": "execute", "code": code})
            self.socket.sendall(message.encode('utf-8'))
            response = b''
            while True:
                chunk = self.socket.recv(4096)
                if not chunk:
                    raise ConnectionError("Connection closed by PyMOL")
                response += chunk
                try:
                    result = json.loads(response.decode('utf-8'))
                    return result
                except json.JSONDecodeError:
                    continue
        except socket.timeout:
            raise TimeoutError("PyMOL command timed out")
        except Exception as e:
            self.disconnect()
            raise ConnectionError(f"Communication error: {e}")

    def execute(self, code):
        """Execute code, reconnecting if necessary. Returns output string or raises."""
        for attempt in range(3):
            try:
                if not self.is_connected():
                    self.connect()
                result = self.send_command(code)
                if result.get("status") == "success":
                    return result.get("output", "")
                else:
                    raise RuntimeError(result.get("error", "Unknown error"))
            except ConnectionError:
                if attempt < 2:
                    time.sleep(0.5)
                    continue
                raise
        raise ConnectionError("Failed to connect after 3 attempts")


def check_pymol_installed():
    """Check if pymol command is available."""
    return shutil.which("pymol") is not None


def launch_pymol(file_path=None, wait_for_socket=True, timeout=10.0):
    """
    Launch PyMOL with the Claude socket plugin.

    Args:
        file_path: Optional file to open (e.g., .pdb, .cif)
        wait_for_socket: Wait for socket to become available
        timeout: How long to wait for socket

    Returns:
        subprocess.Popen process handle
    """
    if not check_pymol_installed():
        raise RuntimeError("PyMOL not found. Please install PyMOL and ensure 'pymol' is in your PATH.")

    plugin_path = Path(__file__).parent / "claude_socket_plugin.py"
    if not plugin_path.exists():
        raise RuntimeError(f"Plugin not found: {plugin_path}")

    cmd_args = ["pymol"]
    if file_path:
        cmd_args.append(str(file_path))
    cmd_args.extend(["-d", f"run {plugin_path}"])

    process = subprocess.Popen(cmd_args)

    if wait_for_socket:
        start = time.time()
        while time.time() - start < timeout:
            try:
                conn = PyMOLConnection()
                conn.connect(timeout=1.0)
                conn.disconnect()
                return process
            except:
                time.sleep(0.5)
        raise TimeoutError(f"PyMOL socket not available after {timeout}s")

    return process


def connect_or_launch(file_path=None):
    """
    Connect to existing PyMOL or launch new instance.

    Returns:
        (PyMOLConnection, process_or_None)
    """
    conn = PyMOLConnection()

    # Try connecting to existing instance
    try:
        conn.connect(timeout=1.0)
        return conn, None
    except ConnectionError:
        pass

    # Launch new instance
    process = launch_pymol(file_path=file_path)
    conn.connect()
    return conn, process
```

**Step 2: Test connection module**

With PyMOL running (and plugin loaded), test from Python:

```python
from pymol_connection import PyMOLConnection

conn = PyMOLConnection()
conn.connect()
result = conn.execute("print('Hello from Claude!')")
print(result)
conn.disconnect()
```

**Step 3: Commit**

```bash
git add pymol_connection.py
git commit -m "feat: add PyMOL connection module

Provides Python interface for Claude Code to communicate with PyMOL:
- PyMOLConnection class with auto-reconnect
- launch_pymol() to spawn PyMOL with plugin
- connect_or_launch() for seamless session management"
```

---

## Task 3: Create pymol-setup Skill

**Files:**
- Create: `.claude/skills/pymol-setup/SKILL.md`

**Step 1: Write the skill**

```markdown
---
name: pymol-setup
description: Use when connecting Claude to PyMOL, troubleshooting socket errors, or setting up the PyMOL integration for the first time
---

# PyMOL Setup

Set up Claude Code to work with PyMOL.

## What This Does

1. Verifies PyMOL is installed
2. Configures pymolrc to auto-load the socket plugin
3. Tests the connection

## Steps

### 1. Check PyMOL Installation

Run this command to verify PyMOL is available:

```bash
which pymol && pymol --version
```

If not found, tell the user to install PyMOL first.

### 2. Find pymolrc Location

PyMOL looks for startup scripts in these locations (in order):
- `~/.pymolrc.py` (Python script)
- `~/.pymolrc` (PyMOL commands)

Check if either exists:

```bash
ls -la ~/.pymolrc.py ~/.pymolrc 2>/dev/null || echo "No pymolrc found"
```

### 3. Configure Auto-Load

Add the plugin to pymolrc. The plugin path is:
`<repo-root>/claude_socket_plugin.py`

If `~/.pymolrc.py` exists, add this line:
```python
import subprocess; subprocess.Popen(['python', '-c', 'pass'])  # dummy to avoid import issues
run /path/to/pymol-mcp/claude_socket_plugin.py
```

If no pymolrc exists, create `~/.pymolrc` with:
```
run /path/to/pymol-mcp/claude_socket_plugin.py
```

Use the actual absolute path to the plugin.

### 4. Test Connection

Launch PyMOL and verify connection:

```bash
pymol &
sleep 3
```

Then use the connection module to test:

```python
from pymol_connection import PyMOLConnection
conn = PyMOLConnection()
conn.connect()
result = conn.execute("print('Setup successful!')")
print(result)
```

### 5. Report Success

Tell the user:
- Setup complete
- PyMOL will auto-connect when launched
- They can say "open PyMOL" or "load <file>" to start working

## Troubleshooting

**"Connection refused"**: PyMOL isn't running or plugin didn't load. Check:
- Is PyMOL running?
- Run `claude_status` in PyMOL console
- Check for errors in PyMOL console

**"pymol: command not found"**: PyMOL not in PATH. User needs to:
- Install PyMOL, or
- Add PyMOL to PATH, or
- Create alias in shell config
```

**Step 2: Commit**

```bash
git add .claude/skills/pymol-setup/SKILL.md
git commit -m "feat: add pymol-setup skill

Guides first-time setup:
- Verify PyMOL installation
- Configure pymolrc for auto-load
- Test connection"
```

---

## Task 4: Create pymol-connect Skill

**Files:**
- Create: `.claude/skills/pymol-connect/SKILL.md`

**Step 1: Write the skill**

```markdown
---
name: pymol-connect
description: Use when launching PyMOL or connecting to an existing PyMOL session for molecular visualization work
---

# PyMOL Connect

Connect to PyMOL for molecular visualization work.

## Quick Start

When user wants to work with PyMOL (e.g., "open PyMOL", "load 1abc.pdb", "show me this structure"):

### 1. Try Connecting to Existing Instance

```python
import sys
sys.path.insert(0, '/path/to/pymol-mcp')  # Use actual repo path
from pymol_connection import PyMOLConnection

conn = PyMOLConnection()
try:
    conn.connect(timeout=1.0)
    print("Connected to existing PyMOL session")
except:
    print("No existing PyMOL session")
```

### 2. Launch PyMOL if Needed

```python
from pymol_connection import launch_pymol, PyMOLConnection

process = launch_pymol()  # or launch_pymol("file.pdb")
conn = PyMOLConnection()
conn.connect()
print("PyMOL launched and connected")
```

### 3. Send Commands

```python
# Simple command
conn.execute("fetch 1abc")

# Multiple commands
conn.execute("""
fetch 1abc
hide everything
show cartoon
color spectrum, chain A
""")

# Get information back
result = conn.execute("""
_result = cmd.get_names()
""")
print(result)  # List of object names
```

## Session Management

**Check connection:**
```python
if conn.is_connected():
    # Good to go
else:
    conn.connect()  # Will auto-reconnect
```

**Connection drops:** The connection module auto-reconnects on failure (up to 3 attempts).

**Close session:** Just close PyMOL normally. No special handling needed.

## Common Patterns

**Load structure from PDB:**
```python
conn.execute("fetch 4HHB")
```

**Load local file:**
```python
conn.execute("load /path/to/structure.pdb")
```

**Basic visualization:**
```python
conn.execute("""
hide everything
show cartoon
color spectrum
orient
""")
```

**Save image:**
```python
conn.execute("""
ray 1920, 1080
png /path/to/output.png
""")
```

## Refer to Other Skills

For specific visualization tasks, use:
- @pymol-fundamentals - selections, representations, colors
- @binding-site-visualization - ligand binding sites
- @publication-figures - high-quality figures
- @structure-alignment-analysis - comparing structures
```

**Step 2: Commit**

```bash
git add .claude/skills/pymol-connect/SKILL.md
git commit -m "feat: add pymol-connect skill

Guides Claude through connecting to PyMOL:
- Connect to existing or launch new
- Send commands
- Common patterns"
```

---

## Task 5: Update pymol-mcp-connection Skill

**Files:**
- Delete or update: `.claude/skills/pymol-mcp-connection/` (currently empty)

**Step 1: Remove empty directory**

```bash
rmdir .claude/skills/pymol-mcp-connection
```

**Step 2: Commit**

```bash
git add -A
git commit -m "chore: remove empty pymol-mcp-connection skill directory"
```

---

## Task 6: Integration Test

**Files:**
- None (manual testing)

**Step 1: Full workflow test**

1. Ensure pymolrc is configured (run setup if not)
2. Close any running PyMOL
3. From Claude Code, test the full flow:

```python
import sys
sys.path.insert(0, '/Users/alex/code/pymol-mcp')
from pymol_connection import connect_or_launch

# Should launch PyMOL and connect
conn, process = connect_or_launch()

# Test commands
print(conn.execute("print('Hello!')"))
print(conn.execute("fetch 1ubq"))
print(conn.execute("""
hide everything
show cartoon
color spectrum
orient
"""))

# Check status in PyMOL console: should see the commands executed
```

**Step 2: Test reconnection**

1. With PyMOL open from above
2. Quit PyMOL
3. Try to execute a command - should fail gracefully
4. Relaunch and reconnect

**Step 3: Document any issues**

If issues found, fix before final commit.

---

## Task 7: Update CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

**Step 1: Add Claude Code workflow section**

Add to CLAUDE.md:

```markdown
## Claude Code Workflow

This project supports direct communication from Claude Code to PyMOL (no MCP server needed).

**First-time setup:** Run `/pymol-setup` or ask Claude to set up PyMOL.

**Starting a session:** Say "open PyMOL" or "load <structure>". Claude will launch PyMOL if needed.

**Architecture:**
```
Claude Code → TCP Socket (9876) → PyMOL Plugin
```

**Key files:**
- `claude_socket_plugin.py` - Headless PyMOL plugin (auto-loads via pymolrc)
- `pymol_connection.py` - Python module for socket communication

**PyMOL commands (run in PyMOL console):**
- `claude_status` - Check if listener is running
- `claude_stop` - Stop listener
- `claude_start` - Start listener
```

**Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: add Claude Code workflow to CLAUDE.md"
```

---

## Summary

After completing all tasks:

1. **New files:**
   - `claude_socket_plugin.py` - Headless PyMOL plugin
   - `pymol_connection.py` - Connection module for Claude Code
   - `.claude/skills/pymol-setup/SKILL.md` - Setup skill
   - `.claude/skills/pymol-connect/SKILL.md` - Connection skill

2. **Modified files:**
   - `CLAUDE.md` - Updated with new workflow

3. **Removed:**
   - Empty `.claude/skills/pymol-mcp-connection/` directory

4. **Unchanged (can be removed later):**
   - `pymol-mcp-socket-plugin/` - Old Qt-based plugin
   - `pymol_mcp_server.py` - Old MCP server
