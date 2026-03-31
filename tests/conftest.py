"""Shared fixtures and helpers for claudemol skill tests."""

import pathlib
import re
import warnings

import pytest


# ---------------------------------------------------------------------------
# Static test fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def repo_root() -> pathlib.Path:
    """Return the absolute path to the repo root."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture
def valid_bridge_commands() -> set[str]:
    """Valid pymol-agent-bridge subcommands per CLAUDE.md."""
    return {"setup", "status", "test", "info", "launch", "exec"}


@pytest.fixture
def distributed_skill_files(repo_root) -> list[pathlib.Path]:
    """All SKILL.md files in the distributed plugin."""
    return sorted(repo_root.glob("claude-plugin/skills/*/SKILL.md"))


@pytest.fixture
def local_skill_files(repo_root) -> list[pathlib.Path]:
    """All SKILL.md files in local dev skills."""
    return sorted(repo_root.glob(".claude/skills/*/SKILL.md"))


def parse_frontmatter(path: pathlib.Path) -> dict | None:
    """Parse YAML frontmatter from a SKILL.md file.

    Returns the frontmatter as a dict, or None if no frontmatter found.
    """
    text = path.read_text()
    if not text.startswith("---"):
        return None
    end = text.find("---", 3)
    if end == -1:
        return None
    frontmatter = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            frontmatter[key.strip()] = value.strip()
    return frontmatter


def extract_bridge_subcommands(text: str) -> set[str]:
    """Extract pymol-agent-bridge subcommands from text.

    Matches command invocations in both plain and path-prefixed forms, e.g.:
    - pymol-agent-bridge exec
    - ~/.pymol-agent-bridge/bin/pymol-agent-bridge exec
    - .venv/bin/pymol-agent-bridge setup
    """
    pattern = r"""(?:^|[\s`"'(])(?:[^\s`"']*/)?pymol-agent-bridge\s+([A-Za-z][\w-]*)"""
    matches = re.findall(pattern, text, re.MULTILINE)
    # Filter out words that are clearly prose, not subcommands
    prose_words = {
        "is", "connects", "the", "and", "or", "not", "tool",
        "socket", "plugin", "package", "binary", "wrapper", "script",
        "already", "installed", "configured", "python", "cli",
    }
    return {m.lower() for m in matches if m.lower() not in prose_words}


# ---------------------------------------------------------------------------
# Agent SDK helpers
# ---------------------------------------------------------------------------

async def collect_agent_messages(prompt: str, options) -> tuple[str, list[tuple[str, dict]]]:
    """Run an agent query and return (result_text, tool_calls).

    tool_calls is a list of (tool_name, tool_input) tuples extracted from
    ToolUseBlock instances in AssistantMessage content.
    """
    sdk = pytest.importorskip("claude_agent_sdk")
    result_text = ""
    tool_calls: list[tuple[str, dict]] = []
    async for message in sdk.query(prompt=prompt, options=options):
        if isinstance(message, sdk.AssistantMessage):
            for block in message.content:
                if isinstance(block, sdk.ToolUseBlock):
                    tool_calls.append((block.name, block.input))
        elif isinstance(message, sdk.ResultMessage):
            result_text = message.result or ""
    return result_text, tool_calls


async def ask_agent(prompt: str, options) -> str:
    """Run an agent query and return just the result text."""
    text, _ = await collect_agent_messages(prompt, options)
    return text


def skill_dirs_from_tool_calls(tool_calls: list[tuple[str, dict]]) -> set[str]:
    """Extract distinct skill directory names from Read tool calls.

    Looks for paths matching .../skills/<name>/... and returns the set of
    skill directory names accessed.
    """
    dirs: set[str] = set()
    for name, inp in tool_calls:
        if name == "Read" and "file_path" in inp:
            m = re.search(r"skills/([^/]+)/", inp["file_path"])
            if m:
                dirs.add(m.group(1))
    return dirs


def assert_skill_accessed(tool_calls: list[tuple[str, dict]], skill_name: str) -> None:
    """Soft assertion: warn if the agent didn't read from the expected skill directory.

    Emits a warning rather than failing — the agent may produce correct output
    from training knowledge without reading the skill file.
    """
    dirs = skill_dirs_from_tool_calls(tool_calls)
    if skill_name not in dirs:
        warnings.warn(
            f"Agent did not read from '{skill_name}' skill directory. "
            f"Skill dirs accessed: {dirs or 'none'}",
            stacklevel=2,
        )


# ---------------------------------------------------------------------------
# Model-specific agent option fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def haiku_options(repo_root):
    """Agent options for Haiku-tier tests."""
    sdk = pytest.importorskip("claude_agent_sdk")
    return sdk.ClaudeAgentOptions(
        cwd=str(repo_root),
        allowed_tools=["Read", "Glob", "Grep"],
        setting_sources=["project"],
        max_turns=4,
        model="claude-haiku-4-5",
    )


@pytest.fixture
def sonnet_options(repo_root):
    """Agent options for Sonnet-tier tests."""
    sdk = pytest.importorskip("claude_agent_sdk")
    return sdk.ClaudeAgentOptions(
        cwd=str(repo_root),
        allowed_tools=["Read", "Glob", "Grep"],
        setting_sources=["project"],
        max_turns=5,
        model="claude-sonnet-4-6",
    )


@pytest.fixture
def opus_options(repo_root):
    """Agent options for Opus-tier tests."""
    sdk = pytest.importorskip("claude_agent_sdk")
    return sdk.ClaudeAgentOptions(
        cwd=str(repo_root),
        allowed_tools=["Read", "Glob", "Grep"],
        setting_sources=["project"],
        max_turns=7,
        model="claude-opus-4-6",
    )
