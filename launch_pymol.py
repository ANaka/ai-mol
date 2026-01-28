#!/usr/bin/env python
"""Launch PyMOL and establish Claude connection."""

from pymol_connection import connect_or_launch

conn, process = connect_or_launch()
if process:
    print("Launched new PyMOL session")
else:
    print("Connected to existing PyMOL session")

result = conn.execute("print('Claude connected!')")
print(f"PyMOL ready: {result}")
