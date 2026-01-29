# Visual Feedback Exploration Plan

## Goal

Establish a robust feedback loop for working with PyMOL, then use it to discover and fix rough patches across workflow, skills, and user experience.

## Constraints

- PyMOL runs locally with socket plugin on port 9876
- I can send Python code via `pymol_cmd.py`
- I can save PNGs and view them with the Read tool
- No MCP server involved - direct socket communication

## Phase 1: Solidify the Feedback Loop

**Objective:** Make it frictionless to render and view what I'm doing.

Tasks:
- Create a helper function/script that combines: execute commands → save PNG → return path
- Establish a naming convention for scratch images (timestamp or sequential)
- Test the loop with a few simple operations to confirm reliability
- Document any friction points encountered

**Success:** I can go from "idea" to "seeing the result" in one smooth operation.

## Phase 2: Systematic Visualization Testing

**Objective:** Work through common structural biology tasks and evaluate results visually.

Test scenarios (in order of complexity):
1. **Single protein basics** - Load, orient, color by secondary structure
2. **Protein-ligand complex** - Binding site, interactions, ligand highlighting
3. **Multi-chain structure** - Color by chain, interface visualization
4. **Structure comparison** - Align two structures, show differences
5. **Publication figure** - Clean styling, labels, ray tracing

For each scenario:
- Execute the workflow
- Save and view the result
- Note what looks good vs. what needs improvement
- Identify missing commands or awkward patterns

## Phase 3: Identify and Fix Rough Patches

**Objective:** Turn discoveries into improvements.

Categories of fixes:
1. **Tooling** - Helper scripts, better error messages, convenience functions
2. **Skills** - Update existing skills with better patterns, add new skills for gaps
3. **Documentation** - Update COOKBOOK with visual examples, add troubleshooting

## Phase 4: Iterate

**Objective:** Use improved tooling/skills to tackle harder tasks.

Potential advanced scenarios:
- Electrostatic surface visualization
- Symmetry mates / crystal packing
- Membrane protein with lipid bilayer
- Morph between conformations (known to be tricky)

## Deliverables

1. **Improved tooling** - Helper scripts for the feedback loop
2. **Updated skills** - Refined based on visual testing
3. **Learning log updates** - Document what works, what doesn't
4. **Visual examples** - Keep a gallery of successful renders for reference

## Session Log Format

For each experiment:
```
### Experiment: [Name]
**Goal:** What I'm trying to do
**Commands:** What I sent
**Result:** [Image] + observations
**Issues:** Any friction or problems
**Action:** What to fix/improve
```

---

## Session Log: 2026-01-28

### Phase 1 Complete: Feedback Loop Established

**Created:** `pymol_view.py` - helper for visual feedback
- `pymol_view(commands, name, width, height, ray)` - execute and save
- `reset_and_view(pdb_id, style)` - quick structure visualization
- `quick_view()` - snapshot current state

**Issues Encountered & Fixed:**
1. **Commercial PyMOL activation dialog** - Froze GUI thread, created zombie processes
   - **Fix:** Installed open-source PyMOL via `brew install pymol`

2. **Window resizing** - `cmd.viewport()` and `cmd.draw()` resized GUI window
   - **Fix:** Use `cmd.png(path, width, height)` directly instead

3. **Water molecules visible** - Cluttered visualizations with red X markers
   - **Fix:** Added `cmd.remove('solvent')` to `reset_and_view()`

4. **Port conflicts** - Zombie processes held ports 9876-9879
   - **Fix:** Using port 9880 now; update to 9876 after reboot

**Current Configuration:**
- Open-source PyMOL 3.1.0 (Homebrew)
- Socket plugin on port 9880
- Scratch directory: `scratch/`

### Phase 2 Complete: Visualization Testing

| Test | Status | Notes |
|------|--------|-------|
| Single protein | Pass | 1ubq cartoon renders cleanly |
| Protein-ligand | Pass | 1hsg binding site with ligand highlighting works well |
| Multi-chain | Pass | Hemoglobin tetramer with chain coloring |
| Alignment | Pass | Lysozyme overlay (1lyz vs 1hel) |
| Publication figure | Pass | Ray-traced with secondary structure coloring |

**Patterns That Work Well:**
- `cmd.fetch()` + `cmd.remove('solvent')` for clean structures
- `cmd.select('ligand', 'organic')` to find small molecules
- `cmd.select('binding_site', 'byres polymer within 4 of ligand')` for pocket
- `cmd.util.cnc()` for element coloring on sticks
- `cmd.align()` for structure superposition
- `cmd.set('cartoon_fancy_helices', 1)` for nice helix rendering

### Phase 3: Identified Improvements

**Tooling:**
- [ ] Add image review subagent integration to pymol_view.py
- [x] Create convenience functions for common tasks (binding_site_view, etc.)
- [x] Update pymol_connection.py to use port 9880 (or make configurable)

**Skills:**
- [x] Update pymol-fundamentals with tested patterns
- [x] Add binding-site-visualization examples (already comprehensive)
- [x] Add publication-figures skill with ray tracing settings

**Documentation:**
- [x] Add visual examples to COOKBOOK

### Phase 4: Advanced Visualization Testing

| Test | Status | Notes |
|------|--------|-------|
| Electrostatic surface | Pass | Use `cmd.rebuild()` after showing surface; color atoms by charge type |
| Membrane protein | Pass | CGO planes for membrane boundaries; `cmd.turn()` for side view |
| Conformational morph | Partial | `cmd.morph()` not in open-source PyMOL; comparison overlay works |
| Crystal packing | Pass | `cmd.symexp()` generates symmetry mates; color original vs mates |

**Key Learnings:**
- `cmd.rebuild()` is essential after `cmd.show("surface")` for programmatic image capture
- Surface inherits atom colors, so color atoms first then show surface
- Simple charge coloring: blue for ARG+LYS+HIS (positive), red for ASP+GLU (negative)
- True electrostatic potential requires APBS plugin (not tested)

**New Convenience Functions Added to pymol_view.py:**
- `binding_site_view(pdb_id)` - protein-ligand binding site visualization
- `surface_view(pdb_id, color_by_charge)` - surface with optional charge coloring
- `alignment_view(pdb_id1, pdb_id2)` - align and compare two structures
- `publication_view(pdb_id)` - ray-traced publication-quality figure

---

## Final Status: COMPLETE

All major objectives achieved:
- **Phase 1**: Feedback loop established with `pymol_view.py`
- **Phase 2**: 5/5 visualization scenarios pass
- **Phase 3**: Tooling, skills, and documentation updated
- **Phase 4**: 4 advanced scenarios tested (3 pass, 1 partial due to open-source limitation)

**Files Modified/Created:**
- `pymol_view.py` (new) - Visual feedback helper
- `pymol_connection.py` - Port update
- `claude_socket_plugin.py` - Port update
- `.claude/skills/pymol-fundamentals/SKILL.md` - Added tips
- `.claude/skills/publication-figures/SKILL.md` - Added tips
- `docs/COOKBOOK.md` - Added tested workflows
- `.gitignore` - Fixed formatting

**Optional remaining work:**
- Image review subagent integration into pymol_view.py
