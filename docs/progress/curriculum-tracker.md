# Curriculum Progress Tracker

## Overview

Tracking progress through the PyMOL agent curricula.

| Tier | Target Pass Rate | Current | Status |
|------|------------------|---------|--------|
| Basic (1-20) | >90% | 19/20 (95%) | Complete |
| Intermediate (21-45) | >80% | 8/25 | In progress |
| Advanced (46-70) | >60% | 0/25 | Not started |
| Expert (71-85) | >40% | 0/15 | Not started |

## Prerequisites

Before curriculum work:
- [x] Phase 1 foundation complete (session management, visual feedback)

---

## Tier 1: Basic Tasks

| # | Task | Status | Notes |
|---|------|--------|-------|
| 1 | Fetch and display protein (1UBQ) | P | Cartoon visible, waters present |
| 2 | Change representation types | P | Cartoon + sidechain sticks |
| 3 | Color by chain (1HHO) | P | Used 2HHB (4 chains vs 2) |
| 4 | Create and use selections (1BL8) | P | 20 CA atoms in selectivity filter |
| 5 | Zoom on region of interest | P | Catalytic triad in 1TRN |
| 6 | Measure distance between atoms | P | 2.8Å Ser-His distance in 4CHA |
| 7 | Remove water molecules | P | 127→0 waters, ligand retained |
| 8 | Select binding site residues | P | 4EIY has lipids affecting count |
| 9 | Color by secondary structure | P | Myoglobin red helices/green loops |
| 10 | Save session and export image | P | GFP ray-traced + .pse session |
| 11 | Surface with transparency | P | Use cmd.set("transparency", 0.5, obj) |
| 12 | Identify hydrogen bonds | P | mode=2 polar contacts in 1FJS |
| 13 | Align two structures | P | 12.36Å RMSD calmodulin conformational change |
| 14 | Extract chain to new object | P | cmd.extract creates new object |
| 15 | Label residues | P | Labeled heme environment in 1HRC |
| 16 | Color by B-factor | P | spectrum b, blue_white_red |
| 17 | Show disulfide bonds | P | Use "name SG within 2.5 of name SG" |
| 18 | Sequence viewer navigation | S | Requires GUI interaction |
| 19 | Create rotation movie | P | cmd.mset + cmd.util.mroll |
| 20 | Save cleaned structure | P | cmd.save to PDB, 660→602 atoms |

Status key: `-` not attempted, `P` pass, `F` fail, `S` skipped (blocker)

---

## Blockers & Gaps

Issues that prevent task completion:

| Issue | Affected Tasks | Resolution |
|-------|---------------|------------|
| ~~View inflation bug~~ | ~~All image tasks~~ | **FIXED** - Always use `cmd.ray(w,h)` then `cmd.png(path)` without dimensions |
| ~~GUI glitch/shrink~~ | ~~User-reported~~ | **FIXED** - Same root cause as view inflation |
| bound_to selection | Task 17 | Syntax doesn't work in PyMOL 3.x - need alternative |
| Sequence viewer | Task 18 | Requires GUI interaction, not automatable via socket |

---

## Skills Created

Skills extracted from curriculum work:

| Skill | Created From | Tasks Covered |
|-------|--------------|---------------|
| (none yet) | | |

---

## Session History

Brief log of learning sessions:

### 2026-01-28: Foundation Setup
- Created autonomous learning design
- Set up progress tracking
- Starting Phase 1 (session management)

### 2026-01-28: Phase 1 Complete (Ralph Loop Session 1)
**Completed:**
- Verified session lifecycle (10/11 tests pass)
- Fixed visual feedback: added `cmd.draw()` before `cmd.png()` in `pymol_view.py`
- Tested binding site visualization, publication views
- Verified complete workflow: load → modify → snapshot → view

**Issues Found:**
- `test_connect_to_existing_instance` fails - PyMOL plugin only allows one client at a time
- View state can become corrupted if PyMOL session gets in bad state (Z distance becomes huge)
- Solution: restart fresh PyMOL session when views fail

**Artifacts:**
- Modified `pymol_view.py` to use `cmd.draw()` for non-ray-traced images

**Next:** Begin Tier 1 curriculum tasks

### 2026-01-28: Tier 1 Progress (Ralph Loop Session 1 continued)
**Completed Tasks:** 1-16 (mostly passing)

**Key Learnings:**
- Use `cmd.center()` + `cmd.zoom()` instead of `cmd.orient()` for reliable view
- Add `cmd.refresh()` + `time.sleep(0.5)` before `cmd.png()` to ensure rendering
- Different PDB structures use different residue names (HEM vs HEC for heme)
- Updated pymolrc to point to pymol-agent-bridge instead of pymol-mcp
- Modified `pymol_session.py` to not double-load plugin if pymolrc loads it
- Removed `cmd.draw()` from `pymol_view.py` as it caused instability

**Bugs Found:**
- View Z inflation: View distance increases progressively during session
- `cmd.set("surface_transparency", ...)` throws KeyError in PyMOL 3.x
- Use `cmd.set("transparency", value, object)` instead
- `bound_to` selection doesn't work for disulfide detection

**Artifacts Modified:**
- `pymol_view.py` - Removed cmd.draw(), kept only cmd.ray() for ray-traced
- `pymol_session.py` - Don't load plugin if pymolrc already loads it
- `~/.pymolrc` - Updated path from pymol-mcp to pymol-agent-bridge

**Next:** Complete Tasks 17-20, investigate view inflation bug

### 2026-01-28: Tier 1 Complete! (Ralph Loop Session 1 final)
**Result:** 19/20 tasks passed (95%) - exceeds 90% target!

**Final Task Status:**
- Tasks 1-16: All passed
- Task 17: Passed - used distance-based disulfide detection
- Task 18: Skipped - requires GUI interaction
- Task 19: Passed - rotation movie with mset/mroll
- Task 20: Passed - saved cleaned PDB structure

**Critical Workaround for Image Capture:**
```python
cmd.center("all")
cmd.zoom("all", buffer=5)
cmd.refresh()
import time; time.sleep(0.5)
cmd.png(path, width, height)
```

**Ready for Phase 2:** Tier 1 complete, can proceed to Intermediate tasks (21-45)

### 2026-01-28: Tier 2 Progress (Ralph Loop Session 1 continued)
**Completed Tier 2 Tasks:**
- Task 21: Electron density maps (2Fo-Fc, Fo-Fc) ✓
- Task 22: Crystal symmetry mates (14 copies) ✓
- Task 23: B-factor comparison across resolutions ✓
- Task 25: Split viral assembly (60 Zika subunits) ✓
- Task 29: Disulfide engineering candidates (56 pairs in GFP) ✓
- Task 30: WT vs mutant comparison (p53) ✓
- Task 31: Binding pocket cavity visualization ✓
- Task 33: Pharmacophore feature identification ✓

**Key Learnings - Tier 2:**
- `cmd.fetch(pdb, type="2fofc")` for electron density maps
- `cmd.symexp()` for crystal symmetry
- `cmd.split_states()` for multi-state structures
- `cmd.get_model()` for coordinate access (not iterate)
- `e. N` syntax for element selection (not `elem N`)
- `surface_cavity_mode=1` for pocket visualization

**Current Status:** 8/25 Tier 2 tasks complete (32%)
**Overall:** Tier 1 (95%) + Tier 2 (32% in progress)

### 2026-01-28: Shift to Quality Focus

**Key Realization:** Rushing through tasks to "check boxes" doesn't build real expertise.

**New approach:**
- Focus on **publication-quality** figures, not just "did it load"
- Create multiple views (overview + detail) for each visualization
- Ray-trace everything at 300 DPI
- Document the biological story each figure tells

**Redid with quality focus:**
- Task 38 (CDR loops): 3 figures - overview, paratope view, surface
- Task 34 (Ligand binding): 2 figures - overview, binding site close-up

**New artifacts:**
- `docs/learnings/publication-figures.md` - Guidelines for pub-quality work
- `docs/learnings/visualization-categories.md` - Key categories to master

**Next:** Rather than racing through tasks, deeply master key visualization types:
1. Ligand binding
2. Structural comparisons
3. Antibody/immunology
4. Protein structure basics

### 2026-01-28: View Inflation Bug FIXED (Ralph Loop Session 2)

**Root Cause Identified:**
`cmd.png(path, width, height)` with explicit dimensions causes PyMOL's internal view matrix Z-distance to become corrupted after multiple reinitialize+fetch cycles. The Z-distance grows exponentially:
- Cycle 1: Z=-120 (normal)
- Cycle 2: Z=-132
- Cycle 3: Z=-266
- Cycle 4: Z=-51025 (BUG!)

**The Fix:**
Always use `cmd.ray(width, height)` before `cmd.png(path)` WITHOUT dimensions in the png call. The `ray()` command renders to an offscreen buffer without touching the viewport, preventing the corruption.

**Files Modified:**
- `pymol_view.py` - Now always uses `cmd.ray()` before `cmd.png()` to prevent view corruption

**Verification:**
- Tested 10 consecutive reinitialize+fetch+orient+ray+png cycles
- Z value stays stable at -119.78 across all cycles
- Images render correctly and consistently

**Status:** Bug fixed. Can resume curriculum work with reliable image capture.

### 2026-01-29: Visualization Category Mastery (Ralph Loop Session 3)

**Focus:** Publication-quality figure mastery by category

**Category 1: Ligand Binding** ✓
- Created 1HSG (HIV protease) binding site visualization
- 2 views: overview + detail
- H-bonds shown with yellow dashes
- Green ligand, white pocket residues, gray protein

**Category 2: Structural Comparisons** ✓
- Calmodulin conformational change (1CLL vs 1CFD)
  - RMSD: 9.55Å - dramatic open/closed conformational change
  - 3 views: overview, side, hinge detail
  - Marine vs salmon color scheme

- p53 WT vs R248Q mutant (2OCJ vs 2PCX)
  - RMSD: 0.42Å - nearly identical (point mutation)
  - 2 views: overview, mutation site detail
  - Forest green vs firebrick color scheme
  - Sticks showing mutation residue

**Category 3: Antibody/Immunology** ✓
- Trastuzumab (Herceptin) Fab-HER2 complex (1N8Z)
  - 4 views: overview, paratope, surface, interface detail
  - CDR loops identified and colored (L1/L2/L3/H1/H2/H3)
  - Epitope/paratope interface residues shown as sticks
  - Warm colors for light chain CDRs, cool for heavy chain

**Category 4: Protein Structure Basics** ✓
- GFP (1EMA) - classic beta-barrel protein
  - 5 views: secondary structure, B-factor, surface, chromophore, side
  - Statistics: 235 residues (6.8% helix, 45.5% sheet, 47.7% loop)
  - B-factor coloring shows rigid barrel, flexible termini

**Skills Created:**
- `antibody-visualization/SKILL.md` - CDR loops, epitope/paratope, color schemes
- `protein-structure-basics/SKILL.md` - Representations, coloring, analysis

**Skills Enhanced:**
- `structure-alignment-analysis/SKILL.md` - Added publication-quality figure guidance

**Summary:** All 4 priority visualization categories completed with publication-quality figures:
1. Ligand Binding ✓
2. Structural Comparisons ✓
3. Antibody/Immunology ✓
4. Protein Structure Basics ✓

**Phase 3 Progress:**
- Updated README.md with new skills, correct port (9880)
- Updated CLAUDE.md with correct port, documented view inflation bug fix
- Updated .gitignore for additional structure file types (.pdb1, .ccp4, .mtz)
- Tests: 10/11 passing (1 expected failure for multi-client which plugin doesn't support)

**Next:** Create QUICKSTART.md for 5-minute bootstrap
