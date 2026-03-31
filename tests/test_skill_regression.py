"""Agent SDK regression tests for claudemol skills.

These tests spawn real Claude Code sessions (Haiku model) and cost tokens.
They are excluded from default pytest runs — use `pytest -m slow` to run them.

Requires: claude-agent-sdk (not yet available on PyPI as of 2026-03-30).
"""

import pytest

sdk = pytest.importorskip("claude_agent_sdk")


async def ask_agent(prompt: str, options) -> str:
    """Run a Claude Agent SDK query and return the final result text."""
    result = ""
    async for message in sdk.query(prompt=prompt, options=options):
        if isinstance(message, sdk.ResultMessage):
            result = message.result or ""
    return result


@pytest.fixture
def agent_options(repo_root):
    """Agent options for skill regression tests."""
    return sdk.ClaudeAgentOptions(
        cwd=str(repo_root),
        allowed_tools=["Read", "Glob", "Grep"],
        setting_sources=["project"],
        max_turns=3,
        model="claude-haiku-4-5",
    )


VALID_BRIDGE_COMMANDS = {"setup", "status", "test", "info", "launch", "exec"}


@pytest.mark.slow
class TestImageCapture:
    async def test_uses_native_pymol_commands(self, agent_options):
        result = await ask_agent(
            "How do I capture a publication-quality image of a protein in PyMOL?",
            agent_options,
        )
        result_lower = result.lower()

        # Must use native PyMOL commands (cmd.ray + cmd.png pattern)
        assert "cmd.ray" in result_lower, "Should reference cmd.ray() for rendering"
        assert "cmd.png" in result_lower, "Should reference cmd.png() for saving"

        # Must NOT reference removed utilities
        for removed in ["pymol-agent-bridge capture", "pymol-agent-bridge image", "pymol-agent-bridge screenshot"]:
            assert removed not in result_lower, f"Should not reference removed utility: {removed}"

        # Should NOT use the broken cmd.png(path, width, height) pattern
        assert "cmd.png(path, width, height)" not in result_lower or "never" in result_lower, (
            "Should not recommend cmd.png(path, width, height) — causes view corruption"
        )


@pytest.mark.slow
class TestBridgeCommands:
    async def test_only_valid_subcommands(self, agent_options):
        result = await ask_agent(
            "List all the pymol-agent-bridge subcommands you would use and explain each one.",
            agent_options,
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
    async def test_correct_connection_steps(self, agent_options):
        result = await ask_agent(
            "Walk me through connecting to PyMOL step by step.",
            agent_options,
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
