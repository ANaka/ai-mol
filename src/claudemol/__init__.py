"""
claudemol: PyMOL integration for Claude Code

Connect to PyMOL via socket for AI-assisted molecular visualization.
"""

from claudemol.connection import (
    PyMOLConnection,
    check_pymol_installed,
    connect_or_launch,
    find_pymol_command,
    get_config,
    get_configured_python,
    launch_pymol,
    save_config,
)
from claudemol.session import (
    PyMOLSession,
    ensure_running,
    get_session,
    stop_pymol,
)

__version__ = "0.4.1"
__all__ = [
    "PyMOLConnection",
    "PyMOLSession",
    "connect_or_launch",
    "launch_pymol",
    "find_pymol_command",
    "check_pymol_installed",
    "get_config",
    "save_config",
    "get_configured_python",
    "get_session",
    "ensure_running",
    "stop_pymol",
]
