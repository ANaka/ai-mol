"""Agent SDK regression tests for claudemol skills.

These tests spawn real Claude Code sessions (Haiku model) and cost tokens.
They are excluded from default pytest runs — use `pytest -m slow` to run them.

Requires: claude-agent-sdk.
"""

import pytest

sdk = pytest.importorskip("claude_agent_sdk")

from conftest import ask_agent  # noqa: E402


VALID_BRIDGE_COMMANDS = {"setup", "status", "test", "info", "launch", "exec"}

REMOVED_UTILITIES = [
    "pymol-agent-bridge capture",
    "pymol-agent-bridge image",
    "pymol-agent-bridge screenshot",
]


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
        for removed in ["pymol-agent-bridge capture", "pymol-agent-bridge image", "pymol_view"]:
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

        # Must NOT recommend the removed capture command
        assert "pymol-agent-bridge capture" not in result_lower or (
            "not" in result_lower or "removed" in result_lower or "doesn't" in result_lower
            or "does not" in result_lower or "no longer" in result_lower
            or "isn't" in result_lower or "invalid" in result_lower
        ), "Should not recommend pymol-agent-bridge capture as a valid command"

        # Should redirect to the correct approach
        assert "cmd.ray" in result_lower or "cmd.png" in result_lower, (
            "Should redirect to cmd.ray()/cmd.png() for image capture"
        )
