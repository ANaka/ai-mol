#!/usr/bin/env python3
"""
Visual feedback helper for PyMOL.

Provides a simple way to execute commands and save/view the result.

Usage:
    from pymol_view import pymol_view, execute_and_view

    # Execute commands and save a snapshot
    path = pymol_view("cmd.fetch('1ubq'); cmd.show('cartoon')", name="ubq_cartoon")

    # Or with auto-naming
    path = pymol_view("cmd.color('red', 'all')")
"""

import json
import os
import socket
import time
from datetime import datetime
from pathlib import Path

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 9880
SCRATCH_DIR = Path(__file__).parent / "scratch"


def ensure_scratch_dir():
    """Ensure the scratch directory exists."""
    SCRATCH_DIR.mkdir(exist_ok=True)
    return SCRATCH_DIR


def send_command(code: str, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT, timeout: float = 120.0) -> dict:
    """Send a command to PyMOL and return the result."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        msg = json.dumps({"type": "execute", "code": code})
        s.sendall(msg.encode())

        response = b""
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            response += chunk
            try:
                return json.loads(response.decode())
            except json.JSONDecodeError:
                continue
    finally:
        s.close()
    return {"status": "error", "error": "No response received"}


def generate_filename(name: str | None = None, extension: str = "png") -> Path:
    """Generate a unique filename in the scratch directory."""
    ensure_scratch_dir()

    if name:
        # Clean the name
        clean_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        return SCRATCH_DIR / f"{clean_name}.{extension}"
    else:
        # Auto-generate with timestamp
        timestamp = datetime.now().strftime("%H%M%S")
        return SCRATCH_DIR / f"view_{timestamp}.{extension}"


def pymol_view(
    commands: str,
    name: str | None = None,
    width: int = 800,
    height: int = 600,
    ray: bool = False,
    port: int = DEFAULT_PORT,
) -> str:
    """
    Execute PyMOL commands and save a snapshot.

    Args:
        commands: PyMOL Python commands to execute (e.g., "cmd.fetch('1ubq')")
        name: Optional name for the output file (auto-generated if None)
        width: Image width in pixels
        height: Image height in pixels
        ray: Whether to ray-trace (slower but prettier)
        port: PyMOL socket port

    Returns:
        Path to the saved image file
    """
    output_path = generate_filename(name)

    # Build the full command sequence
    # Note: Using png with explicit dimensions to avoid resizing the GUI window
    full_code = f"""
{commands}

# Save the image with explicit dimensions (doesn't resize window)
{"cmd.ray({}, {})".format(width, height) if ray else ""}
cmd.png(r"{output_path}", {width}, {height})
print(f"Saved: {output_path}")
"""

    result = send_command(full_code, port=port, timeout=120.0)

    if result.get("status") == "success":
        # Wait briefly for file to be written
        time.sleep(0.2)
        if output_path.exists():
            return str(output_path)
        else:
            raise RuntimeError(f"Image was not saved to {output_path}")
    else:
        raise RuntimeError(f"PyMOL error: {result.get('error', 'Unknown error')}")


def quick_view(port: int = DEFAULT_PORT) -> str:
    """
    Take a quick snapshot of the current PyMOL view.

    Returns:
        Path to the saved image
    """
    return pymol_view("pass", name=None, port=port)


def reset_and_view(pdb_id: str, style: str = "cartoon", port: int = DEFAULT_PORT) -> str:
    """
    Clear PyMOL, fetch a structure, and save a view.

    Args:
        pdb_id: PDB ID to fetch (e.g., "1ubq")
        style: Display style (cartoon, surface, sticks, etc.)
        port: PyMOL socket port

    Returns:
        Path to the saved image
    """
    commands = f"""
cmd.reinitialize()
cmd.fetch('{pdb_id}')
cmd.remove('solvent')  # Remove water molecules
cmd.hide('everything')
cmd.show('{style}')
cmd.orient()
cmd.bg_color('white')
"""
    return pymol_view(commands, name=f"{pdb_id}_{style}", port=port)


def binding_site_view(pdb_id: str, port: int = DEFAULT_PORT) -> str:
    """
    Visualize a protein-ligand binding site.

    Args:
        pdb_id: PDB ID with a ligand (e.g., "1hsg")
        port: PyMOL socket port

    Returns:
        Path to the saved image
    """
    commands = f"""
cmd.reinitialize()
cmd.fetch('{pdb_id}')
cmd.remove('solvent')

# Identify components
cmd.select('ligand', 'organic')
cmd.select('protein', 'polymer.protein')
cmd.select('pocket', 'byres (protein within 4 of ligand)')

# Style protein
cmd.show('cartoon', 'protein')
cmd.color('lightblue', 'protein')
cmd.hide('lines')

# Style ligand
cmd.show('sticks', 'ligand')
cmd.util.cbay('ligand')  # Yellow carbons

# Style pocket
cmd.show('sticks', 'pocket')
cmd.color('salmon', 'pocket and elem C')

cmd.zoom('ligand', 8)
cmd.bg_color('white')
"""
    return pymol_view(commands, name=f"{pdb_id}_binding_site", port=port)


def surface_view(pdb_id: str, color_by_charge: bool = False, port: int = DEFAULT_PORT) -> str:
    """
    Visualize a protein surface.

    Args:
        pdb_id: PDB ID to fetch
        color_by_charge: If True, color by residue charge type
        port: PyMOL socket port

    Returns:
        Path to the saved image
    """
    color_commands = ""
    if color_by_charge:
        color_commands = """
cmd.color('blue', 'resn ARG+LYS+HIS')  # Positive
cmd.color('red', 'resn ASP+GLU')       # Negative
cmd.color('white', 'not (resn ARG+LYS+HIS+ASP+GLU)')  # Neutral
"""
    else:
        color_commands = "cmd.color('cyan')"

    commands = f"""
cmd.reinitialize()
cmd.fetch('{pdb_id}')
cmd.remove('resn HOH')
{color_commands}
cmd.hide('everything')
cmd.show('surface')
cmd.rebuild()
cmd.zoom('all', buffer=5)
cmd.bg_color('white')
"""
    suffix = "_charge_surface" if color_by_charge else "_surface"
    return pymol_view(commands, name=f"{pdb_id}{suffix}", ray=True, port=port)


def alignment_view(pdb_id1: str, pdb_id2: str, port: int = DEFAULT_PORT) -> str:
    """
    Align and compare two structures.

    Args:
        pdb_id1: First PDB ID (reference, cyan)
        pdb_id2: Second PDB ID (mobile, magenta)
        port: PyMOL socket port

    Returns:
        Path to the saved image
    """
    commands = f"""
cmd.reinitialize()
cmd.fetch('{pdb_id1}', 'struct1')
cmd.fetch('{pdb_id2}', 'struct2')
cmd.remove('solvent')
cmd.align('struct2', 'struct1')
cmd.color('cyan', 'struct1')
cmd.color('magenta', 'struct2')
cmd.show('cartoon')
cmd.hide('lines')
cmd.orient()
cmd.bg_color('white')
"""
    return pymol_view(commands, name=f"{pdb_id1}_vs_{pdb_id2}", port=port)


def publication_view(pdb_id: str, port: int = DEFAULT_PORT) -> str:
    """
    Create a publication-quality figure with ray tracing.

    Args:
        pdb_id: PDB ID to fetch
        port: PyMOL socket port

    Returns:
        Path to the saved image
    """
    commands = f"""
cmd.reinitialize()
cmd.fetch('{pdb_id}')
cmd.remove('solvent')

# Clean cartoon style
cmd.show('cartoon')
cmd.set('cartoon_fancy_helices', 1)
cmd.set('cartoon_smooth_loops', 1)

# Color by secondary structure
cmd.color('marine', 'ss h')   # helices blue
cmd.color('orange', 'ss s')   # sheets orange
cmd.color('gray70', 'ss l+')  # loops gray

# Nice rendering settings
cmd.bg_color('white')
cmd.set('ray_shadows', 0)
cmd.set('specular', 0.2)
cmd.set('ambient', 0.4)

cmd.orient()
"""
    return pymol_view(commands, name=f"{pdb_id}_publication", width=1200, height=900, ray=True, port=port)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        # Execute command from args
        command = " ".join(sys.argv[1:])
        try:
            path = pymol_view(command)
            print(f"Image saved: {path}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Quick view
        try:
            path = quick_view()
            print(f"Quick view saved: {path}")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
