---
name: movie-creation
description: Use when creating movies, animations, rotations, or morphing sequences in PyMOL through MCP.
version: 0.1.0
---

# Movie Creation

Workflows for creating animations and movies in PyMOL.

## Movie Basics

### Set Frame Count

```python
cmd.mset("1 x360")  # 360 frames (one state repeated)
cmd.mset("1 x90")   # 90 frames
cmd.mset("")        # Clear movie
```

### Frame Navigation

```python
cmd.frame(1)        # Go to frame 1
cmd.frame(45)       # Go to frame 45
cmd.forward()       # Next frame
cmd.backward()      # Previous frame
```

### Playback Control

```python
cmd.mplay()         # Start playback
cmd.mstop()         # Stop playback
cmd.rewind()        # Go to first frame
```

## Simple Rotation Movie

### Using mroll

```python
# Full 360-degree rotation around Y axis
cmd.mset("1 x360")
cmd.util.mroll(1, 360, 1)  # start_frame, end_frame, axis (1=Y)
```

### Axis Options for mroll

- `1` = Y axis (horizontal rotation)
- `2` = X axis (vertical rotation)
- `3` = Z axis (in-plane rotation)

## Scene-Based Movies

### Store Scenes

```python
cmd.orient()
cmd.scene("overview", "store")

cmd.zoom("ligand", 5)
cmd.scene("closeup", "store")

cmd.zoom("resi 100-120")
cmd.scene("domain", "store")
```

### Create Movie from Scenes

```python
# Set total frames
cmd.mset("1 x90")

# Store keyframes
cmd.frame(1)
cmd.scene("overview", "recall")
cmd.mview("store")

cmd.frame(30)
cmd.scene("closeup", "recall")
cmd.mview("store")

cmd.frame(60)
cmd.scene("domain", "recall")
cmd.mview("store")

cmd.frame(90)
cmd.scene("overview", "recall")
cmd.mview("store")

# Interpolate between keyframes
cmd.mview("interpolate")
```

## Camera Movement

### Store View Keyframes

```python
cmd.mset("1 x60")

# Starting view
cmd.frame(1)
cmd.orient()
cmd.mview("store")

# Rotated view
cmd.frame(30)
cmd.turn("y", 90)
cmd.mview("store")

# Zoomed view
cmd.frame(60)
cmd.zoom("resi 50", 5)
cmd.mview("store")

# Smooth interpolation
cmd.mview("interpolate")
```

### Interpolation Modes

```python
cmd.mview("interpolate")           # Linear interpolation
cmd.mview("interpolate", power=1)  # Linear
cmd.mview("interpolate", power=2)  # Smooth (ease in/out)
```

## Multi-State Movies

### For NMR Ensembles or MD Trajectories

```python
# If structure has multiple states
cmd.mset("1 -%d" % cmd.count_states())  # All states
cmd.mplay()
```

### Loop Through States

```python
n_states = cmd.count_states()
cmd.mset("1 x" + str(n_states))
# Each frame shows corresponding state
```

## Exporting Movies

### PNG Sequence

```python
import os
output_dir = os.path.expanduser("~/Desktop/movie_frames")
os.makedirs(output_dir, exist_ok=True)

cmd.mpng(output_dir + "/frame")
# Creates frame0001.png, frame0002.png, etc.
```

### With Ray Tracing (Slow but High Quality)

```python
cmd.set("ray_trace_frames", 1)
cmd.mpng(output_dir + "/frame")
cmd.set("ray_trace_frames", 0)
```

### Convert to Video (External)

After exporting PNG sequence, use ffmpeg:
```bash
ffmpeg -framerate 30 -i frame%04d.png -c:v libx264 -pix_fmt yuv420p movie.mp4
```

## Complete Workflows

### 360-Degree Rotation

```python
from pymol import cmd

# Setup
cmd.delete("all")
cmd.fetch("1ubq")
cmd.show("cartoon")
cmd.hide("lines")
cmd.color("green")
cmd.bg_color("white")

# Create rotation movie
cmd.mset("1 x360")
cmd.util.mroll(1, 360, 1)

# Export (optional)
# cmd.mpng("~/Desktop/rotation/frame")
```

### Zoom In/Out Animation

```python
from pymol import cmd

# Setup structure
cmd.orient()
cmd.mset("1 x60")

# Full view
cmd.frame(1)
cmd.zoom("all", 5)
cmd.mview("store")

# Close-up
cmd.frame(30)
cmd.zoom("resi 45-50", 3)
cmd.mview("store")

# Back to full
cmd.frame(60)
cmd.zoom("all", 5)
cmd.mview("store")

# Smooth transition
cmd.mview("interpolate", power=2)
```

### Tour of Binding Site

```python
from pymol import cmd

# Assume structure with ligand loaded
cmd.select("lig", "organic")
cmd.select("pocket", "byres (polymer.protein within 5 of lig)")

# Store views
cmd.zoom("all")
cmd.scene("full", "store")

cmd.zoom("lig", 8)
cmd.scene("ligand", "store")

cmd.zoom("pocket", 5)
cmd.turn("y", 45)
cmd.scene("pocket_side", "store")

# Create movie
cmd.mset("1 x120")

cmd.frame(1)
cmd.scene("full", "recall")
cmd.mview("store")

cmd.frame(40)
cmd.scene("ligand", "recall")
cmd.mview("store")

cmd.frame(80)
cmd.scene("pocket_side", "recall")
cmd.mview("store")

cmd.frame(120)
cmd.scene("full", "recall")
cmd.mview("store")

cmd.mview("interpolate", power=2)
```

## Tips

- Use `mview("interpolate", power=2)` for smooth camera motion
- 30 frames = 1 second at typical playback
- Store scenes before creating movies for easier editing
- Ray tracing movies takes significant time
- Export as PNG sequence, then convert to video externally
- `mset("")` clears the movie completely
