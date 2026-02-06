"""
PyMOL Connection Module

Provides functions for Claude Code to communicate with PyMOL via socket.
"""

import json
import os
import shutil
import socket
import subprocess
import time
from pathlib import Path

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9880
CONNECT_TIMEOUT = 5.0
RECV_TIMEOUT = 30.0

CONFIG_DIR = Path.home() / ".claudemol"
CONFIG_FILE = CONFIG_DIR / "config.json"

# Common PyMOL installation paths
PYMOL_PATHS = [
    # uv environment (created by /pymol-setup)
    os.path.expanduser("~/.pymol-env/bin/python"),
    # macOS app locations
    "/Applications/PyMOL.app/Contents/MacOS/PyMOL",
    os.path.expanduser("~/Applications/PyMOL.app/Contents/MacOS/PyMOL"),
    # Linux system locations
    "/usr/bin/pymol",
    "/usr/local/bin/pymol",
]


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
            raise ConnectionError(
                f"Cannot connect to PyMOL on {self.host}:{self.port}: {e}"
            )

    def disconnect(self):
        """Disconnect from PyMOL."""
        if self.socket:
            try:
                self.socket.close()
            except OSError:
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
                if data == b"":
                    self.disconnect()
                    return False
            except BlockingIOError:
                pass
            finally:
                self.socket.setblocking(True)
                self.socket.settimeout(RECV_TIMEOUT)
            return True
        except OSError:
            self.disconnect()
            return False

    def send_command(self, code):
        """Send Python code to PyMOL and return result."""
        if not self.socket:
            raise ConnectionError("Not connected to PyMOL")
        try:
            message = json.dumps({"type": "execute", "code": code})
            self.socket.sendall(message.encode("utf-8"))
            response = b""
            while True:
                chunk = self.socket.recv(4096)
                if not chunk:
                    raise ConnectionError("Connection closed by PyMOL")
                response += chunk
                try:
                    result = json.loads(response.decode("utf-8"))
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


def find_pymol_command():
    """
    Find how to launch PyMOL.

    Returns:
        List of command arguments (e.g., ["pymol"] or ["python", "-m", "pymol"])
        or None if PyMOL is not found.
    """
    # Check if pymol is in PATH
    pymol_path = shutil.which("pymol")
    if pymol_path:
        return [pymol_path]

    # Check uv environment first (most common for this project)
    uv_python = os.path.expanduser("~/.pymol-env/bin/python")
    if os.path.isfile(uv_python) and os.access(uv_python, os.X_OK):
        # Verify pymol is installed in this environment
        try:
            result = subprocess.run(
                [uv_python, "-c", "import pymol"],
                capture_output=True,
                timeout=5,
            )
            if result.returncode == 0:
                return [uv_python, "-m", "pymol"]
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

    # Check other common paths
    for path in PYMOL_PATHS:
        if path.endswith("/python"):
            continue  # Already checked uv environment above
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return [path]

    return None


def find_pymol_executable():
    """Find PyMOL executable path (legacy compatibility)."""
    cmd = find_pymol_command()
    return cmd[0] if cmd else None


def check_pymol_installed():
    """Check if pymol command is available."""
    return find_pymol_command() is not None


def get_plugin_path():
    """Get the path to the socket plugin file."""
    return Path(__file__).parent / "plugin.py"


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
    pymol_cmd = find_pymol_command()
    if not pymol_cmd:
        raise RuntimeError(
            "PyMOL not found. Please install PyMOL:\n"
            "  - Run: claudemol setup\n"
            "  - Or: pip install pymol-open-source-whl\n"
            "  - Or: brew install pymol (macOS)"
        )

    plugin_path = get_plugin_path()
    if not plugin_path.exists():
        raise RuntimeError(f"Plugin not found: {plugin_path}")

    # Build command: base pymol command + optional file + plugin
    cmd_args = list(pymol_cmd)
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
            except ConnectionError:
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


def get_config():
    """Read persisted claudemol config."""
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_config(config):
    """Save claudemol config."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n")


def get_configured_python():
    """Get the Python path from persisted config. Returns path string or None."""
    config = get_config()
    python_path = config.get("python_path")
    if python_path and os.path.isfile(python_path) and os.access(python_path, os.X_OK):
        return python_path
    return None
