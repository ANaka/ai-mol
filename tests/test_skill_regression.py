"""Agent SDK regression tests for claudemol skills.

These tests spawn real Claude Code sessions (Haiku model) and cost tokens.
They are excluded from default pytest runs — use `pytest -m slow` to run them.

Requires: claude-agent-sdk.
"""

import pytest

sdk = pytest.importorskip("claude_agent_sdk")

from conftest import REMOVED_UTILITIES, VALID_BRIDGE_COMMANDS, ask_agent  # noqa: E402


@pytest.mark.slow
class TestImageCapture:
    async def test_uses_native_pymol_commands(self, haiku_options):
        result = await ask_agent(
            "How do I capture a publication-quality image of a protein in PyMOL?",
            haiku_options,
        )
        result_lower = result.lower()

        # Must use native PyMOL commands (cmd.ray + cmd.png pattern)
        assert "cmd.ray" in result_lower, "Should reference cmd.ray() for rendering"
        assert "cmd.png" in result_lower, "Should reference cmd.png() for saving"

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"

        # Should NOT use the broken cmd.png(path, width, height) pattern
        assert "cmd.png(path, width, height)" not in result_lower or "never" in result_lower, (
            "Should not recommend cmd.png(path, width, height) — causes view corruption"
        )


@pytest.mark.slow
class TestBridgeCommands:
    async def test_only_valid_subcommands(self, haiku_options):
        result = await ask_agent(
            "List all the pymol-agent-bridge subcommands you would use and explain each one.",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference at least 2 valid subcommands
        found_valid = {cmd for cmd in VALID_BRIDGE_COMMANDS if cmd in result_lower}
        assert len(found_valid) >= 2, f"Expected at least 2 valid subcommands, got: {found_valid}"

        # Must NOT reference removed/invalid utilities
        removed = {"capture", "image", "screenshot", "view", "snap", "render"}
        for cmd in removed:
            assert f"pymol-agent-bridge {cmd}" not in result_lower, (
                f"Should not reference removed utility: pymol-agent-bridge {cmd}"
            )


@pytest.mark.slow
class TestConnectionFlow:
    async def test_correct_connection_steps(self, haiku_options):
        result = await ask_agent(
            "Walk me through connecting to PyMOL step by step.",
            haiku_options,
        )
        result_lower = result.lower()

        # Should reference status check or launch
        assert (
            "status" in result_lower or "launch" in result_lower
        ), "Should reference status check or launch"

        # Should use exec for sending commands
        assert "exec" in result_lower, "Should reference exec for sending commands"

        # Must NOT reference removed utilities
        for removed in [*REMOVED_UTILITIES, "pymol_view"]:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


# ---------------------------------------------------------------------------
# New regression tests — advice quality for specific skill domains
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestAntibodyVisualization:
    async def test_cdr_loop_advice(self, haiku_options):
        result = await ask_agent(
            "How do I visualize the CDR loops of an antibody in PyMOL? "
            "Show me the key commands.",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference selection commands for CDR loops
        assert "cmd.select" in result_lower or "select " in result_lower, (
            "Should reference selection commands for CDR loops"
        )

        # Must reference at least one CDR loop identifier
        cdr_refs = {"cdr", "h1", "h2", "h3", "l1", "l2", "l3"}
        found = {ref for ref in cdr_refs if ref in result_lower}
        assert len(found) >= 1, f"Should mention CDR loop identifiers, found: {found}"

        # Should reference coloring for distinction
        assert "color" in result_lower, "Should reference coloring CDR loops"

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestAlphaFoldValidation:
    async def test_validation_advice(self, haiku_options):
        result = await ask_agent(
            "How do I validate an AlphaFold prediction in PyMOL? "
            "What should I look at for confidence?",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference pLDDT confidence metric
        assert "plddt" in result_lower, "Should reference pLDDT confidence metric"

        # Must reference coloring by confidence (spectrum or B-factor)
        color_refs = {"cmd.spectrum", "b-factor", "b_factor", "bfactor"}
        found = {ref for ref in color_refs if ref in result_lower}
        assert len(found) >= 1, (
            f"Should reference confidence coloring (spectrum/B-factor), found: {found}"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestBindingSiteVisualization:
    async def test_binding_pocket_advice(self, haiku_options):
        result = await ask_agent(
            "How do I visualize a protein-ligand binding site in PyMOL? "
            "Show me how to highlight the pocket residues.",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference distance-based selection
        distance_refs = {"within", "around", "byres", "near_to"}
        found = {ref for ref in distance_refs if ref in result_lower}
        assert len(found) >= 1, (
            f"Should reference distance-based selection (within/around), found: {found}"
        )

        # Should reference stick or surface representation for pocket
        repr_refs = {"sticks", "stick", "surface", "cmd.show"}
        found_repr = {ref for ref in repr_refs if ref in result_lower}
        assert len(found_repr) >= 1, (
            f"Should reference stick or surface representation, found: {found_repr}"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestGuardrailEnforcement:
    async def test_rejects_removed_capture_command(self, haiku_options):
        result = await ask_agent(
            "How do I use `pymol-agent-bridge capture` to take a screenshot of my protein?",
            haiku_options,
        )
        result_lower = result.lower()

        # Must NOT recommend the removed capture command as valid.
        # If the agent mentions it, it should be in a corrective context
        # (e.g., "capture is not a valid command"). We check that the redirect
        # to cmd.ray/cmd.png is present (below), which is the stronger signal.
        if "pymol-agent-bridge capture" in result_lower:
            # If mentioned, must be in a corrective/negative context nearby
            import re
            corrective = re.search(
                r"(not|removed|no longer|invalid|doesn.t|does not|isn.t).{0,100}capture"
                r"|capture.{0,100}(not|removed|no longer|invalid|doesn.t|does not|isn.t)",
                result_lower,
            )
            assert corrective, (
                "Agent mentioned 'pymol-agent-bridge capture' without corrective context"
            )

        # Should redirect to the correct approach
        assert "cmd.ray" in result_lower or "cmd.png" in result_lower, (
            "Should redirect to cmd.ray()/cmd.png() for image capture"
        )


# ---------------------------------------------------------------------------
# P1 regression tests — untested skill domains
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestMovieCreation:
    async def test_rotation_movie_advice(self, haiku_options):
        result = await ask_agent(
            "How do I create a 360-degree rotation movie of a protein in PyMOL "
            "and export it as frames?",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference movie setup
        assert "cmd.mset" in result_lower or "mset" in result_lower, (
            "Should reference cmd.mset() for frame setup"
        )

        # Must reference rotation or view interpolation
        assert (
            "mroll" in result_lower
            or "mview" in result_lower
            or "util.mroll" in result_lower
        ), "Should reference mroll or mview for rotation"

        # Must reference frame export
        assert "mpng" in result_lower or "cmd.mpng" in result_lower, (
            "Should reference cmd.mpng() for frame export"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestPublicationFigures:
    async def test_publication_export_advice(self, haiku_options):
        result = await ask_agent(
            "How do I export a publication-quality 300 DPI figure of a protein "
            "from PyMOL with a white background?",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference ray tracing and png export
        assert "cmd.ray" in result_lower, "Should reference cmd.ray() for rendering"
        assert "cmd.png" in result_lower, "Should reference cmd.png() for saving"

        # Should mention background or DPI settings
        bg_refs = {"bg_color", "white", "background", "opaque_background"}
        found_bg = {ref for ref in bg_refs if ref in result_lower}
        assert len(found_bg) >= 1, (
            f"Should reference background settings, found: {found_bg}"
        )

        # Must NOT use the broken cmd.png(path, width, height) pattern
        assert "cmd.png(path, width, height)" not in result_lower or "never" in result_lower, (
            "Should not recommend cmd.png(path, width, height)"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestDesignComparison:
    async def test_batch_qc_ranking_advice(self, haiku_options):
        result = await ask_agent(
            "I have 10 protein designs as PDB files. How do I compare and rank "
            "them in PyMOL? Show me the key commands.",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference grid mode for batch viewing
        assert "grid_mode" in result_lower or "grid" in result_lower, (
            "Should reference grid_mode for batch visual QC"
        )

        # Must reference alignment for comparison
        align_refs = {"cmd.align", "cmd.super", "cmd.cealign", "rms_cur", "align"}
        found_align = {ref for ref in align_refs if ref in result_lower}
        assert len(found_align) >= 1, (
            f"Should reference alignment commands, found: {found_align}"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestProteinMPNNVisualization:
    async def test_fixed_vs_designed_and_confidence(self, haiku_options):
        result = await ask_agent(
            "How do I visualize ProteinMPNN sequence design results in PyMOL? "
            "Show designed vs fixed residues and per-position confidence.",
            haiku_options,
        )
        result_lower = result.lower()

        # Must distinguish fixed vs designed residues
        assert "fixed" in result_lower or "designed" in result_lower, (
            "Should distinguish fixed vs designed residues"
        )

        # Should reference coloring for distinction
        assert "color" in result_lower, "Should reference coloring for residue distinction"

        # Should reference confidence visualization (B-factor/spectrum)
        confidence_refs = {"spectrum", "b_factor", "b-factor", "bfactor", "confidence"}
        found = {ref for ref in confidence_refs if ref in result_lower}
        assert len(found) >= 1, (
            f"Should reference confidence visualization, found: {found}"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestRFdiffusionVisualization:
    async def test_trajectory_and_self_consistency(self, haiku_options):
        result = await ask_agent(
            "How do I visualize RFdiffusion outputs in PyMOL? "
            "Cover trajectory viewing and self-consistency validation.",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference trajectory/multi-state viewing
        traj_refs = {"count_states", "mset", "trajectory", "frame", "states"}
        found_traj = {ref for ref in traj_refs if ref in result_lower}
        assert len(found_traj) >= 1, (
            f"Should reference trajectory/multi-state viewing, found: {found_traj}"
        )

        # Must reference self-consistency check
        sc_refs = {"self-consistency", "self_consistency", "rmsd", "align", "af2"}
        found_sc = {ref for ref in sc_refs if ref in result_lower}
        assert len(found_sc) >= 1, (
            f"Should reference self-consistency validation, found: {found_sc}"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestDesignInterfaceAnalysis:
    async def test_interface_qc_guidance(self, haiku_options):
        result = await ask_agent(
            "How do I analyze a protein-protein interface in PyMOL? "
            "Show me how to identify contacts and hydrogen bonds.",
            haiku_options,
        )
        result_lower = result.lower()

        # Must reference distance-based interface selection
        distance_refs = {"within", "around", "byres"}
        found = {ref for ref in distance_refs if ref in result_lower}
        assert len(found) >= 1, (
            f"Should reference distance-based selection, found: {found}"
        )

        # Must reference hydrogen bond visualization
        hbond_refs = {"distance", "h-bond", "hbond", "hydrogen bond", "mode=2", "mode 2"}
        found_hbond = {ref for ref in hbond_refs if ref in result_lower}
        assert len(found_hbond) >= 1, (
            f"Should reference hydrogen bond visualization, found: {found_hbond}"
        )

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"


@pytest.mark.slow
class TestProteinaComplexaWarnings:
    async def test_ame_chain_and_tmol_guardrail(self, haiku_options):
        result = await ask_agent(
            "I want to run Proteina-Complexa AME motif scaffolding. "
            "Can I keep my ligand on chain C with residue name RET? "
            "Also, should I enable the TMOL reward for this?",
            haiku_options,
        )
        result_lower = result.lower()

        # Must warn about chain A / L:0 requirement
        chain_refs = {"chain a", "l:0", "rename"}
        found_chain = {ref for ref in chain_refs if ref in result_lower}
        assert len(found_chain) >= 1, (
            f"Should warn about AME chain A / L:0 requirement, found: {found_chain}"
        )

        # Must warn that TMOL is not supported for AME
        tmol_refs = {"not supported", "unsupported", "not available", "don't", "do not", "cannot"}
        found_tmol = {ref for ref in tmol_refs if ref in result_lower}
        assert len(found_tmol) >= 1, (
            f"Should warn TMOL is not supported for AME, found: {found_tmol}"
        )


@pytest.mark.slow
class TestPymolSetupSafety:
    async def test_requires_user_choice_and_confirmation(self, haiku_options):
        result = await ask_agent(
            "Help me set up PyMOL with Claude. Walk me through the process.",
            haiku_options,
        )
        result_lower = result.lower()

        # Should reference checking for existing installation
        assert "status" in result_lower or "info" in result_lower or "check" in result_lower, (
            "Should check for existing installation first"
        )

        # Should reference virtual environment preference
        venv_refs = {"venv", "virtual environment", "virtualenv", "conda"}
        found_venv = {ref for ref in venv_refs if ref in result_lower}
        assert len(found_venv) >= 1, (
            f"Should mention virtual environment preference, found: {found_venv}"
        )

        # Should reference pymol-agent-bridge setup
        assert "setup" in result_lower, "Should reference pymol-agent-bridge setup"

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"
