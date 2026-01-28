#!/usr/bin/env python3
"""
Send commands to PyMOL via socket.

Usage:
    python pymol_cmd.py "cmd.fetch('1ubq')"
    python pymol_cmd.py "cmd.show('cartoon')"
    echo "cmd.color('red', 'all')" | python pymol_cmd.py -
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from pymol_connection import PyMOLConnection


def main():
    if len(sys.argv) < 2:
        print("Usage: python pymol_cmd.py <command>", file=sys.stderr)
        print("       python pymol_cmd.py -  (read from stdin)", file=sys.stderr)
        sys.exit(1)

    # Get command from args or stdin
    if sys.argv[1] == "-":
        code = sys.stdin.read().strip()
    else:
        code = " ".join(sys.argv[1:])

    if not code:
        print("No command provided", file=sys.stderr)
        sys.exit(1)

    try:
        conn = PyMOLConnection()
        conn.connect(timeout=2.0)
        result = conn.execute(code)
        if result and result != "OK":
            print(result)
    except ConnectionError as e:
        print(f"Connection error: {e}", file=sys.stderr)
        print("Is PyMOL running with the socket plugin?", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"PyMOL error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
