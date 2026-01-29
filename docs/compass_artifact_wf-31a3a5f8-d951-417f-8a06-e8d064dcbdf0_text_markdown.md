# PyMOL Agent Curriculum: 85 Test Cases for Structural Biology Mastery

An AI agent learning to control PyMOL through a socket connection needs progressive exposure to increasingly complex structural biology tasks. This curriculum provides **85 test cases** organized into four difficulty tiers and eight domains, designed to build foundational skills before advancing to expert-level workflows.

## Curriculum architecture and progression

The curriculum follows a skill-tree design where earlier tasks build capabilities required for later ones. **Basic tasks** (1-20) establish core command fluency; **Intermediate tasks** (21-45) introduce domain-specific analysis; **Advanced tasks** (46-70) combine multiple workflows; **Expert tasks** (71-85) require creative problem-solving and multi-tool integration. Each tier assumes mastery of previous tiers.

Tasks are distributed across eight domains: **Core Visualization** (foundation for all others), **Crystallography**, **Cryo-EM**, **Protein Engineering**, **Drug Discovery**, **Membrane Proteins**, **Antibody/Immunology**, and **Publication Figures**. Domain-specific skills often transfer—binding site analysis in drug discovery uses the same selection syntax as epitope mapping in immunology.

---

## Tier 1: Basic (20 tasks)

### Domain: Core visualization fundamentals

**Task 1: Fetch and display a protein structure**
- *Description*: "Load the structure of human ubiquitin (PDB 1UBQ) and display it as a cartoon representation with the default coloring."
- *Required operations*: `fetch 1UBQ`, `show cartoon`
- *Success criteria*: Structure loads without errors; cartoon representation visible with rainbow coloring by chain
- *Failure modes*: Network timeout on fetch; forgetting to hide default line representation
- *PDB*: 1UBQ

**Task 2: Change representation types**
- *Description*: "Display lysozyme (PDB 2LYZ) showing the backbone as cartoon and all side chains as sticks."
- *Required operations*: `fetch 2LYZ`, `hide all`, `show cartoon`, `show sticks, sidechain`
- *Success criteria*: Cartoon backbone visible; all side chains displayed as sticks; no overlapping lines representation
- *Failure modes*: Using wrong selection syntax; showing sticks on entire protein including backbone
- *PDB*: 2LYZ

**Task 3: Apply custom coloring by chain**
- *Description*: "Load hemoglobin (PDB 1HHO) and color each chain a different color: chain A blue, chain B green, chain C yellow, chain D red."
- *Required operations*: `fetch 1HHO`, `color blue, chain A`, `color green, chain B`, etc.
- *Success criteria*: Four distinct chain colors visible; heme groups remain default color
- *Failure modes*: Misspelling chain identifiers; coloring entire object instead of chains
- *PDB*: 1HHO

**Task 4: Create and use selections**
- *Description*: "In the KcsA potassium channel (PDB 1BL8), select the selectivity filter residues 75-79 from all four chains and color them magenta."
- *Required operations*: `fetch 1BL8`, `select sf, resi 75-79`, `color magenta, sf`
- *Success criteria*: Selection contains exactly 20 residues (5 residues × 4 chains); selectivity filter highlighted
- *Failure modes*: Incorrect residue range; forgetting that selection applies to all chains
- *PDB*: 1BL8

**Task 5: Zoom and orient on a region of interest**
- *Description*: "Focus the view on the active site of trypsin (PDB 1TRN) centered on the catalytic triad residues His57, Asp102, and Ser195."
- *Required operations*: `fetch 1TRN`, `select cat_triad, resi 57+102+195`, `zoom cat_triad`, `show sticks, cat_triad`
- *Success criteria*: Catalytic triad fills viewport; three residues clearly visible as sticks
- *Failure modes*: Using wrong residue numbers; forgetting the `+` syntax for non-consecutive residues
- *PDB*: 1TRN

**Task 6: Measure a distance between atoms**
- *Description*: "Measure the distance between the catalytic serine OG atom and histidine NE2 atom in chymotrypsin (PDB 4CHA)."
- *Required operations*: `fetch 4CHA`, `distance d1, /4CHA//A/SER\`195/OG, /4CHA//A/HIS\`57/NE2`
- *Success criteria*: Distance measurement displays ~2.8-3.2 Å; dashed line connects atoms
- *Failure modes*: Incorrect atom naming; using residue selection instead of atom selection
- *PDB*: 4CHA

**Task 7: Remove water molecules and ligands**
- *Description*: "Clean up the HIV protease structure (PDB 1HSG) by removing all water molecules while keeping the inhibitor."
- *Required operations*: `fetch 1HSG`, `remove solvent`
- *Success criteria*: Water molecules removed; MVX inhibitor retained; protein structure intact
- *Failure modes*: Using `remove HOH` instead of `remove solvent`; accidentally removing the ligand with `remove het`
- *PDB*: 1HSG

**Task 8: Select binding site residues around a ligand**
- *Description*: "Identify and highlight all residues within 5Å of the ligand in the A2A adenosine receptor structure (PDB 4EIY)."
- *Required operations*: `fetch 4EIY`, `select lig, organic`, `select binding_site, byres polymer within 5 of lig`, `show sticks, binding_site`
- *Success criteria*: Selection contains **18-25 residues** surrounding the ZMA ligand; complete residues selected (not just atoms)
- *Failure modes*: Forgetting `byres` (selects only atoms, not complete residues); wrong distance cutoff
- *PDB*: 4EIY

**Task 9: Color by secondary structure**
- *Description*: "Display myoglobin (PDB 1MBN) colored by secondary structure: helices in red, sheets in yellow, loops in green."
- *Required operations*: `fetch 1MBN`, `color red, ss H`, `color yellow, ss S`, `color green, ss L+''`
- *Success criteria*: Eight alpha helices colored red; any coil regions green; heme group unaffected
- *Failure modes*: Using wrong secondary structure codes; forgetting empty string for unassigned regions
- *PDB*: 1MBN

**Task 10: Save a session and export an image**
- *Description*: "Create a publication-ready PNG image of GFP (PDB 1GFL) at 300 DPI with a white background."
- *Required operations*: `fetch 1GFL`, `bg_color white`, `ray 2400, 2400`, `png gfp_figure.png, dpi=300`
- *Success criteria*: PNG file created; white background; ray-traced quality; appropriate file size (~2-5 MB)
- *Failure modes*: Forgetting `ray` command before `png`; incorrect resolution calculation
- *PDB*: 1GFL

**Task 11: Show and customize surface representation**
- *Description*: "Display the molecular surface of lysozyme (PDB 2LYZ) with 50% transparency so the cartoon is visible underneath."
- *Required operations*: `fetch 2LYZ`, `show surface`, `show cartoon`, `set surface_transparency, 0.5`
- *Success criteria*: Surface and cartoon both visible; transparency correctly applied
- *Failure modes*: Setting transparency before showing surface; using wrong parameter name
- *PDB*: 2LYZ

**Task 12: Identify and display hydrogen bonds**
- *Description*: "Find and display all polar contacts between the ligand and protein in the factor Xa inhibitor complex (PDB 1FJS)."
- *Required operations*: `fetch 1FJS`, `select lig, organic`, `distance hbonds, lig, polymer, mode=2`
- *Success criteria*: **3-5 hydrogen bonds** displayed as dashed yellow lines; distances labeled
- *Failure modes*: Using `mode=0` (default distance); missing the mode parameter
- *PDB*: 1FJS

**Task 13: Align two related structures**
- *Description*: "Superimpose apo calmodulin (PDB 1CLL) onto calcium-bound calmodulin (PDB 1CDL) and report the RMSD."
- *Required operations*: `fetch 1CLL 1CDL, async=0`, `align 1CLL, 1CDL`
- *Success criteria*: RMSD reported in console (~2-4 Å expected due to conformational change); structures overlaid
- *Failure modes*: Confusing mobile/target order; not using `async=0` for sequential fetching
- *PDB*: 1CLL, 1CDL

**Task 14: Extract a chain to a new object**
- *Description*: "Extract chain B from the hemoglobin tetramer (PDB 1HHO) as a separate object named 'beta_subunit'."
- *Required operations*: `fetch 1HHO`, `extract beta_subunit, chain B`
- *Success criteria*: New object 'beta_subunit' appears in object list; chain B removed from original object
- *Failure modes*: Using `create` instead of `extract` (leaves copy in original); case sensitivity in chain ID
- *PDB*: 1HHO

**Task 15: Label residues in the active site**
- *Description*: "Add labels showing residue name and number for all residues within 4Å of the heme in cytochrome c (PDB 1HRC)."
- *Required operations*: `fetch 1HRC`, `select heme_env, byres polymer within 4 of resn HEM`, `label heme_env and name CA, "%s%s" % (resn, resi)`
- *Success criteria*: Labels appear at CA positions; format like "His18", "Met80"
- *Failure modes*: Labeling all atoms instead of just CA; wrong string formatting syntax
- *PDB*: 1HRC

**Task 16: Color by B-factor (temperature factor)**
- *Description*: "Visualize the flexibility of adenylate kinase (PDB 1AKE) by coloring from blue (rigid) to red (flexible) based on B-factors."
- *Required operations*: `fetch 1AKE`, `spectrum b, blue_white_red, minimum=10, maximum=80`
- *Success criteria*: Core regions blue; lid domain and mobile loops red; gradient visible
- *Failure modes*: Not setting min/max values (auto-scaling obscures patterns); wrong color order
- *PDB*: 1AKE

**Task 17: Show disulfide bonds**
- *Description*: "Highlight all disulfide bonds in ribonuclease A (PDB 7RSA) by showing them as yellow sticks."
- *Required operations*: `fetch 7RSA`, `select disulfides, (cys/sg and bound_to cys/sg)`, `show sticks, disulfides`, `color yellow, disulfides`
- *Success criteria*: **4 disulfide bonds** highlighted (Cys26-84, 40-95, 58-110, 65-72)
- *Failure modes*: Wrong selection syntax for bonded atoms; missing some disulfides
- *PDB*: 7RSA

**Task 18: Navigate using the sequence viewer**
- *Description*: "Enable the sequence viewer for insulin (PDB 2INS) and select the A-chain by clicking in the sequence."
- *Required operations*: `fetch 2INS`, `set seq_view, 1`, then select via GUI sequence bar
- *Success criteria*: Sequence bar appears; clicking selects corresponding residues in 3D view
- *Failure modes*: Sequence viewer not enabled; confusion between chains
- *PDB*: 2INS

**Task 19: Create a simple rotation movie**
- *Description*: "Generate a 360-degree rotation movie of GFP (PDB 1GFL) with 120 frames."
- *Required operations*: `fetch 1GFL`, `mset 1 x120`, `util.mroll(1, 120, 1)`, `mplay`
- *Success criteria*: Smooth 360° rotation; movie plays in viewport
- *Failure modes*: Wrong frame count in mset; not using util.mroll correctly
- *PDB*: 1GFL

**Task 20: Save a cleaned structure to PDB file**
- *Description*: "Save the protein-only portion of the thrombin-inhibitor complex (PDB 1PPB) to a new PDB file, excluding waters and ligands."
- *Required operations*: `fetch 1PPB`, `remove solvent`, `remove organic`, `save thrombin_clean.pdb, polymer`
- *Success criteria*: Output file contains only protein atoms; ATOM records present; no HETATM for waters/ligands
- *Failure modes*: Not specifying selection in save command; keeping unwanted molecules
- *PDB*: 1PPB

---

## Tier 2: Intermediate (25 tasks)

### Domain: Crystallography

**Task 21: Visualize electron density maps**
- *Description*: "Load the 2Fo-Fc and Fo-Fc electron density maps for the A2A receptor (PDB 4EIY) and display the ligand density at 1.0σ and difference density at ±3.0σ."
- *Required operations*: `fetch 4EIY`, `fetch 4EIY, type=2fofc, 2fofc`, `fetch 4EIY, type=fofc, fofc`, `isomesh mesh2fo, 2fofc, 1.0, organic, carve=2.0`, `isomesh meshfo_pos, fofc, 3.0, organic, carve=2.0`, `isomesh meshfo_neg, fofc, -3.0, organic, carve=2.0`
- *Success criteria*: Blue mesh around ligand (2Fo-Fc); green positive and red negative difference peaks
- *Failure modes*: Forgetting carve parameter (entire map renders, crashing PyMOL); wrong sigma levels
- *PDB*: 4EIY

**Task 22: Generate symmetry mates for crystal packing analysis**
- *Description*: "Generate all symmetry-related molecules within 5Å of ubiquitin (PDB 1UBQ) to analyze crystal contacts."
- *Required operations*: `fetch 1UBQ`, `symexp sym, 1UBQ, (1UBQ), 5`, `util.color_objs("(sym*)")`
- *Success criteria*: Multiple symmetry copies generated; different colors distinguish copies; crystal contacts visible
- *Failure modes*: Structure lacks CRYST1 record; distance too large crashes PyMOL
- *PDB*: 1UBQ

**Task 23: Color structure by resolution-dependent B-factors**
- *Description*: "Compare B-factor distributions between a high-resolution (PDB 1ETN, 0.54Å) and medium-resolution structure (PDB 3B5D, 2.5Å) of aldose reductase."
- *Required operations*: `fetch 1ETN 3B5D, async=0`, `spectrum b, blue_red, 1ETN, minimum=5, maximum=40`, `spectrum b, blue_red, 3B5D, minimum=15, maximum=80`
- *Success criteria*: High-resolution structure shows tighter B-factor range; patterns comparable despite different scales
- *Failure modes*: Using same min/max for both (obscures high-res detail)
- *PDB*: 1ETN, 3B5D

### Domain: Cryo-EM

**Task 24: Load and visualize cryo-EM density**
- *Description*: "Fetch the 3.4Å cryo-EM map of the 80S ribosome (EMDB-2660) and display it at the recommended contour level."
- *Required operations*: `fetch emd-2660`, `isomesh rib_mesh, emd-2660, 0.02, carve=50`, or `volume rib_vol, emd-2660`
- *Success criteria*: Ribosome density visible; both 40S and 60S subunits distinguishable
- *Failure modes*: Wrong contour level (too high = nothing visible, too low = noise); memory issues
- *PDB*: EMDB-2660

**Task 25: Split and visualize a large viral assembly**
- *Description*: "Load the Zika virus capsid (PDB 5IRE) and split it into individual subunits for selective display."
- *Required operations*: `fetch 5IRE, type=pdb1`, `split_states 5IRE, prefix=Zika`, `delete 5IRE`
- *Success criteria*: 60 individual objects created; each can be shown/hidden independently
- *Failure modes*: Memory exhaustion; not using type=pdb1 for biological assembly
- *PDB*: 5IRE

**Task 26: Compare conformational states from cryo-EM**
- *Description*: "Align and morph between open (PDB 5WJ9) and closed (PDB 5WJ5) states of the TRPML1 channel."
- *Required operations*: `fetch 5WJ5 5WJ9, async=0`, `align 5WJ9, 5WJ5`, `morph trpml_morph, 5WJ5, 5WJ9, refinement=3`
- *Success criteria*: Smooth morph between states; channel pore opening/closing visible
- *Failure modes*: Alignment failure due to chain differences; morph requires licensed PyMOL
- *PDB*: 5WJ5, 5WJ9

### Domain: Protein engineering

**Task 27: Introduce a point mutation using the mutagenesis wizard**
- *Description*: "In T4 lysozyme (PDB 2LZM), mutate Leu99 to alanine and select a rotamer with no steric clashes."
- *Required operations*: `fetch 2LZM`, Wizard → Mutagenesis → click L99 → select ALA → Apply
- *Success criteria*: Mutation applied; no red clash indicators; structure saves correctly
- *Failure modes*: Residue has alternate conformations; movie running during mutagenesis
- *PDB*: 2LZM

**Task 28: Visualize electrostatic surface potential**
- *Description*: "Calculate and display the electrostatic potential surface of barnase (PDB 1BRS) using APBS at ±5 kT/e."
- *Required operations*: `fetch 1BRS`, Plugin → APBS Electrostatics → Run, adjust ramp to ±5
- *Success criteria*: Surface shows blue (positive) and red (negative) regions; active site shows appropriate charge distribution
- *Failure modes*: Missing atoms cause pdb2pqr failure; wrong contour levels
- *PDB*: 1BRS

**Task 29: Design and visualize a potential disulfide bond**
- *Description*: "Identify residue pairs in GFP (PDB 1GFL) with Cβ-Cβ distance of 3.5-4.5Å suitable for disulfide engineering."
- *Required operations*: `fetch 1GFL`, iterate through CB pairs, `distance` measurements, identify candidates
- *Success criteria*: At least 2-3 candidate pairs identified; distances within range; no buried hydrophobic pairs
- *Failure modes*: Glycines have no CB; buried disulfides destabilize proteins
- *PDB*: 1GFL

**Task 30: Compare wild-type and mutant structures**
- *Description*: "Align wild-type p53 DNA-binding domain (PDB 2AC0) with the cancer-associated R248Q mutant (PDB 2BIM) and highlight the mutation site."
- *Required operations*: `fetch 2AC0 2BIM, async=0`, `align 2BIM, 2AC0`, `select mut_site, resi 248`, `show spheres, mut_site`
- *Success criteria*: RMSD ~0.5-1.5Å; position 248 clearly shows Arg→Gln change
- *Failure modes*: Chain ID mismatches; mutant may have different numbering
- *PDB*: 2AC0, 2BIM

### Domain: Drug discovery

**Task 31: Analyze binding pocket shape and volume**
- *Description*: "Visualize the binding pocket of CDK2 (PDB 1HCK) using cavity detection mode and estimate pocket depth."
- *Required operations*: `fetch 1HCK`, `remove solvent`, `set surface_cavity_mode, 1`, `show surface`
- *Success criteria*: ATP binding pocket clearly visible as cavity; pocket entrance and depth distinguishable
- *Failure modes*: Ligand still present fills cavity; wrong surface mode
- *PDB*: 1HCK

**Task 32: Visualize multiple docking poses**
- *Description*: "Load 5 docking poses for a kinase inhibitor and align them to show pose variability."
- *Required operations*: Load multiple SDF files, `align` each to protein, `show sticks` for all poses, color differently
- *Success criteria*: All poses visible in binding site; conformational differences apparent
- *Failure modes*: Poses not aligned; overlapping makes individual poses indistinguishable
- *PDB*: 3IG7 (CDK2 with inhibitor)

**Task 33: Map pharmacophore features in a binding site**
- *Description*: "Identify and color H-bond donors (blue), acceptors (red), and hydrophobic groups (yellow) in the oseltamivir binding site of neuraminidase (PDB 2HT8)."
- *Required operations*: `fetch 2HT8`, select donor/acceptor atoms by element and neighbor criteria, color by feature type
- *Success criteria*: Three distinct pharmacophore feature colors; ligand features match protein complementarity
- *Failure modes*: Incorrect donor/acceptor chemistry assignment
- *PDB*: 2HT8

**Task 34: Calculate and display protein-ligand interaction fingerprint**
- *Description*: "Identify all interaction types (H-bonds, hydrophobic contacts, π-stacking) between vemurafenib and BRAF V600E (PDB 3OG7)."
- *Required operations*: `fetch 3OG7`, `h_add`, create selections for each interaction type, `distance` for H-bonds, visual identification of contacts
- *Success criteria*: **5+ H-bonds** identified; hydrophobic interactions with gatekeeper residue visible
- *Failure modes*: Missing hydrogens; π-stacking requires manual identification
- *PDB*: 3OG7

### Domain: Membrane proteins

**Task 35: Position a membrane protein in the bilayer**
- *Description*: "Load the OPM-oriented structure of bacteriorhodopsin and visualize the membrane boundaries."
- *Required operations*: Download from OPM (opm.phar.umich.edu), `load 1c3w_opm.pdb`, select DUM atoms, `show spheres`
- *Success criteria*: Membrane boundary planes visible; TM helices span between planes
- *Failure modes*: Using standard PDB (lacks membrane orientation); DUM atoms not recognized
- *PDB*: 1C3W

**Task 36: Visualize an ion channel pore**
- *Description*: "Display the pore of the Kir2.2 channel (PDB 3SPI) with the selectivity filter residues highlighted and potassium ions visible."
- *Required operations*: `fetch 3SPI`, `show surface, polymer`, `select sf, resi 142-146`, `show sticks, sf`, `show spheres, elem K`
- *Success criteria*: Pore visible along channel axis; K+ ions visible in selectivity filter
- *Failure modes*: Wrong residue numbers; K atoms in wrong format
- *PDB*: 3SPI

**Task 37: Analyze GPCR transmembrane helix arrangement**
- *Description*: "Color the seven transmembrane helices of the β2-adrenergic receptor (PDB 2RH1) with different colors and label each TM."
- *Required operations*: `fetch 2RH1`, color TM1-TM7 with distinct colors based on residue ranges (29-60, 67-96, etc.)
- *Success criteria*: Seven distinct TM colors; canonical GPCR fold visible from extracellular view
- *Failure modes*: Incorrect TM boundaries; missing loop regions
- *PDB*: 2RH1

### Domain: Antibody/Immunology

**Task 38: Identify and color CDR loops**
- *Description*: "Highlight all six CDR loops of the Fab fragment from cetuximab (PDB 1YY8) using Kabat numbering."
- *Required operations*: `fetch 1YY8`, select CDR-L1/L2/L3 and CDR-H1/H2/H3 using Kabat residue ranges, color each distinctly
- *Success criteria*: Six colored loops visible at antibody tip; heavy and light chain CDRs distinguishable
- *Failure modes*: Wrong numbering scheme; chain ID confusion (H vs L)
- *PDB*: 1YY8

**Task 39: Analyze an antibody-antigen interface**
- *Description*: "Identify all interface residues between the Fab and IL-1β in the gevokizumab complex (PDB 4G6M) and calculate buried surface area."
- *Required operations*: `fetch 4G6M`, `select interface_ab, (chain H+L) within 4 of chain B`, `select interface_ag, chain B within 4 of (chain H+L)`, calculate areas
- *Success criteria*: Interface residues identified on both partners; ~1500-2000 Å² buried surface
- *Failure modes*: Missing one side of interface; not using `byres` for complete residues
- *PDB*: 4G6M

**Task 40: Map an epitope onto antigen surface**
- *Description*: "Color the epitope residues on EGFR (from structure 8HGO) as identified by alanine scanning mutagenesis."
- *Required operations*: `fetch 8HGO`, `show surface, chain A`, `select epitope, chain A and resi [epitope_list]`, `set surface_color, red, epitope`
- *Success criteria*: Epitope appears as red patch on otherwise white surface; footprint size appropriate
- *Failure modes*: Surface color not applying to selection; wrong residue list
- *PDB*: 8HGO

### Domain: External tool integration

**Task 41: Color by AlphaFold pLDDT confidence**
- *Description*: "Load an AlphaFold prediction and color it by pLDDT confidence using the official color scheme (dark blue >90, light blue 70-90, yellow 50-70, orange <50)."
- *Required operations*: Load AlphaFold PDB, `set_color` for four confidence colors, `color` based on b-factor ranges
- *Success criteria*: Well-ordered regions dark blue; disordered termini orange/yellow
- *Failure modes*: pLDDT stored in B-factor column; color scale reversed
- *PDB*: Any AlphaFold DB entry (e.g., AF-P0A799-F1)

**Task 42: Superimpose AlphaFold prediction onto experimental structure**
- *Description*: "Compare the AlphaFold prediction of E. coli DHFR with the experimental structure (PDB 1RX2) and report RMSD."
- *Required operations*: `fetch 1RX2`, load AF prediction, `align af_model, 1RX2`
- *Success criteria*: RMSD <1.5Å for well-ordered regions; flexible loops show larger deviations
- *Failure modes*: Numbering mismatches; alignment failures in low-confidence regions
- *PDB*: 1RX2

**Task 43: Load and animate a molecular dynamics trajectory**
- *Description*: "Load a GROMACS trajectory of ubiquitin and create a smoothed animation."
- *Required operations*: `load ubq.gro`, `load_traj ubq.xtc`, `smooth object, window=5`, `mset 1-100`, `mplay`
- *Success criteria*: Trajectory plays smoothly; protein dynamics visible; no jerky motion
- *Failure modes*: Atom count mismatch between topology and trajectory; memory issues
- *PDB*: 1UBQ (with external trajectory files)

**Task 44: Perform batch processing of multiple structures**
- *Description*: "Load all kinase structures from a family (1ATP, 1HCK, 1QMZ), align them, and export cleaned versions."
- *Required operations*: Fetch multiple PDBs, `alignto` reference, process each with `remove solvent`, `save`
- *Success criteria*: All structures aligned; RMSD values reported; cleaned files saved
- *Failure modes*: async timing issues; different chain IDs across structures
- *PDB*: 1ATP, 1HCK, 1QMZ

**Task 45: Visualize sequence conservation on structure**
- *Description*: "Color the structure of a SH2 domain by conservation scores from a ConSurf analysis."
- *Required operations*: Load ConSurf output PDB, `spectrum b, blue_white_magenta, minimum=1, maximum=9`
- *Success criteria*: Conserved regions (binding site) in magenta; variable regions in blue
- *Failure modes*: Conservation in wrong B-factor column; color scale interpretation
- *PDB*: 1SHC with ConSurf annotation

---

## Tier 3: Advanced (25 tasks)

### Domain: Complex crystallography workflows

**Task 46: Validate model quality against density**
- *Description*: "Identify poorly-fit regions in a refinement by finding residues where the model doesn't match the 2Fo-Fc density at 1.0σ."
- *Required operations*: Load structure and maps, carve density around each residue, visual inspection for breaks in density
- *Success criteria*: Identify 3-5 residues with poor density fit; suggest alternative rotamers
- *Failure modes*: Too strict sigma level; confusing map quality with model quality
- *PDB*: 4EIY

**Task 47: Build missing loops from density**
- *Description*: "Visualize the density for a disordered loop (residues 50-60) in a medium-resolution structure and assess whether it can be built."
- *Required operations*: Carve Fo-Fc map at ±2.5σ around gap region, look for continuous density
- *Success criteria*: Report whether density is continuous enough for building; identify visible residues
- *Failure modes*: Looking at 2Fo-Fc instead of Fo-Fc; wrong sigma level
- *PDB*: Structure with missing loop

**Task 48: Analyze anisotropic B-factors**
- *Description*: "Display anisotropic displacement ellipsoids for a sub-angstrom resolution structure."
- *Required operations*: `fetch 1ETN`, `show ellipsoids` (requires anisotropic data in PDB)
- *Success criteria*: Thermal ellipsoids visible; elongated ellipsoids indicate motion direction
- *Failure modes*: Structure lacks ANISOU records; ellipsoid display settings
- *PDB*: 1ETN (0.54Å resolution)

### Domain: Advanced cryo-EM analysis

**Task 49: Fit atomic model into cryo-EM density**
- *Description*: "Load the spike protein trimer (PDB 6VYB) and its associated EM map, verify the fit quality."
- *Required operations*: Fetch structure and EMDB map, `isomesh` around model, assess density-model agreement
- *Success criteria*: Model fits within density; no major density outside model
- *Failure modes*: Map/model misalignment; wrong contour level
- *PDB*: 6VYB, EMDB-21375

**Task 50: Visualize local resolution variation**
- *Description*: "Load a local resolution map and color the atomic model by local resolution values."
- *Required operations*: Load local resolution map, sample values onto model atoms, `spectrum` coloring
- *Success criteria*: Core regions show higher resolution; peripheral regions lower
- *Failure modes*: Local resolution map format issues; mapping values to atoms
- *PDB*: Any recent cryo-EM structure with local resolution

**Task 51: Analyze heterogeneity in cryo-EM data**
- *Description*: "Load multiple conformational states of the ribosome from 3D classification and compare them."
- *Required operations*: Load multiple states, align, measure distances between moving parts, create morph
- *Success criteria*: Conformational differences quantified; ratcheting motion visualized
- *Failure modes*: States not properly aligned; scale differences
- *PDB*: Multiple ribosome states

### Domain: Advanced protein engineering

**Task 52: Analyze a protein interface for hotspot mutations**
- *Description*: "Identify potential hotspot residues at the interface of IL-2 and IL-2Rα (PDB 1Z92) that could be mutated to enhance binding."
- *Required operations*: Select interface residues, identify aromatic/charged clusters, measure H-bond networks
- *Success criteria*: Identify **3-5 hotspot candidates** (Trp, Tyr, Arg clusters); calculate buried surface
- *Failure modes*: Missing key interactions; focusing on peripheral residues
- *PDB*: 1Z92

**Task 53: Design a circular permutation**
- *Description*: "Visualize the termini of GFP (PDB 1GFL) and identify positions suitable for circular permutation that wouldn't disrupt the barrel."
- *Required operations*: Identify N/C-termini, find loops suitable for new termini, assess distance to chromophore
- *Success criteria*: 2-3 candidate loop sites identified; distance from chromophore >10Å
- *Failure modes*: Selecting positions that would disrupt β-barrel; proximity to active site
- *PDB*: 1GFL

**Task 54: Compare electrostatics of homologs with different pI**
- *Description*: "Calculate and compare electrostatic surfaces of acidic (low pI) and basic (high pI) variants of a protein family."
- *Required operations*: APBS on multiple homologs, consistent color scale, side-by-side comparison
- *Success criteria*: Clear charge distribution differences; pI differences rationalized by surface
- *Failure modes*: Different pH settings; inconsistent contour levels
- *PDB*: Protein family with pI variation

### Domain: Advanced drug discovery

**Task 55: Perform ensemble docking visualization**
- *Description*: "Compare binding poses across an NMR ensemble of 20 conformers to identify consistent and variable interactions."
- *Required operations*: Load ensemble, dock to each, overlay poses, identify conserved H-bonds
- *Success criteria*: Consensus interactions identified; pose variability quantified
- *Failure modes*: Too many conformers overwhelms visualization; losing track of which pose is which
- *PDB*: NMR ensemble structure

**Task 56: Analyze water molecules in binding site**
- *Description*: "Identify conserved water molecules in the binding site of HIV protease across multiple structures."
- *Required operations*: Align 5+ HIV protease structures, identify water positions that superimpose
- *Success criteria*: 2-3 conserved waters identified; structural/bridging role apparent
- *Failure modes*: Waters not conserved in naming; small coordinate variations
- *PDB*: 1HSG, 1HVR, 1QBR, 3NU3, 4HVP

**Task 57: Create a pharmacophore model from bound ligand**
- *Description*: "Extract pharmacophore features (HBD, HBA, hydrophobic, aromatic) from the co-crystallized inhibitor of EGFR kinase (PDB 1M17)."
- *Required operations*: Identify feature atoms, create pseudoatoms at feature positions, visualize as spheres
- *Success criteria*: 5-7 pharmacophore points defined; distances between points measured
- *Failure modes*: Missing features; incorrect atom classifications
- *PDB*: 1M17

### Domain: Membrane protein analysis

**Task 58: Analyze lipid binding sites**
- *Description*: "Identify and visualize annular lipid binding sites around a GPCR (PDB 4EIY) using molecular surface analysis."
- *Required operations*: Load OPM-oriented structure, create surface at membrane boundary height, identify grooves
- *Success criteria*: Lipid-exposed grooves between TM helices identified
- *Failure modes*: Wrong membrane position; missing lipid binding features
- *PDB*: 4EIY

**Task 59: Map ion permeation pathway**
- *Description*: "Trace the ion permeation pathway through the voltage-gated sodium channel NavAb (PDB 3RVY) from extracellular to intracellular side."
- *Required operations*: Align channel along z-axis, create series of cavity selections, visualize pathway
- *Success criteria*: Complete pathway from selectivity filter to cytoplasm; constriction points identified
- *Failure modes*: Side fenestrations confused with main pore; orientation issues
- *PDB*: 3RVY

**Task 60: Compare active and inactive GPCR states**
- *Description*: "Align inactive (PDB 2RH1) and active (PDB 3SN6) β2AR structures and measure TM6 outward movement."
- *Required operations*: Align on TM3 (stable), measure TM6 cytoplasmic displacement
- *Success criteria*: TM6 movement of **10-14Å** measured; G-protein binding site opening visible
- *Failure modes*: Wrong alignment reference; including G-protein in alignment
- *PDB*: 2RH1, 3SN6

### Domain: Advanced antibody analysis

**Task 61: Analyze CDR loop conformations (canonical classes)**
- *Description*: "Classify the CDR-L1 loop of trastuzumab (PDB 1N8Z) into its canonical class based on length and key residues."
- *Required operations*: Identify loop length, key positions, compare to canonical structures
- *Success criteria*: Correct canonical class assignment; supporting residues identified
- *Failure modes*: Wrong numbering scheme; missing key positions
- *PDB*: 1N8Z

**Task 62: Compare paratope shapes across antibody family**
- *Description*: "Align multiple anti-lysozyme antibodies and compare their paratope surface shapes."
- *Required operations*: Align on Fab framework, show surface at CDRs only, compare shapes
- *Success criteria*: Paratope shape variations visible; epitope complementarity apparent
- *Failure modes*: Framework alignment includes CDRs; surface artifacts
- *PDB*: 1FDL, 1MLC, 1DQJ

**Task 63: Design CDR grafting visualization**
- *Description*: "Visualize the CDR grafting of mouse CDRs onto a human framework, highlighting positions requiring back-mutations."
- *Required operations*: Color CDRs vs framework differently, identify Vernier zone residues
- *Success criteria*: CDR/framework boundary clear; key Vernier residues labeled
- *Failure modes*: Missing Vernier zone residues; framework selection too broad
- *PDB*: Humanized antibody

### Domain: Publication figure workflows

**Task 64: Create a multi-panel structure comparison figure**
- *Description*: "Generate a 2x2 panel figure showing four kinase structures in identical orientations with consistent coloring."
- *Required operations*: Align all structures, store view, apply to each, `set grid_mode, 1`, ray
- *Success criteria*: All four panels at identical orientation; consistent color scheme; publication resolution
- *Failure modes*: View drift between panels; inconsistent lighting
- *PDB*: 1ATP, 1HCK, 1QMZ, 2PHK

**Task 65: Create a morph movie between functional states**
- *Description*: "Generate a morph animation showing the conformational change in adenylate kinase between open (PDB 4AKE) and closed (PDB 1AKE) states."
- *Required operations*: `align`, `morph`, `mset`, ray-trace frames, export as GIF
- *Success criteria*: Smooth 60-frame morph; lid domain closure clearly visible; loopback animation
- *Failure modes*: Geometric distortions in morph; jerky interpolation
- *PDB*: 4AKE, 1AKE

**Task 66: Design a figure highlighting binding site interactions**
- *Description*: "Create a publication figure of the SARS-CoV-2 main protease (PDB 7BUY) with inhibitor showing all interactions, suitable for Nature."
- *Required operations*: Clean structure, optimal orientation, H-bonds, hydrophobic surface, labels, white background, ray at 300 DPI
- *Success criteria*: Figure meets Nature guidelines (180mm width, 300 DPI); colorblind-friendly; all key interactions labeled
- *Failure modes*: Busy figure; poor color choices; low resolution
- *PDB*: 7BUY

### Domain: Integration workflows

**Task 67: Map genetic variants onto protein structure**
- *Description*: "Load gnomAD variant data for BRCA1 BRCT domains (PDB 1T2V) and color by variant frequency and pathogenicity."
- *Required operations*: Load structure, add variant data to B-factors, spectrum coloring
- *Success criteria*: Pathogenic variants cluster in functional regions; benign variants on surface
- *Failure modes*: Variant mapping to wrong residues; numbering mismatches
- *PDB*: 1T2V

**Task 68: Compare predicted contacts with experimental structure**
- *Description*: "Overlay AlphaFold PAE-derived contact predictions with actual contacts in an experimental structure."
- *Required operations*: Calculate contact map from structure, compare with PAE, visualize discrepancies
- *Success criteria*: High PAE regions correlate with true contacts; discrepancies identified in flexible regions
- *Failure modes*: PAE interpretation; contact definition threshold
- *PDB*: Any protein with AlphaFold prediction

**Task 69: Prepare structure for RFdiffusion binder design**
- *Description*: "Trim and clean a target protein structure (EGFR, PDB 8HGO) for input to RFdiffusion, defining hotspot residues."
- *Required operations*: Remove waters, distant domains; identify hotspot residues; save minimal PDB; document contig specification
- *Success criteria*: Clean PDB <500 residues around epitope; hotspots defined in correct format; no orphan atoms
- *Failure modes*: Partial residues; losing critical context; wrong hotspot format
- *PDB*: 8HGO

**Task 70: Validate a designed binder structure**
- *Description*: "Load a computationally designed binder from BindCraft and assess interface quality: contacts, buried surface, H-bonds."
- *Required operations*: Load binder-target complex, analyze interface using standard metrics
- *Success criteria*: >1000 Å² buried surface; 3+ H-bonds; no severe clashes
- *Failure modes*: Missing interface assessment metrics; incorrect selection of interface
- *PDB*: Designed binder structure

---

## Tier 4: Expert (15 tasks)

### Domain: Complex multi-step workflows

**Task 71: Complete crystallographic validation workflow**
- *Description*: "Perform comprehensive model validation: check Ramachandran outliers, rotamer quality, clashes, and density fit. Generate validation report."
- *Required operations*: Calculate all geometry metrics, identify outliers, visualize in context, assess density support
- *Success criteria*: All outliers identified and explained; correlation with resolution; validation report generated
- *Failure modes*: Missing validation categories; not considering resolution context
- *PDB*: 4EIY

**Task 72: Analyze symmetry-related crystal contacts affecting function**
- *Description*: "Determine whether a dimeric interface in the crystal (PDB 1XYZ) represents a biological dimer or crystal artifact using PISA criteria."
- *Required operations*: Generate symmetry mates, calculate buried surface, assess interface stability metrics
- *Success criteria*: Correct classification (biological vs artifact); supporting evidence documented
- *Failure modes*: Confusing ASU with biological unit; missing solvation energy calculation
- *PDB*: Ambiguous oligomeric state structure

**Task 73: Map cryo-EM flexibility to functional mechanism**
- *Description*: "Analyze local resolution variations in a molecular machine (spliceosome, ribosome) to identify flexible regions relevant to function."
- *Required operations*: Load local resolution map, identify low-resolution regions, correlate with functional states
- *Success criteria*: Flexible regions correlate with known mobile elements; mechanistic insight generated
- *Failure modes*: Confusing flexibility with disorder; missing mechanistic context
- *PDB*: Spliceosome or ribosome EM structure

### Domain: Agentic and literature-informed tasks

**Task 74: Identify functionally important residues from literature**
- *Description*: "For protein kinase A (PDB 1ATP), identify residues mentioned as catalytically important in literature and highlight them structurally."
- *Required operations*: Cross-reference literature residue lists, map to structure, visualize in active site context
- *Success criteria*: Catalytic lysine, DFG motif, activation loop correctly identified; literature citations documented
- *Failure modes*: Residue numbering differences across publications; missing key residues
- *PDB*: 1ATP

**Task 75: Suggest mutations to improve thermostability**
- *Description*: "Analyze the structure of mesophilic malate dehydrogenase and suggest 3-5 mutations to improve thermostability based on structural principles."
- *Required operations*: Identify flexible regions, surface charge optimization, helix capping, buried hydrophobic core enhancement
- *Success criteria*: Rationale provided for each suggestion; supported by thermostability principles; avoiding active site
- *Failure modes*: Suggestions near active site; ignoring protein engineering precedent
- *PDB*: Mesophilic enzyme structure

**Task 76: Compare homologous structures to identify selectivity determinants**
- *Description*: "Compare the Na+ channel NavAb (PDB 3RVY) with K+ channel KcsA (PDB 1BL8) to identify structural features determining ion selectivity."
- *Required operations*: Align selectivity filters, compare pore dimensions, identify DEKA vs TVGY selectivity filter residues
- *Success criteria*: Selectivity filter differences documented; pore size differences measured; selectivity mechanism explained
- *Failure modes*: Non-equivalent structural alignment; missing key selectivity features
- *PDB*: 3RVY, 1BL8

**Task 77: Generate hypothesis about unusual kinetics from structure**
- *Description*: "Examine the structure of a slow-cycling GTPase and propose structural explanations for its unusual kinetics."
- *Required operations*: Compare to fast GTPases, identify switch region differences, analyze active site geometry
- *Success criteria*: Testable structural hypothesis generated; comparison with fast homologs
- *Failure modes*: Generic explanations; missing kinetic-structural correlation
- *PDB*: Slow GTPase structure

### Domain: Adaptyv Bio competition-style challenges

**Task 78: Prepare target for de novo binder design**
- *Description*: "Following BenchBB protocols, prepare EGFR extracellular domain (PDB 8HGO) for binder design: clean, trim, define hotspots, specify contigs."
- *Required operations*: Remove artifacts, identify optimal epitope region, format for RFdiffusion/BindCraft input
- *Success criteria*: Output matches BenchBB format; hotspots in contact-accessible positions; ~500 residue context
- *Failure modes*: Wrong chain; including non-productive epitope region; formatting errors
- *PDB*: 8HGO

**Task 79: Analyze designed binder interface quality metrics**
- *Description*: "Calculate ipAE, iPTM-equivalent metrics, buried surface, H-bonds, and shape complementarity for an RFdiffusion binder."
- *Required operations*: Load predicted complex, calculate all interface metrics, compare to successful designs
- *Success criteria*: All metrics calculated correctly; comparison to BenchBB hit rates; pass/fail assessment
- *Failure modes*: Missing key metrics; wrong interpretation of scores
- *PDB*: Designed binder structure

**Task 80: Compare multiple design methods on same target**
- *Description*: "Visualize and compare binders generated by RFdiffusion, BindCraft, and AlphaProteo for the same target, assessing binding mode diversity."
- *Required operations*: Load all designs, align to target, assess epitope overlap, compare approaches
- *Success criteria*: Binding mode diversity quantified; method-specific patterns identified
- *Failure modes*: Designs not comparable (different targets); missing binding mode analysis
- *PDB*: Multiple designed binders for same target

### Domain: Complex analysis challenges

**Task 81: Comprehensive H-bond network analysis**
- *Description*: "Map the complete hydrogen bond network in the active site of a serine protease, including water-mediated bridges and compare across the protease family."
- *Required operations*: `h_add`, identify all H-bonds with proper geometry (distance <3.5Å, angle >120°), trace water bridges, compare 5+ family members
- *Success criteria*: Complete network mapped; conserved waters identified; catalytic H-bonds documented
- *Failure modes*: Missing water-mediated contacts; wrong angle criteria; incomplete family comparison
- *PDB*: 1TRN, 4CHA, 1PPB, 1SGT, 3TGI

**Task 82: Salt bridge network and pH-dependent behavior**
- *Description*: "Identify all salt bridges in a hemoglobin tetramer and predict which might break at low pH (Bohr effect)."
- *Required operations*: Identify all Asp/Glu...Lys/Arg/His pairs <4Å, focus on surface His residues, assess accessibility
- *Success criteria*: His-mediated salt bridges identified as pH-sensitive; correlation with known Bohr protons
- *Failure modes*: Missing interior salt bridges; wrong pKa assumptions
- *PDB*: 2HHB

**Task 83: Design allosteric mutation site**
- *Description*: "Identify a potential allosteric site in a kinase (PDB 1ATP) distant from the active site suitable for designing an allosteric inhibitor."
- *Required operations*: Map conserved cavities, identify communication pathways to active site, assess druggability
- *Success criteria*: Site identified >15Å from active site; communication pathway proposed; similar sites in literature
- *Failure modes*: Site too close to active site; no communication pathway rationale
- *PDB*: 1ATP

**Task 84: Multi-domain assembly visualization**
- *Description*: "Assemble and visualize a full antibody from Fab (PDB 1IGT) and Fc (PDB 1FC1) domains with appropriate hinge modeling."
- *Required operations*: Load domains, position using known geometry, model hinge flexibility, visualize full IgG
- *Success criteria*: Y-shaped IgG visible; hinge flexibility represented; scale accurate
- *Failure modes*: Wrong relative positioning; hinge geometry errors
- *PDB*: 1IGT, 1FC1

**Task 85: Complete pipeline: structure to publication figure**
- *Description*: "Starting from a PDB code, create a complete publication-ready figure package: main structure view, binding site detail, electrostatics panel, and comparison overlay - all at Nature specifications."
- *Required operations*: Complete workflow from fetch through APBS, multi-panel composition, consistent styling, 300 DPI export
- *Success criteria*: Four-panel figure; Nature-compliant dimensions and resolution; colorblind-safe; labeled
- *Failure modes*: Inconsistent styling; poor color choices; resolution issues; missing scale
- *PDB*: Any relevant structure

---

## Appendix A: PDB codes by task domain

| Domain | Easy/Reference | Medium Complexity | Challenging |
|--------|---------------|-------------------|-------------|
| **General** | 1UBQ, 2LYZ, 1MBN | 1HSG, 4EIY, 1AKE | 5IRE, 6VYB |
| **Crystallography** | 1UBQ, 4EIY | 1ETN (ultra-high res) | Multi-dataset |
| **Cryo-EM** | EMDB-2660 | 5WJ5/5WJ9, 6VYB | Ribosome assemblies |
| **Protein Engineering** | 2LZM, 1GFL | 1BRS, 2AC0 | Multi-mutant series |
| **Drug Discovery** | 1HSG, 1HCK | 3OG7, 2HT8 | 7BUY, 1M17 |
| **Membrane Proteins** | 1BL8, 2RH1 | 3SPI, 3RVY | 3SN6 (complex) |
| **Antibody** | 1YY8, 4G6M | 8HGO, 1N8Z | Multi-Fab comparison |
| **Binder Design** | 8HGO, 3DI3 | 4Z18, 2WH6 | De novo targets |

## Appendix B: Critical PyMOL settings for reproducibility

```python
# Standard initialization for test consistency
reinitialize
set hash_max, 300
set antialias, 2
set ray_trace_mode, 1
set ambient, 0.5
set surface_quality, 2
set cartoon_sampling, 14
bg_color white
```

## Appendix C: Success metrics by tier

| Tier | Expected Pass Rate | Time per Task | Key Assessment |
|------|-------------------|---------------|----------------|
| Basic | >95% | <5 minutes | Command accuracy |
| Intermediate | >80% | 5-15 minutes | Workflow completion |
| Advanced | >60% | 15-30 minutes | Result quality |
| Expert | >40% | 30-60 minutes | Insight generation |

---

## Curriculum implementation notes

**Progressive skill building**: Tasks reference skills from earlier tasks explicitly. Task 21 (electron density) requires Task 1 (fetch), Task 11 (surface), and Task 8 (selections). The agent should maintain a skill registry and recognize when prerequisite skills are incomplete.

**Self-play verification**: Each task includes explicit success criteria that can be verified programmatically where possible (RMSD values, residue counts, file sizes) or through visual inspection (correct representations, appropriate coloring). The agent should develop internal quality checks.

**Failure mode learning**: Common failures are documented so the agent can recognize and recover from typical errors. Self-play should include deliberate introduction of these failure modes to develop robustness.

**Domain transfer**: Skills transfer across domains—selection syntax used in drug discovery binding site analysis is identical to antibody epitope analysis. The curriculum explicitly reuses core operations across domains to reinforce generalization.

This curriculum provides comprehensive coverage of structural biology PyMOL workflows, from basic visualization through expert-level analysis, suitable for training an AI agent to assist structural biologists with their daily visualization and analysis needs.