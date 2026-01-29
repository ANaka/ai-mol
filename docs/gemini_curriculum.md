# Comprehensive Curriculum for Agentic Structural Biology and Molecular Visualization in PyMOL

The advent of automated structural biology requires a paradigm shift in how molecular visualization software is utilized by artificial intelligence. PyMOL, an open-source molecular graphics system with an embedded Python interpreter, has long been the gold standard for real-time visualization and the generation of high-quality molecular images. For an AI agent, such as a Claude Code instance, to become proficient in this domain, it must move beyond simple command execution and develop a nuanced understanding of structural hierarchy, experimental data types, and field-standard aesthetic requirements. 

This curriculum provides a rigorous, 100-step progressive framework designed to transition an agent from foundational atomic manipulation to expert-level biological hypothesis generation and publication-standard figure production.

## Foundations of Automated Structural Bioinformatics

Structural bioinformatics is a critical interdisciplinary domain that combines computational techniques with the analysis of biological data. At its core, the field examines biomolecular structures, such as proteins and nucleic acids, and their complex interactions. PyMOL serves as a powerful utility for studying these molecules because it is highly polished, produces high-quality graphics without requiring manual text editing of POV-Ray files, and possesses an extensive help system. However, for an agent to control PyMOL effectively via a socket connection, it must master the "mouse matrix" through API commands and navigate the "External GUI" and "Visualization Area" programmatically.

The most frequent tasks structural biologists perform in PyMOL involve a sequence of operations that constitute a "canonical" workflow: loading a structure, cleaning up non-essential atoms (such as redundant waters or crystallization buffers), aligning the structure to a reference, visualizing specific motifs (like binding sites or catalytic triads), measuring geometric properties, and finally exporting a rendered figure. Human users often find multi-step selection logic and parameter optimization for ray-tracing to be tedious bottlenecks. By automating these workflows, an agentic system can provide rapid insights into molecular functions, drug development, and evolutionary relationships.

## Summary of Core PyMOL Mechanics for Agents

| Mechanical Category | API Command / Concept | Biological Utility |
|---------------------|----------------------|-------------------|
| Selection Algebra | `select name, selection-expression` | Identifying functional atoms, residues, or chains. |
| Representations | `show/hide cartoon, sticks, spheres` | Visualizing secondary vs. tertiary structure. |
| View Management | `zoom, orient, center` | Navigating to regions of interest like active sites. |
| Metric Analysis | `distance, angle, dihedral` | Quantifying interactions and bond geometry. |
| State Control | `split_states, intra_fit` | Analyzing MD trajectories or NMR ensembles. |

---

## Tier 1: Foundational Mechanics and Atomic Operations

The primary goal of the first tier is to establish a solid foundation in PyMOL's syntax and the internal logic of the Protein Data Bank (PDB). The agent must learn to acquire data, manipulate basic representations, and perform the initial "cleanup" tasks that are mandatory before any meaningful analysis can begin.

### Test Case 1: Structure Acquisition and Basic Initialization

- **Task Description:** "Fetch the structure of human hemoglobin (PDB: 4HHB), clear the workspace of any previous data, and center the view on the protein."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `reinitialize`, `fetch 4hhb`, `center`
- **Success Criteria:** The workspace must contain exactly one object named "4hhb" centered in the viewer.
- **Common Failure Modes:** Retaining data from previous sessions due to failure to reinitialize.
- **Representative PDB Codes:** 4HHB, 1HEL

### Test Case 2: Hierarchy-Based Selection Logic

- **Task Description:** "Select all alpha-carbon atoms in the loaded structure and store them as a new selection named 'ca_atoms'."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `select ca_atoms, name ca`
- **Success Criteria:** A new selection entry "ca_atoms" appears in the right-hand panel containing only $C_\alpha$ atoms.
- **Common Failure Modes:** Selecting all carbon atoms (`elem c`) instead of specifically alpha-carbons.
- **Representative PDB Codes:** 1TIM, 2PYP

### Test Case 3: Representation Toggling and Visibility

- **Task Description:** "Hide the default lines and non-bonded representations. Display the protein as a cartoon and any ligands as sticks."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `hide everything`, `show cartoon`, `show sticks, organic`
- **Success Criteria:** The protein backbone is shown as a ribbon-like cartoon; ligands are shown with bond-thickness sticks.
- **Common Failure Modes:** Leaving "lines" on, which creates visual clutter when overlaid with "cartoon."
- **Representative PDB Codes:** 1T46, 2HT8

### Test Case 4: Secondary Structure Coloring

- **Task Description:** "Color the protein such that alpha-helices are red, beta-sheets are yellow, and loops are green."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `color red, ss h`, `color yellow, ss s`, `color green, ss l+""`
- **Success Criteria:** Visual verification of a tri-color scheme mapping precisely to secondary structure elements.
- **Common Failure Modes:** Using `ss l` without the empty string check, which may miss some loop regions.
- **Representative PDB Codes:** 3V03, 1A8G

### Test Case 5: Chain-Specific Manipulation

- **Task Description:** "For a dimeric structure, color Chain A cyan and Chain B magenta."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `color cyan, chain A`, `color magenta, chain B`
- **Success Criteria:** Each monomer is rendered in a distinct solid color.
- **Common Failure Modes:** Using residue ranges instead of chain identifiers.
- **Representative PDB Codes:** 1TIM, 1A8G

### Test Case 6: Basic Interatomic Measurement

- **Task Description:** "Measure the distance between the catalytic triad residues Asp102 and Ser195 in PDB 1SGB."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `distance d1, (resi 102 and name cg), (resi 195 and name og)`
- **Success Criteria:** A distance object "d1" is created with the correct measurement value in $\text{\AA}$.
- **Common Failure Modes:** Measuring from $C_\alpha$ to $C_\alpha$ instead of functionally relevant sidechain atoms.
- **Representative PDB Codes:** 1SGB, 3SGB

### Test Case 7: Simple Object Renaming and Organization

- **Task Description:** "Load 1HEL and 1AKI. Rename them to 'Hen_Lysozyme' and 'Human_Lysozyme' respectively."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `set_name`
- **Success Criteria:** The internal object list reflects the new, descriptive names.
- **Common Failure Modes:** Renaming selections instead of the parent objects.
- **Representative PDB Codes:** 1HEL, 1AKI

### Test Case 8: Workspace Orientation via Selection

- **Task Description:** "Orient the view to maximize the visibility of the ligand in 2HT8."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `orient organic`
- **Success Criteria:** The camera rotates and zooms to center the ligand in the viewer.
- **Common Failure Modes:** Using `center` which only shifts the origin without aligning the axes for optimal viewing.
- **Representative PDB Codes:** 2HT8

### Test Case 9: Element-Based Selection for Cysteine Bridges

- **Task Description:** "Select all sulfur atoms to identify potential disulfide bridges."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `select sulfur, elem s`
- **Success Criteria:** Exactly all Sulfur atoms (from Cys and Met residues) are highlighted.
- **Common Failure Modes:** Selecting Phosphorus or other heavy elements by mistake.
- **Representative PDB Codes:** 1EBZ, 7RSA

### Test Case 10: High-Resolution Image Export

- **Task Description:** "Render the current scene at 1920x1080 resolution and save it as 'figure_1.png'."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `ray 1920, 1080`, `png figure_1.png`
- **Success Criteria:** A high-quality PNG file is generated on the filesystem.
- **Common Failure Modes:** Saving a screenshot without ray tracing, resulting in low-quality aliased edges.
- **Representative PDB Codes:** Any

### Test Case 11: Background Color and Fog Management

- **Task Description:** "Change the background color to white and turn off fog to improve depth clarity."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `bg_color white`, `set fog, 0`
- **Success Criteria:** The workspace background is solid white without atmospheric fading.
- **Common Failure Modes:** Fog interferes with the visibility of distant parts of large complexes.
- **Representative PDB Codes:** 3J3Q

### Test Case 12: Sequence Extraction for Sanity Checks

- **Task Description:** "Display the primary sequence of the loaded protein in the internal GUI."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `set seq_view, 1`
- **Success Criteria:** The one-letter amino acid code sequence appears at the top of the viewer.
- **Common Failure Modes:** Failing to enable the sequence view before attempting sequence-based selections.
- **Representative PDB Codes:** 1HEW

### Test Case 13: Residue Selection via Sequence Bar

- **Task Description:** "Select residues 4 to 16 in the protein sequence and name the selection 'helix_1'."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `select helix_1, resi 4-16`
- **Success Criteria:** Residues in the specified range are highlighted and stored as a group.
- **Common Failure Modes:** Incorrect residue numbering if the PDB file has insertion codes.
- **Representative PDB Codes:** 1HEW

### Test Case 14: Simple B-Factor Coloring

- **Task Description:** "Color the structure according to the temperature factors (B-factors) provided in the PDB file."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `spectrum b, blue_white_red`
- **Success Criteria:** The structure displays a gradient from blue (low B-factor, rigid) to red (high B-factor, flexible).
- **Common Failure Modes:** Not understanding that B-factors represent displacement parameters.
- **Representative PDB Codes:** 1SNC

### Test Case 15: Identifying Water Molecules

- **Task Description:** "Select and hide all water molecules to focus on the protein structure."
- **Difficulty Tier:** Basic
- **Required PyMOL Operations:** `select waters, resn hoh`, `hide everything, waters`
- **Success Criteria:** The solvent atoms are removed from the visual display but retained in the object.
- **Common Failure Modes:** Deleting waters permanently before checking if any mediate ligand binding.
- **Representative PDB Codes:** 1YET

---

## Tier 2: Intermediate Comparative and Quantitative Analysis

In this tier, the agent advances to tasks involving structural comparison, surface analysis, and more complex geometric logic. These skills are essential for identifying functional differences between homologs or variants.

### Test Case 16: Structural Alignment via RMSD

- **Task Description:** "Superimpose a mutant structure (1STN) onto the wild-type (2STN) and report the $RMSD$."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `align 1stn, 2stn`
- **Success Criteria:** The structures are spatially aligned; the console prints the $RMSD$ in $\text{\AA}$.
- **Common Failure Modes:** Using `align` on sequences with very low identity; `cealign` would be required for divergent homologs.
- **Representative PDB Codes:** 1STN, 2STN

### Test Case 17: Generating Biological Assemblies

- **Task Description:** "Reconstruct the biological hexamer of insulin from the monomeric asymmetric unit."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `symexp sym, 1ins, (1ins), 5.0`
- **Success Criteria:** Multiple symmetry-related objects appear, forming the correct oligomeric state.
- **Common Failure Modes:** Setting the distance cutoff too low to capture all neighbors in the lattice.
- **Representative PDB Codes:** 1INS

### Test Case 18: Solvent Accessible Surface Area (SASA) Calculation

- **Task Description:** "Display the solvent accessible surface of the protein and color it by residue hydrophobicity."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `show surface`, `select hydrophobes, resn ala+gly+val+ile+leu+phe+met+pro`, `color grey, hydrophobes`
- **Success Criteria:** The protein is shown as a solid surface with hydrophobic patches visually distinct.
- **Common Failure Modes:** Showing a "molecular surface" when a "solvent accessible" surface was requested.
- **Representative PDB Codes:** 1HEW

### Test Case 19: Transparency and Pocket Visualization

- **Task Description:** "Show the protein surface with 40% transparency to allow viewing of the internal ligand."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `set transparency, 0.4`, `show surface`
- **Success Criteria:** The internal cavity and ligand are visible through the semi-opaque protein shell.
- **Common Failure Modes:** Surface becomes invisible if transparency is set too close to $1.0$.
- **Representative PDB Codes:** 2HT8, 3U5J

### Test Case 20: Hydrogen Bond Detection (Basic)

- **Task Description:** "Find and display all potential hydrogen bonds between the ligand and the receptor."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `dist h_bonds, ligand, protein, mode=2`
- **Success Criteria:** Yellow dashed lines indicate polar contacts within standard geometric cutoffs.
- **Common Failure Modes:** Missing bonds because hydrogens were not added (`h_add`) to the structure.
- **Representative PDB Codes:** 1ABE

### Test Case 21: Catalytic Triad Zoom and Labeling

- **Task Description:** "Focus the camera on the catalytic triad (Asp, His, Ser) and label the $C_\alpha$ atoms with residue names."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `zoom triad`, `label triad and name ca, "%s-%s" % (resn, resi)`
- **Success Criteria:** The view is tight on the active site with clear text labels identifying each residue.
- **Common Failure Modes:** Labeling every atom in the residue, leading to unreadable text overlap.
- **Representative PDB Codes:** 1SGB

### Test Case 22: Mutagenesis and Steric Clash Analysis

- **Task Description:** "Mutate a buried Alanine to a bulky Tryptophan and identify potential steric clashes."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `wizard mutagenesis`, `show patches`
- **Success Criteria:** The mutation is performed, and "red disks" or high $VDW$ overlap areas are visible.
- **Common Failure Modes:** Selecting a rotamer that is energetically unfavorable without checking the library probabilities.
- **Representative PDB Codes:** 1L2Y

### Test Case 23: Creating Scenes for a Storyboard

- **Task Description:** "Store two scenes: Scene 1 (overview) and Scene 2 (binding site). Toggle between them to verify storage."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `scene F1, store`, `scene F2, store`, `scene F1, recall`
- **Success Criteria:** The camera and representation states (e.g., surface vs. sticks) are correctly restored upon recall.
- **Common Failure Modes:** Not using `scene store`, leading to the loss of representation settings between views.
- **Representative PDB Codes:** 1T46

### Test Case 24: Vacuum Electrostatics Mapping

- **Task Description:** "Calculate the vacuum electrostatic potential and map it onto the molecular surface."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `action > generate > vacuum electrostatics`
- **Success Criteria:** The surface is colored with Red (negative) and Blue (positive) gradients.
- **Common Failure Modes:** Computation fails if the structure has non-standard residues without defined charges.
- **Representative PDB Codes:** 2CBA

### Test Case 25: Fragment Separation for Multi-Chain Complexes

- **Task Description:** "Separate a heteromeric complex into individual objects based on chain ID."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `split_chains`
- **Success Criteria:** The object list grows to include each chain as a separate entity.
- **Common Failure Modes:** Overlapping objects if the original object is not hidden.
- **Representative PDB Codes:** 4HHB

### Test Case 26: Dihedral Angle Measurement for Ramachandran Check

- **Task Description:** "Measure the $\phi$ and $\psi$ angles for residue 50 in the protein."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `phi_psi_res = cmd.get_phi_psi('resi 50')`
- **Success Criteria:** The two dihedral values are retrieved and printed in degrees.
- **Common Failure Modes:** Measuring angles on the first or last residue, which lack the necessary neighbors for full dihedrals.
- **Representative PDB Codes:** 1HEL

### Test Case 27: Measuring Plane Angles Between Helices

- **Task Description:** "Calculate the angle between the axes of two prominent alpha-helices."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `angle_between_helices selection1, selection2` (via script)
- **Success Criteria:** An angular measurement reflecting the relative orientation of the two domains.
- **Common Failure Modes:** Selecting too few residues to define a stable helical axis.
- **Representative PDB Codes:** 1TIM

### Test Case 28: Coloring by Sequence Conservation

- **Task Description:** "Color the protein surface by conservation scores (ConSurf style) provided in the B-factor column."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `spectrum b, white_purple`
- **Success Criteria:** Functional "hotspots" appear deeply colored while variable regions remain light.
- **Common Failure Modes:** Inverting the color scheme (making variable regions dark).
- **Representative PDB Codes:** Homology models with conservation data

### Test Case 29: Ball-and-Stick vs. CPK Representations

- **Task Description:** "Represent the ligand in ball-and-stick mode by combining spheres and sticks with specific scaling."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `show sticks, ligand`, `show spheres, ligand`, `set sphere_scale, 0.3`
- **Success Criteria:** The ligand has defined atoms (spheres) and bonds (sticks) of appropriate proportions.
- **Common Failure Modes:** Default sphere size ($1.0 \text{\AA}$) obscures the stick representation.
- **Representative PDB Codes:** 2HT8

### Test Case 30: Automated Distance Matrix Generation

- **Task Description:** "Calculate a distance matrix between all $C_\alpha$ atoms within a $10 \text{\AA}$ radius of the ligand."
- **Difficulty Tier:** Intermediate
- **Required PyMOL Operations:** `find_pairs`, `iterate`, `distance`
- **Success Criteria:** A list or file containing all inter-residue distances for the pocket.
- **Common Failure Modes:** Computational overhead if the radius is set too large (e.g., the whole protein).
- **Representative PDB Codes:** 3EML

---

## Tier 3: Domain-Specific Expertise

The third tier requires the agent to handle domain-specific experimental data types, such as electron density maps from X-ray crystallography and reconstruction maps from Cryo-EM.

### Crystallography: Interpretation of Electron Density

Crystallography produces electron density maps, which are the primary results of the experiments. The atomic model is an interpretation of these maps.

#### Test Case 31: Loading and Contouring 2Fo-Fc Maps

- **Task Description:** "Fetch PDB 4EIY and its map. Display the 2Fo-Fc map at $1.0 \sigma$ around the ligand."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `fetch 4eiy, type=2fofc`, `isomesh map1, 2fofc, 1.0, ligand, carve=2.0`
- **Success Criteria:** A blue mesh correctly encapsulates the ligand density.
- **Common Failure Modes:** Memory crash from loading the entire unit cell map instead of "carving" around the selection.

#### Test Case 32: Difference Map (Fo-Fc) Visualization

- **Task Description:** "Show positive difference density at $+3.0 \sigma$ and negative at $-3.0 \sigma$."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `isomesh pos, fofc, 3.0`, `isomesh neg, fofc, -3.0`, `color green, pos`, `color red, neg`
- **Success Criteria:** Visual cues (green/red blobs) indicate where the model doesn't fit the data.
- **Common Failure Modes:** Incorrectly identifying positive density as "missing atoms" when it might be noise.

#### Test Case 33: Identifying Solvent Molecules in Density

- **Task Description:** "Verify if a specific water molecule is supported by electron density at $1.5 \sigma$."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `isomesh water_check, 2fofc, 1.5, resi 500, carve=1.5`
- **Success Criteria:** Clear density surrounds the oxygen atom of the water.
- **Common Failure Modes:** Low contour levels ($<0.8 \sigma$) showing false-positive density.
- **Representative PDB Codes:** 4EIY

### Cryo-EM: Map Fitting and Validation

Cryo-EM workflows often involve large, multi-domain complexes where model-to-map validation is paramount.

#### Test Case 34: Loading Cryo-EM Maps and Isosurfaces

- **Task Description:** "Load EMDB-3342 and display the isosurface at the author-recommended level of 0.015."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `load emd_3342.map`, `isosurface surf1, emd_3342, 0.015`
- **Success Criteria:** A solid surface appears representing the high-resolution reconstruction.
- **Common Failure Modes:** Choosing a level that results in "dust" (too low) or "holes" (too high).

#### Test Case 35: Local Resolution Coloring on Maps

- **Task Description:** "Map local resolution data onto the EM map surface using a color gradient."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `load local_res.mrc`, `color_sample map_surface, local_res`
- **Success Criteria:** The map is colored by its local quality (e.g., blue for core, red for flexible periphery).
- **Common Failure Modes:** Mismatch in voxel spacing between the primary map and the local resolution map.

#### Test Case 36: Model-in-Map Cross-Correlation Check

- **Task Description:** "Calculate the correlation coefficient between the atomic model and the EM map."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** External script integration; `volume_correlation`
- **Success Criteria:** A numerical value (0 to 1) indicating the quality of the fit.
- **Common Failure Modes:** Failing to account for different voxel sizes in simulated vs. experimental maps.

### Drug Discovery and Binding Site Analysis

The focus here is on identifying cavities and visualizing interactions that determine drug potency.

#### Test Case 37: Automated Binding Site Identification (Cleft Finding)

- **Task Description:** "Find the largest cavity in the protein and orient the view to it."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `run getcleft.py`, `select largest_cleft, cleft01`
- **Success Criteria:** A dummy-atom or mesh representation of the binding pocket is created.
- **Common Failure Modes:** Identifying internal structural voids that are not solvent-accessible.

#### Test Case 38: Ligand-Protein Interaction Map (2D/3D Hybrid)

- **Task Description:** "Identify all hydrophobic and polar contacts for the bound inhibitor and highlight them."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `dist`, `select hydrophobes`, `show dots`
- **Success Criteria:** A comprehensive visual summary of the binding mode.
- **Common Failure Modes:** Over-labeling interactions, making the figure unreadable.

#### Test Case 39: Docking Pose Comparison

- **Task Description:** "Compare the native ligand pose with three different docking predictions and calculate heavy-atom $RMSD$ for each."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `align (ligand and resn PRED), (ligand and resn NATIVE)`
- **Success Criteria:** Precise $RMSD$ values for the ligand orientation.
- **Common Failure Modes:** Aligning the protein backbones but failing to isolate the ligand for the $RMSD$ calculation.

### Membrane Protein Workflows

Membrane proteins require special handling to represent the hydrophobic environment of the lipid bilayer.

#### Test Case 40: Membrane Plane Representation

- **Task Description:** "Load 1C3W from the OPM database and visualize the membrane boundaries."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `pseudoatom top, pos=`, `pseudoatom bot, pos=[0,0,-15]`, `show cgo`
- **Success Criteria:** Two parallel planes represent the core of the bilayer.
- **Common Failure Modes:** Incorrect orientation relative to the membrane normal (Z-axis).

#### Test Case 41: Ion Pathway (Pore) Visualization

- **Task Description:** "Identify the central conduction pathway in an ion channel and visualize its radius."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** Integration with HOLE or CAVER.
- **Success Criteria:** A colored "tube" indicating the constriction points of the channel.
- **Common Failure Modes:** Selecting a start point for the search that is outside the channel.

### Antibody and Immunology Workflows

Antibody visualization relies on standardized numbering schemes like Kabat or Chothia.

#### Test Case 42: CDR Annotation and Coloring

- **Task Description:** "Identify and color the Complementarity Determining Regions (CDRs) of the heavy and light chains."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `annotate_v("VH", "chothia")`
- **Success Criteria:** Six distinct loops are colored according to their CDR identity (H1, H2, H3, L1, L2, L3).
- **Common Failure Modes:** Misnumbering the residues if the scheme used by the agent differs from the one in the PDB file.

#### Test Case 43: Epitope Mapping of a Viral Antigen

- **Task Description:** "Highlight all residues on the Viral Spike protein that are within $5 \text{\AA}$ of the neutralizing antibody."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `select epitope, (chain A) within 5.0 of (chain H or chain L)`
- **Success Criteria:** The binding footprint is clearly visible on the antigen surface.
- **Common Failure Modes:** Including framework residues in the selection if chain boundaries are not strict.

---

## Tier 4: Integrative Modeling and Dynamic Visualization

The fourth tier focuses on the integration of data from external computational pipelines, such as Molecular Dynamics (MD) and AlphaFold structure predictions.

### Molecular Dynamics (MD) Trajectories

Trajectories present unique challenges because they involve multiple "states" of the same object.

#### Test Case 44: Loading and Playing MD Trajectories

- **Task Description:** "Load a 500-frame MD trajectory and animate it at 30 frames per second."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `load traj.xtc, protein`, `mplay`
- **Success Criteria:** Smooth visual movement of the protein over time.
- **Common Failure Modes:** Jittery movement due to lack of periodic boundary alignment (`intra_fit`).

#### Test Case 45: Trajectory Smoothing and Fitting

- **Task Description:** "Perform a 5-frame moving average smooth on the trajectory to reduce high-frequency noise."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `smooth protein, 2`, `intra_fit protein`
- **Success Criteria:** A cleaner, more biologically relevant view of large-scale motions.
- **Common Failure Modes:** Over-smoothing, which removes important small-scale fluctuations.

#### Test Case 46: RMSF Mapping over Trajectory

- **Task Description:** "Calculate the Root Mean Square Fluctuation (RMSF) per residue and color the structure by it."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** Python iteration over `cmd.get_coordset`.
- **Success Criteria:** Flexible regions (loops) appear red; rigid cores appear blue.
- **Common Failure Modes:** Failure to align the trajectory to a reference state before calculation.

### AlphaFold and Machine Learning Outputs

Machine learning models provide confidence metrics that must be visualized to interpret the reliability of the models.

#### Test Case 47: pLDDT Score Mapping

- **Task Description:** "Color the AlphaFold model using the standard confidence scale: blue ($>90$), cyan ($70-90$), yellow ($50-70$), orange ($<50$)."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** `spectrum b, red_yellow_green_cyan_blue, minimum=0, maximum=100`
- **Success Criteria:** The model looks identical to the view in the AlphaFold Database.
- **Common Failure Modes:** Not realizing that AlphaFold stores pLDDT in the B-factor column.

#### Test Case 48: PAE Confidence in Multimers

- **Task Description:** "For an AlphaFold multimer, highlight regions where the inter-domain orientation is uncertain ($PAE > 15 \text{\AA}$)."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** Integration with PAE JSON data.
- **Success Criteria:** The agent identifies "wobbly" domains that should not be used for docking.
- **Common Failure Modes:** Difficulty mapping the $N \times N$ matrix indices to the PDB residue numbers.

### Binder Design and Adaptyv Competitions

De novo binder design requires identifying hotspots and validating interfaces with scores like ipSAE.

#### Test Case 49: Hotspot Identification for Binder Design

- **Task Description:** "Identify hydrophobic patches on the target protein that are also solvent-accessible."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** `select hotspots, (resn leu+ile+phe+trp) and (sasa > 20)`
- **Success Criteria:** Selection of "druggable" or "bindable" regions on the target.
- **Common Failure Modes:** Selecting hydrophobic residues that are buried in the protein core.

#### Test Case 50: Trimming PDBs for Computational Tools

- **Task Description:** "Trim the protein to include only the binding domain and remove all distal loops for use in RFdiffusion."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** `select keep, domain_A`, `remove not keep`
- **Success Criteria:** A clean PDB file containing only the minimal structural motif required for the design tool.
- **Common Failure Modes:** Removing too much structural context, causing the design tool to fail.

---

## Tier 5: Expert Synthesis and Novel Agentic Capabilities

The final tier pushes the agent into the realm of biological hypothesis generation and expert-level comparative analysis.

### Test Case 51: Comparative Mechanism Analysis (HcKCR1 vs. ChRmine)

- **Task Description:** "Load HcKCR1 (8GI8) and ChRmine (7Z09). Compare their retinal binding pockets and highlight residues that explain the blue-shift in HcKCR2."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** `align 8gi8, 7z09`, `select retinal_pocket, resi 140+136 in 8h86`
- **Success Criteria:** Detailed visualization of the steric clash (e.g., Ala140 in HcKCR2 vs. Gly in HcKCR1) that induces retinal rotation.
- **Common Failure Modes:** Missing the subtle difference in ionone ring geometry.

### Test Case 52: Rational Thermostability Engineering

- **Task Description:** "Suggest three mutations to improve the thermostability of the target protein without disrupting the active site."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** Cavity analysis and hydrophobic packing check.
- **Success Criteria:** Proposal of packing mutations (e.g., Ala to Val in a cavity) or new disulfide bonds.
- **Common Failure Modes:** Suggesting mutations in conserved catalytic residues.

### Test Case 53: Hypothesis Generation for Kinetic Anomalies

- **Task Description:** "What structural features might explain why this variant has a $10 \times$ slower off-rate?"
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** H-bond and salt-bridge network analysis.
- **Success Criteria:** Identifying an additional interaction (e.g., a new salt bridge) that stabilizes the bound state.
- **Common Failure Modes:** Over-interpreting small geometric differences as the primary cause.

### Test Case 54: Literature-Informed Residue Highlighting

- **Task Description:** "Read the provided summary of the 'Inner Gate' in Channelrhodopsins and highlight the corresponding residues in CrChR2."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** NLP-to-Selection mapping.
- **Success Criteria:** Correct highlighting of Glu82, Glu83, and His134.
- **Common Failure Modes:** Incorrect residue numbering if the paper uses an isoform (e.g., HcKCR1 numbering instead of CrChR2).

### Test Case 55: Automated H-Bond Refinement Scripting

- **Task Description:** "Implement a custom script to identify H-bonds using strict heavy-atom distance ($3.2 \text{\AA}$) and angle ($>120^{\circ}$) criteria."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** `iterate_state`, `get_angle`, `distance`
- **Success Criteria:** A more reliable H-bond list than the default "polar contacts".
- **Common Failure Modes:** Mathematical errors in calculating the donor-hydrogen-acceptor angle.

### Summary of Expert Capabilities

| Capability | PyMOL Requirement | Biological Outcome |
|------------|-------------------|-------------------|
| Structural Design | Mutagenesis + Sculpting | Engineering of new functions. |
| Comparative Genomics | Sequence-Structure Mapping | Identifying conservation-driven hotspots. |
| Experimental Validation | Model-to-Map Fitting | Ensuring atomic models match raw data. |
| Publication Ready | `ray` + `set_state` | High-impact journal figures. |

---

## Advanced Publication-Quality Production

High-impact journals like Nature, Science, and Cell have strict requirements for molecular figures. An agent must master these settings to produce usable results.

### Publication-Standard Settings Table

| Parameter | PyMOL Command | Journal Standard |
|-----------|---------------|------------------|
| Background | `bg_color white` | Required for clear printing. |
| Ray Tracing | `set ray_trace_mode, 1` | Natural colors with black outlines for definition. |
| Anti-aliasing | `set antialias, 2` | Smooth edges without excessive blur. |
| Shadows | `set ray_shadows, 0` | Often turned off to avoid occluding details. |
| Resolution | `png figure.png, dpi=300` | Mandatory for publication. |

### Test Case 56: Multi-Panel Figure Layout

- **Task Description:** "Create a 3-panel figure: (A) Overview, (B) Active Site, (C) Conservation surface. Export as a single high-resolution image."
- **Difficulty Tier:** Advanced
- **Required PyMOL Operations:** PyMOL-PUB logic or viewport + scene automation.
- **Success Criteria:** A single file with consistent lighting and scales across panels.
- **Common Failure Modes:** Inconsistent background or fog settings across scenes.

### Test Case 57: Cinematic Movie Generation

- **Task Description:** "Create a 10-second movie that slowly rotates the protein $360^{\circ}$ while transitioning from cartoon to surface representation."
- **Difficulty Tier:** Expert
- **Required PyMOL Operations:** `mset`, `mview`, `util.mroll`
- **Success Criteria:** A smooth MP4 or GIF suitable for a supplemental video.
- **Common Failure Modes:** Discontinuous "jump" at the loop point of the animation.

---

## Curated List of Test Cases (58-100)

The following table summarizes the remaining test cases required to reach the target curriculum depth, spanning all requested domains.

| Case # | Domain | Difficulty | Brief Description | Representative PDB |
|--------|--------|------------|-------------------|-------------------|
| 58 | Crystallography | Advanced | B-factor putty representation of a ribosome. | 4V6W |
| 59 | Cryo-EM | Advanced | Map-to-model FSC calculation. | EMD-3001 |
| 60 | Drug Discovery | Intermediate | Identifying water-mediated ligand contacts. | 1YET |
| 61 | Membranes | Advanced | Visualizing pore-water in a transporter. | 6VMS |
| 62 | Protein Eng. | Expert | Designing a disulfide bond to lock a conformation. | 1AKE |
| 63 | Antibodies | Advanced | Epitope mapping of Omicron Spike vs. mAb. | 7K8Z |
| 64 | Binder Design | Advanced | Trimming PDB for AlphaFold-Multimer docking. | 6VSB |
| 65 | MD Visual | Advanced | Visualizing a hinge-bending motion ensemble. | 1AKE |
| 66 | Integration | Expert | Plotting APBS potential on a DNA surface. | 1BNA |
| 67 | Publication | Advanced | Creating a 'depth-cue' figure with fog settings. | 3J3Q |
| 68 | Novel Agent | Expert | Comparing HcKCR1 (8GI8) and WiChR (AF-model). | 8GI8 |
| 69 | Mechanics | Basic | Aligning multiple chains of a large complex. | 4V4A |
| 70 | Mechanics | Basic | Identifying non-standard ligands (HETATM). | Any |
| 71 | Crystallography | Advanced | Displaying unit cell axes and boundaries. | 4EIY |
| 72 | Cryo-EM | Advanced | Segmenting a map by domain density. | EMD-2984 |
| 73 | Drug Discovery | Advanced | Pharmacophore visualization (mesh on site). | 1FJS |
| 74 | Membranes | Advanced | Z-axis normal calculation for bilayer center. | 1C3W |
| 75 | Protein Eng. | Intermediate | Modeling a SNP (single nucleotide polymorphism). | 4E26 |
| 76 | Antibodies | Advanced | Calculating paratope area per CDR loop. | 1BJ1 |
| 77 | Binder Design | Expert | Scoring an interface by iPAE standard. | Designed |
| 78 | MD Visual | Expert | Principal Component Analysis (PCA) mode display. | 1TIM |
| 79 | Integration | Advanced | Mapping PDB to UniProt variants. | 4E26 |
| 80 | Publication | Advanced | Using ray_trace_mode 3 for 'comic' effect. | Any |
| 81 | Novel Agent | Expert | Suggesting mutations for 'K+ selectivity shift'. | 8GI8 |
| 82 | Mechanics | Basic | Measuring dihedral angles of a ligand. | 1T46 |
| 83 | Crystallography | Advanced | Generating anomalous difference density maps. | 1EBZ |
| 84 | Cryo-EM | Expert | Refitting a flexible loop into 4A density. | EMD-3342 |
| 85 | Drug Discovery | Advanced | Visualizing covalent bond formation in a site. | 1HHP |
| 86 | Membranes | Advanced | Highlighting the selectivity filter of KcsA. | 1BL8 |
| 87 | Protein Eng. | Expert | Identifying 'dead-space' cavities for packing. | 1L2Y |
| 88 | Antibodies | Advanced | Color by IMGT numbering scheme. | 3HFM |
| 89 | Binder Design | Expert | Selecting residues for 'Binder-Target' iPAE. | 6VSB |
| 90 | MD Visual | Advanced | Extracting a PDB from a specific frame. | Traj |
| 91 | Integration | Expert | Visualizing NMR constraints (UPL/CNS files). | 1L2Y |
| 92 | Publication | Expert | Making a cross-fading movie between scenes. | Any |
| 93 | Novel Agent | Expert | Predicting impact of pH shift on salt bridges. | 1AF7 |
| 94 | Mechanics | Basic | Calculating the centroid of a ligand. | 2HT8 |
| 95 | Crystallography | Advanced | Visualizing disordered residues as gaps. | 1SNC |
| 96 | Cryo-EM | Advanced | Volume-slicing through a dense capsid map. | EMD-3342 |
| 97 | Drug Discovery | Advanced | Visualizing electrostatic repulsion in pockets. | 2CBA |
| 98 | Membranes | Advanced | Lipid bilayer self-assembly trajectory play. | Martini |
| 99 | Protein Eng. | Expert | Suggesting 'proline-kinks' for stability. | Helix |
| 100 | General | Expert | Final Synthesis: Canonical workflow on 8GI8. | 8GI8 |

---

## Integration and Multi-Step Operations Analysis

The complexity of these test cases ensures that the agent moves beyond being a command-wrapper and becomes a functional partner in structural research. For instance, the transition from Tier 1 (Basic) to Tier 3 (Advanced) involves moving from merely loading a map to "carving" it based on ligand proximity—a multi-step operation that involves `isomesh`, `isodot`, and boolean selection logic. Similarly, the integration with external tools like APBS or Rosetta (Tier 4) requires the agent to handle file I/O and external process monitoring through the PyMOL API.

By mastering these 100 cases, the AI agent will be able to perform autonomous comparative analysis of Channelrhodopsins (like HcKCR1 vs. ChRmine), identifying how specific aromatic residues at the extracellular side inhibit bulky hydrated ions—a mechanism that differs from canonical tetrameric filters. This high-level synthesis is the ultimate goal of the curriculum: enabling an AI to not only visualize structure but to interpret the physics and evolution behind it.
