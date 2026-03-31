"""Static validation of SKILL.md files.

These tests are free, deterministic, and run by default (no LLM, no API key).
"""

import pathlib

from conftest import extract_bridge_subcommands, parse_frontmatter

# Skills that only exist in .claude/skills/ (local dev), not distributed
KNOWN_LOCAL_ONLY = {"rfd3", "skill-development"}

# Local-only skills that intentionally lack YAML frontmatter
KNOWN_NO_FRONTMATTER = {"rfd3"}

# Patterns that indicate references to removed utilities
REMOVED_PATTERNS = [
    "pymol-agent-bridge capture",
    "pymol-agent-bridge image",
    "pymol-agent-bridge screenshot",
    "pymol_view",
]


def _skill_name(path: pathlib.Path) -> str:
    """Extract skill directory name from a SKILL.md path."""
    return path.parent.name


class TestDistributedSkillFrontmatter:
    """All distributed skills must have valid YAML frontmatter."""

    def test_all_have_frontmatter(self, distributed_skill_files):
        missing = []
        for path in distributed_skill_files:
            fm = parse_frontmatter(path)
            if fm is None:
                missing.append(_skill_name(path))
        assert not missing, f"Skills missing YAML frontmatter: {missing}"

    def test_all_have_required_fields(self, distributed_skill_files):
        incomplete = []
        for path in distributed_skill_files:
            fm = parse_frontmatter(path)
            if fm is None:
                continue
            missing_fields = []
            if "name" not in fm:
                missing_fields.append("name")
            if "description" not in fm:
                missing_fields.append("description")
            if missing_fields:
                incomplete.append(f"{_skill_name(path)}: missing {missing_fields}")
        assert not incomplete, f"Skills with incomplete frontmatter: {incomplete}"


class TestLocalSkillFrontmatter:
    """Local skills should have valid frontmatter (with known exclusions)."""

    def test_all_have_frontmatter(self, local_skill_files):
        missing = []
        for path in local_skill_files:
            name = _skill_name(path)
            if name in KNOWN_NO_FRONTMATTER:
                continue
            fm = parse_frontmatter(path)
            if fm is None:
                missing.append(name)
        assert not missing, f"Local skills missing YAML frontmatter: {missing}"


class TestNoRemovedUtilities:
    """No SKILL.md should reference removed pymol-agent-bridge utilities."""

    def test_distributed_skills(self, distributed_skill_files):
        violations = []
        for path in distributed_skill_files:
            text = path.read_text()
            for pattern in REMOVED_PATTERNS:
                if pattern in text:
                    violations.append(f"{_skill_name(path)}: contains '{pattern}'")
        assert not violations, f"Removed utility references found: {violations}"

    def test_local_skills(self, local_skill_files):
        violations = []
        for path in local_skill_files:
            text = path.read_text()
            for pattern in REMOVED_PATTERNS:
                if pattern in text:
                    violations.append(f"{_skill_name(path)}: contains '{pattern}'")
        assert not violations, f"Removed utility references found: {violations}"


class TestSkillDirectorySync:
    """Distributed and local skill directories should be in sync."""

    def test_directories_match(self, repo_root):
        distributed = {
            p.name
            for p in (repo_root / "claude-plugin" / "skills").iterdir()
            if p.is_dir()
        }
        local = {
            p.name
            for p in (repo_root / ".claude" / "skills").iterdir()
            if p.is_dir()
        }
        local_only = local - distributed - KNOWN_LOCAL_ONLY
        distributed_only = distributed - local

        errors = []
        if local_only:
            errors.append(
                f"In .claude/skills/ but not distributed (and not in KNOWN_LOCAL_ONLY): {local_only}"
            )
        if distributed_only:
            errors.append(
                f"In claude-plugin/skills/ but not in .claude/skills/: {distributed_only}"
            )
        assert not errors, "\n".join(errors)


class TestBridgeCommandsValid:
    """All pymol-agent-bridge subcommands in skills must be valid."""

    def test_distributed_skills(self, distributed_skill_files, valid_bridge_commands):
        invalid = {}
        for path in distributed_skill_files:
            text = path.read_text()
            cmds = extract_bridge_subcommands(text)
            bad = cmds - valid_bridge_commands
            if bad:
                invalid[_skill_name(path)] = bad
        assert not invalid, f"Invalid bridge subcommands found: {invalid}"

    def test_local_skills(self, local_skill_files, valid_bridge_commands):
        invalid = {}
        for path in local_skill_files:
            text = path.read_text()
            cmds = extract_bridge_subcommands(text)
            bad = cmds - valid_bridge_commands
            if bad:
                invalid[_skill_name(path)] = bad
        assert not invalid, f"Invalid bridge subcommands found: {invalid}"
