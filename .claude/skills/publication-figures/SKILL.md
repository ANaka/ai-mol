---
name: publication-figures
description: Use when creating publication-quality molecular figures with proper styling, ray tracing, and export settings through PyMOL MCP.
version: 0.1.0
---

# Publication Figures

Settings and workflows for creating journal-quality molecular visualizations.

## Background Settings

### White Background

```python
cmd.bg_color("white")
cmd.set("ray_opaque_background", 1)
```

### Transparent Background

```python
cmd.set("ray_opaque_background", 0)
cmd.bg_color("white")  # For preview
# PNG will have transparent background
```

## Quality Settings

### Antialiasing

```python
cmd.set("antialias", 2)  # 0=off, 1=fast, 2=quality
```

### Lighting

```python
# Clean, even lighting
cmd.set("direct", 0.5)  # Direct light intensity
cmd.set("spec_reflect", 0.5)  # Specular reflection
cmd.set("ambient", 0.4)  # Ambient light
```

### Shadows and Depth

```python
# For clean diagrams (no shadows)
cmd.set("ray_shadows", 0)
cmd.set("depth_cue", 0)

# For 3D effect (with shadows)
cmd.set("ray_shadows", 1)
cmd.set("ray_shadow_decay_factor", 0.1)
cmd.set("depth_cue", 1)
```

## Cartoon Styling

### Basic Improvements

```python
cmd.set("cartoon_fancy_helices", 1)
cmd.set("cartoon_smooth_loops", 1)
cmd.set("cartoon_flat_sheets", 1)
```

### Cylinder Helices

```python
cmd.set("cartoon_cylindrical_helices", 1)
```

### Line Width

```python
cmd.set("cartoon_tube_radius", 0.3)
cmd.set("cartoon_loop_radius", 0.3)
```

## Stick Styling

```python
cmd.set("stick_radius", 0.15)
cmd.set("stick_ball", 1)
cmd.set("stick_ball_ratio", 1.5)
```

## Surface Styling

```python
cmd.set("surface_quality", 1)  # Higher = smoother
cmd.set("transparency", 0.5)
cmd.set("surface_color", "white")
```

## Viewport and Resolution

### Set Viewport

```python
cmd.viewport(1200, 900)  # 4:3 aspect
cmd.viewport(1600, 900)  # 16:9 aspect
```

### Common Sizes

| Use Case | Resolution | DPI |
| -------- | ---------- | --- |
| Web/slides | 1200x900 | 72-150 |
| Journal (1 col) | 1200x1200 | 300 |
| Journal (2 col) | 2400x1200 | 300 |
| Poster | 3000x2000 | 300 |

## Rendering

### Preview (Fast)

```python
cmd.draw(1200, 900)  # OpenGL render, fast
```

### Final (Ray Traced)

```python
cmd.ray(1200, 900)  # High quality, slower
```

### Ray Tracing Settings

```python
cmd.set("ray_trace_mode", 1)  # 0=normal, 1=color-only, 3=quantized
cmd.set("ray_trace_gain", 0.1)  # Edge detection
```

## Saving Images

### PNG

```python
# After ray tracing
cmd.png("/path/to/image.png", 1200, 900, dpi=300, ray=1)

# Without ray (faster, lower quality)
cmd.png("/path/to/image.png", 1200, 900, dpi=150, ray=0)
```

### With Ray Tracing

```python
# Combined command
cmd.png("/path/to/figure.png", width=2400, height=1800, dpi=300, ray=1)
```

## Scenes for Figures

### Store Views

```python
cmd.scene("panel_A", "store", message="Overview")
cmd.scene("panel_B", "store", message="Active site")
cmd.scene("panel_C", "store", message="Close-up")
```

### Recall and Export

```python
for panel in ["panel_A", "panel_B", "panel_C"]:
    cmd.scene(panel, "recall")
    cmd.png("/path/to/" + panel + ".png", 1200, 900, dpi=300, ray=1)
```

## Complete Workflow

### Standard Figure

```python
from pymol import cmd

# 1. Load and style
cmd.fetch("1ubq")
cmd.show("cartoon")
cmd.hide("lines")
cmd.dss()
cmd.color("green", "ss h")
cmd.color("yellow", "ss s")
cmd.color("cyan", "ss l+")

# 2. Publication settings
cmd.bg_color("white")
cmd.set("ray_opaque_background", 1)
cmd.set("antialias", 2)
cmd.set("cartoon_fancy_helices", 1)
cmd.set("ray_shadows", 0)
cmd.set("depth_cue", 0)

# 3. View
cmd.orient()
cmd.zoom("all", 2)

# 4. Export
cmd.png("/path/to/figure.png", 2400, 1800, dpi=300, ray=1)
```

### Multi-Panel Figure

```python
# Set up views
cmd.orient()
cmd.scene("overview", "store")

cmd.zoom("resi 45-50", 5)
cmd.scene("detail", "store")

# Export each
import os
output_dir = os.path.expanduser("~/Desktop")

for scene in ["overview", "detail"]:
    cmd.scene(scene, "recall")
    cmd.png(output_dir + "/" + scene + ".png", 1200, 900, dpi=300, ray=1)
```

## Color Recommendations

### Colorblind-Friendly

```python
# Blue/Orange (safe)
cmd.color("marine", "chain A")
cmd.color("orange", "chain B")

# Teal/Coral
cmd.color("teal", "chain A")
cmd.color("salmon", "chain B")
```

### Classic Schemes

```python
# Secondary structure
cmd.color("red", "ss h")     # Helices
cmd.color("yellow", "ss s")  # Sheets
cmd.color("green", "ss l+")  # Loops

# By chain
cmd.do("util.cbc")
```

## Tips

- Ray trace final figures; use `draw` for previews
- 300 DPI for print, 150 DPI for web/slides
- Disable shadows for clean diagrams
- White background is standard for journals
- Store scenes before adjusting for different panels
- Test colors with colorblindness simulators
