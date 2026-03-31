"""Agent SDK behavioral tests for claudemol skills.

These tests inspect tool calls (not just result text) to verify that the agent
correctly discovers, reads, and applies skill content. Uses the SDK's
AssistantMessage.content containing ToolUseBlock to verify agent behavior.

Tests are organized by model tier:
- @pytest.mark.slow  — Haiku (cheap, structural/discovery)
- @pytest.mark.sonnet — Sonnet (script generation, cross-skill synthesis)
- @pytest.mark.opus  — Opus (complex multi-skill reasoning)

All tests run without PyMOL or external services.

Requires: claude-agent-sdk.
"""

import ast
import re
import warnings

import pytest

sdk = pytest.importorskip("claude_agent_sdk")

from conftest import (  # noqa: E402
    REMOVED_UTILITIES,
    assert_skill_accessed,
    collect_agent_messages,
    skill_dirs_from_tool_calls,
)


# ---------------------------------------------------------------------------
# Haiku behavioral tests
# ---------------------------------------------------------------------------


@pytest.mark.slow
class TestSkillDiscovery:
    """Verify the agent discovers and reads the correct skill file for a topic."""

    async def test_finds_antibody_skill(self, haiku_options):
        result, tool_calls = await collect_agent_messages(
            "How do I visualize antibody CDR loops in PyMOL? "
            "Read the relevant skill file and summarize the approach.",
            haiku_options,
        )
        result_lower = result.lower()

        # HARD: result contains CDR-specific content
        cdr_refs = {"cdr", "h1", "h2", "h3", "l1", "l2", "l3"}
        found = {ref for ref in cdr_refs if ref in result_lower}
        assert len(found) >= 1, (
            f"Result should mention CDR loop identifiers, found: {found}"
        )
        assert "color" in result_lower or "select" in result_lower, (
            "Result should mention coloring or selection for CDR loops"
        )

        # SOFT: agent read from the antibody-visualization skill directory
        assert_skill_accessed(tool_calls, "antibody-visualization")


@pytest.mark.slow
class TestToolUsagePatterns:
    """Verify the agent uses appropriate tools even when Bash is available."""

    async def test_prefers_read_over_bash_for_info(self, haiku_options_with_bash):
        """When Bash is available, agent should still prefer Read/Glob/Grep
        for looking up information from skill files."""
        result, tool_calls = await collect_agent_messages(
            "What are the basic PyMOL commands for loading and visualizing "
            "a protein structure? Read the relevant skill file.",
            haiku_options_with_bash,
        )
        result_lower = result.lower()

        # HARD: result contains useful PyMOL commands
        assert "cmd.fetch" in result_lower or "cmd.load" in result_lower, (
            "Result should mention cmd.fetch() or cmd.load()"
        )

        # HARD: agent should not use Bash for a read-only informational query
        bash_calls = [name for name, _ in tool_calls if name == "Bash"]
        assert len(bash_calls) == 0, (
            f"Agent should not use Bash for information lookup, "
            f"but made {len(bash_calls)} Bash call(s)"
        )

        # SOFT: agent read from a relevant skill directory
        dirs = skill_dirs_from_tool_calls(tool_calls)
        relevant = dirs & {"pymol-fundamentals", "protein-structure-basics"}
        if not relevant:
            warnings.warn(
                f"Agent didn't read from pymol-fundamentals or "
                f"protein-structure-basics. Dirs accessed: {dirs or 'none'}",
                stacklevel=2,
            )


# ---------------------------------------------------------------------------
# Sonnet behavioral tests
# ---------------------------------------------------------------------------


@pytest.mark.sonnet
class TestScriptGeneration:
    """Verify the agent generates syntactically valid PyMOL scripts."""

    async def test_antibody_cdr_script(self, sonnet_options):
        result, tool_calls = await collect_agent_messages(
            "Write a complete PyMOL Python script that:\n"
            "1. Fetches antibody structure 7FAE\n"
            "2. Selects each CDR loop (H1, H2, H3)\n"
            "3. Colors each loop a different color\n"
            "4. Shows the antibody as cartoon with CDR loops as sticks\n\n"
            "Output ONLY the Python script, no explanation.",
            sonnet_options,
        )

        # Extract code blocks from the result
        code_blocks = re.findall(r"```(?:python)?\s*\n(.*?)```", result, re.DOTALL)
        script = code_blocks[0] if code_blocks else result

        # HARD: script is syntactically valid Python
        try:
            ast.parse(script)
        except SyntaxError as e:
            pytest.fail(f"Generated script has syntax error: {e}\n\nScript:\n{script}")

        script_lower = script.lower()

        # HARD: script contains key PyMOL patterns
        assert "cmd.select" in script_lower or "select " in script_lower, (
            "Script should contain selection commands"
        )
        assert "cmd.color" in script_lower or "color " in script_lower, (
            "Script should contain coloring commands"
        )
        assert "cmd.show" in script_lower or "show " in script_lower, (
            "Script should contain show commands"
        )

        # SOFT: agent consulted the antibody skill
        assert_skill_accessed(tool_calls, "antibody-visualization")


@pytest.mark.sonnet
class TestCrossSkillSynthesis:
    """Verify the agent reads from multiple skills for a cross-domain question."""

    async def test_alphafold_antibody_workflow(self, sonnet_options):
        result, tool_calls = await collect_agent_messages(
            "I have an AlphaFold model of an antibody. Walk me through how to:\n"
            "1. Validate the prediction quality (confidence, pLDDT)\n"
            "2. Visualize the CDR loops\n"
            "Read the relevant skill files before answering.",
            sonnet_options,
        )
        result_lower = result.lower()

        # HARD: result covers both validation and CDR visualization
        assert "plddt" in result_lower, (
            "Should mention pLDDT for AlphaFold validation"
        )
        cdr_refs = {"cdr", "h1", "h2", "h3", "l1", "l2", "l3"}
        found_cdr = {ref for ref in cdr_refs if ref in result_lower}
        assert len(found_cdr) >= 1, (
            f"Should mention CDR identifiers, found: {found_cdr}"
        )

        # SOFT: agent read from both skill directories
        dirs = skill_dirs_from_tool_calls(tool_calls)
        expected = {"alphafold-validation", "antibody-visualization"}
        found = dirs & expected
        if len(found) < 2:
            warnings.warn(
                f"Expected reads from {expected}, but only found: {found}. "
                f"All dirs accessed: {dirs or 'none'}",
                stacklevel=2,
            )


@pytest.mark.sonnet
class TestBridgeCommandConstruction:
    """Verify the agent constructs correct pymol-agent-bridge exec commands."""

    async def test_multi_step_bridge_commands(self, sonnet_options):
        result, tool_calls = await collect_agent_messages(
            "Construct the exact pymol-agent-bridge exec commands I would run to:\n"
            "1. Load a PDB structure 1ubq\n"
            "2. Color it by B-factor using spectrum\n"
            "3. Save a PNG image to /tmp/bfactor.png\n\n"
            "Give me the literal shell commands, ready to copy-paste.",
            sonnet_options,
        )

        # HARD: output contains pymol-agent-bridge exec invocations
        exec_pattern = r"pymol-agent-bridge\s+exec"
        exec_matches = re.findall(exec_pattern, result)
        assert len(exec_matches) >= 2, (
            f"Expected at least 2 pymol-agent-bridge exec commands, "
            f"found {len(exec_matches)}"
        )

        result_lower = result.lower()

        # HARD: commands reference the key operations
        assert "fetch" in result_lower or "load" in result_lower, (
            "Should include a fetch/load command for 1ubq"
        )
        assert "spectrum" in result_lower or "b-factor" in result_lower or "b_factor" in result_lower, (
            "Should include B-factor coloring"
        )
        assert "png" in result_lower, "Should include PNG save command"

        # Must NOT reference removed utilities
        for removed in REMOVED_UTILITIES:
            assert removed not in result_lower, (
                f"Should not reference removed utility: {removed}"
            )


# ---------------------------------------------------------------------------
# Opus behavioral test
# ---------------------------------------------------------------------------


@pytest.mark.opus
class TestComplexWorkflowReasoning:
    """Verify the agent reasons across multiple skills for a complex workflow."""

    async def test_proteinmpnn_qc_workflow(self, opus_options):
        result, tool_calls = await collect_agent_messages(
            "I have 5 ProteinMPNN designs for a binder. Walk me through the "
            "full QC workflow in PyMOL:\n"
            "1. Load all designs and the input backbone\n"
            "2. Align and compare designs to the input\n"
            "3. Check interface contacts and buried surface area\n"
            "4. Color by ProteinMPNN confidence scores\n"
            "5. Export comparison figures\n\n"
            "Read the relevant skill files and give me the complete workflow "
            "with PyMOL commands.",
            opus_options,
        )
        result_lower = result.lower()

        # HARD: result covers the major workflow stages
        # Stage 1: loading/alignment
        assert "cmd.load" in result_lower or "cmd.fetch" in result_lower, (
            "Should include structure loading commands"
        )
        assert "align" in result_lower or "super" in result_lower or "cealign" in result_lower, (
            "Should include alignment commands"
        )

        # Stage 2: interface analysis
        interface_refs = {"interface", "buried surface", "bsa", "contact", "distance"}
        found_interface = {ref for ref in interface_refs if ref in result_lower}
        assert len(found_interface) >= 1, (
            f"Should reference interface analysis concepts, found: {found_interface}"
        )

        # Stage 3: confidence coloring
        assert "spectrum" in result_lower or "b_factor" in result_lower or "confidence" in result_lower, (
            "Should reference confidence-based coloring"
        )

        # Stage 4: figure export
        assert "cmd.png" in result_lower or "cmd.ray" in result_lower, (
            "Should include figure export commands"
        )

        # SOFT: agent consulted at least 3 distinct skill directories
        dirs = skill_dirs_from_tool_calls(tool_calls)
        expected = {
            "design-comparison", "proteinmpnn-viz",
            "design-interface-analysis", "publication-figures",
        }
        found = dirs & expected
        if len(found) < 3:
            warnings.warn(
                f"Expected reads from at least 3 of {expected}, "
                f"but found: {found}. All dirs: {dirs or 'none'}",
                stacklevel=2,
            )
