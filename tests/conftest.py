"""Shared fixtures for claudemol skill tests."""

import pathlib
import re

import pytest


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
