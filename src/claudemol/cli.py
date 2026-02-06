"""
CLI for claudemol setup and management.

Usage:
    claudemol setup    # Configure PyMOL to auto-load the socket plugin
    claudemol status   # Check if PyMOL is running and connected
    claudemol test     # Test the connection
"""

import argparse
import sys
from pathlib import Path

from claudemol.connection import (
    CONFIG_FILE,
    PyMOLConnection,
    check_pymol_installed,
    find_pymol_command,
    get_config,
    get_configured_python,
    get_plugin_path,
    save_config,
)


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


def main():
    parser = argparse.ArgumentParser(
        description="claudemol: PyMOL integration for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  setup     Configure PyMOL to auto-load the socket plugin
  status    Check if PyMOL is running and connected
  test      Test the connection with a simple command
  info      Show installation info

For Claude Code skills, install the claudemol-skills plugin:
  /plugin marketplace add ANaka/claudemol?path=claude-plugin
  /plugin install claudemol-skills
""",
    )
    parser.add_argument(
        "command",
        nargs="?",
        choices=["setup", "status", "test", "info"],
        default="info",
        help="Command to run",
    )

    args = parser.parse_args()

    if args.command == "setup":
        return setup_pymol()
    elif args.command == "status":
        return check_status()
    elif args.command == "test":
        return test_connection()
    elif args.command == "info":
        show_info()
        return 0


if __name__ == "__main__":
    sys.exit(main())
