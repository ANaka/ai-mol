"""
CLI for claudemol setup and management.

Usage:
    claudemol setup    # Configure PyMOL to auto-load the socket plugin
    claudemol status   # Check if PyMOL is running and connected
    claudemol test     # Test the connection
    claudemol info     # Show installation info
    claudemol launch   # Launch PyMOL or connect to existing instance
    claudemol exec     # Execute code in PyMOL
"""

import argparse
import os
import stat
import sys
from pathlib import Path

from claudemol.connection import (
    CONFIG_FILE,
    PyMOLConnection,
    check_pymol_installed,
    connect_or_launch,
    find_pymol_command,
    get_config,
    get_configured_python,
    get_plugin_path,
    save_config,
)

WRAPPER_DIR = Path.home() / ".claudemol" / "bin"
WRAPPER_PATH = WRAPPER_DIR / "claudemol"


def _create_wrapper_script():
    """Create ~/.claudemol/bin/claudemol shell wrapper with baked Python path."""
    WRAPPER_DIR.mkdir(parents=True, exist_ok=True)
    python_path = sys.executable
    script = f"""#!/bin/bash
exec "{python_path}" -m claudemol.cli "$@"
"""
    WRAPPER_PATH.write_text(script)
    WRAPPER_PATH.chmod(
        WRAPPER_PATH.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    )
    return python_path


def setup_pymol():
    """Configure PyMOL to auto-load the socket plugin."""
    plugin_path = get_plugin_path()
    if not plugin_path.exists():
        print(f"Error: Plugin not found at {plugin_path}", file=sys.stderr)
        return 1

    pymolrc_path = Path.home() / ".pymolrc"

    # Check if already configured
    if pymolrc_path.exists():
        content = pymolrc_path.read_text()
        if "claudemol" in content or "claude_socket_plugin" in content:
            print("PyMOL already configured for claudemol.")
            print(f"Plugin: {plugin_path}")
            # Still save config (in case Python path changed)
            save_config({"python_path": sys.executable})
            print(f"Saved Python path: {sys.executable}")
            # Create/update wrapper script
            _create_wrapper_script()
            print(f"Wrapper script: {WRAPPER_PATH}")
            return 0

    # Add to .pymolrc
    run_command = f"\n# claudemol: Claude Code integration\nrun {plugin_path}\n"

    if pymolrc_path.exists():
        with open(pymolrc_path, "a") as f:
            f.write(run_command)
        print(f"Added claudemol plugin to existing {pymolrc_path}")
    else:
        pymolrc_path.write_text(run_command.lstrip())
        print(f"Created {pymolrc_path} with claudemol plugin")

    print(f"Plugin path: {plugin_path}")
    print("\nSetup complete! The plugin will auto-load when you start PyMOL.")

    # Check if PyMOL is installed
    if not check_pymol_installed():
        print("\nNote: PyMOL not found in PATH.")
        print("Install PyMOL with one of:")
        print("  - pip install pymol-open-source-whl")
        print("  - brew install pymol (macOS)")
        print("  - Download from https://pymol.org")

    # Save Python path for SessionStart hook and skills
    save_config({"python_path": sys.executable})
    print(f"Saved Python path: {sys.executable}")

    # Create wrapper script
    _create_wrapper_script()
    print(f"Wrapper script: {WRAPPER_PATH}")

    return 0


def check_status():
    """Check PyMOL connection status."""
    print("Checking PyMOL status...")

    # Show configured Python if available
    configured_python = get_configured_python()
    if configured_python:
        print(f"Configured Python: {configured_python}")

    # Check if PyMOL is installed
    pymol_cmd = find_pymol_command()
    if pymol_cmd:
        print(f"PyMOL found: {' '.join(pymol_cmd)}")
    else:
        print("PyMOL not found in PATH")
        return 1

    # Try to connect
    conn = PyMOLConnection()
    try:
        conn.connect(timeout=2.0)
        print("Socket connection: OK (port 9880)")
        conn.disconnect()
        return 0
    except ConnectionError:
        print("Socket connection: Not available")
        print("  (PyMOL may not be running, or plugin not loaded)")
        return 1


def test_connection():
    """Test the PyMOL connection with a simple command."""
    conn = PyMOLConnection()
    try:
        conn.connect(timeout=2.0)
        result = conn.execute("print('claudemol connection test')")
        print("Connection test: OK")
        print(f"Response: {result}")
        conn.disconnect()
        return 0
    except ConnectionError as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        print("\nMake sure PyMOL is running with the socket plugin.")
        print("Start PyMOL and run: claude_status")
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def show_info():
    """Show claudemol installation info."""
    plugin_path = get_plugin_path()
    pymolrc_path = Path.home() / ".pymolrc"

    print("claudemol installation info:")
    print(f"  Plugin: {plugin_path}")
    print(f"  Plugin exists: {plugin_path.exists()}")
    print(f"  .pymolrc: {pymolrc_path}")
    print(f"  .pymolrc exists: {pymolrc_path.exists()}")

    if pymolrc_path.exists():
        content = pymolrc_path.read_text()
        configured = "claudemol" in content or "claude_socket_plugin" in content
        print(f"  Configured in .pymolrc: {configured}")

    pymol_cmd = find_pymol_command()
    print(f"  PyMOL command: {' '.join(pymol_cmd) if pymol_cmd else 'not found'}")

    print(f"  Config file: {CONFIG_FILE}")
    config = get_config()
    if config:
        for key, value in config.items():
            print(f"  Config {key}: {value}")
    else:
        print("  Config: not set (run 'claudemol setup' to configure)")

    print(f"  Wrapper script: {WRAPPER_PATH}")
    print(f"  Wrapper exists: {WRAPPER_PATH.exists()}")


def do_launch(args):
    """Launch PyMOL or connect to existing instance."""
    file_path = getattr(args, "file", None)
    try:
        conn, process = connect_or_launch(file_path=file_path)
        if process:
            print(f"Launched PyMOL (pid {process.pid})")
        else:
            print("Connected to existing PyMOL instance")
        conn.disconnect()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


def do_exec(args):
    """Execute code in PyMOL."""
    code = getattr(args, "code", None)

    # Read from positional arg or stdin
    if code:
        code = code
    elif not os.isatty(sys.stdin.fileno()):
        code = sys.stdin.read()
    else:
        print(
            "Error: No code provided. Pass as argument or pipe via stdin.",
            file=sys.stderr,
        )
        print("  claudemol exec \"cmd.fetch('1ubq')\"", file=sys.stderr)
        print("  echo \"cmd.fetch('1ubq')\" | claudemol exec", file=sys.stderr)
        return 1

    if not code.strip():
        print("Error: Empty code.", file=sys.stderr)
        return 1

    conn = PyMOLConnection()
    try:
        conn.connect(timeout=2.0)
    except ConnectionError:
        print("Error: Cannot connect to PyMOL. Is it running?", file=sys.stderr)
        print("  Run: claudemol launch", file=sys.stderr)
        return 1

    try:
        result = conn.execute(code)
        if result:
            print(result, end="" if result.endswith("\n") else "\n")
        conn.disconnect()
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        conn.disconnect()
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="claudemol: PyMOL integration for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(dest="command")

    # setup
    subparsers.add_parser(
        "setup", help="Configure PyMOL to auto-load the socket plugin"
    )

    # status
    subparsers.add_parser("status", help="Check if PyMOL is running and connected")

    # test
    subparsers.add_parser("test", help="Test the connection with a simple command")

    # info
    subparsers.add_parser("info", help="Show installation info")

    # launch
    launch_parser = subparsers.add_parser(
        "launch", help="Launch PyMOL or connect to existing instance"
    )
    launch_parser.add_argument(
        "file", nargs="?", default=None, help="File to open (e.g., .pdb, .cif)"
    )

    # exec
    exec_parser = subparsers.add_parser("exec", help="Execute code in PyMOL")
    exec_parser.add_argument(
        "code",
        nargs="?",
        default=None,
        help="Python code to execute (or pipe via stdin)",
    )

    args = parser.parse_args()

    if args.command is None:
        show_info()
        return 0
    elif args.command == "setup":
        return setup_pymol()
    elif args.command == "status":
        return check_status()
    elif args.command == "test":
        return test_connection()
    elif args.command == "info":
        show_info()
        return 0
    elif args.command == "launch":
        return do_launch(args)
    elif args.command == "exec":
        return do_exec(args)


if __name__ == "__main__":
    sys.exit(main())
