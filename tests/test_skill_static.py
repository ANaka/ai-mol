"""Static validation of SKILL.md files.

These tests are free, deterministic, and run by default (no LLM, no API key).
"""

import pathlib

import re

from conftest import (
    REMOVED_UTILITIES,
    extract_bridge_subcommands,
    extract_skill_refs,
    parse_frontmatter,
)

# Skills that only exist in .claude/skills/ (local dev), not distributed
KNOWN_LOCAL_ONLY = {"rfd3", "skill-development"}

# Local-only skills that intentionally lack YAML frontmatter
KNOWN_NO_FRONTMATTER = {"rfd3"}

# Patterns that indicate references to removed utilities
# Extends the shared list with patterns only relevant to static skill checks
REMOVED_PATTERNS = REMOVED_UTILITIES + ["pymol_view"]


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


class TestSkillContentSync:
    """Distributed and local SKILL.md files should have identical content."""

    def test_skill_md_contents_match(self, repo_root):
        distributed_dir = repo_root / "claude-plugin" / "skills"
        local_dir = repo_root / ".claude" / "skills"
        drifted = []
        for dist_skill in sorted(distributed_dir.iterdir()):
            if not dist_skill.is_dir():
                continue
            local_skill = local_dir / dist_skill.name
            if not local_skill.exists():
                continue  # caught by TestSkillDirectorySync
            dist_md = dist_skill / "SKILL.md"
            local_md = local_skill / "SKILL.md"
            if dist_md.exists() and local_md.exists():
                if dist_md.read_text() != local_md.read_text():
                    drifted.append(dist_skill.name)
        assert not drifted, f"SKILL.md content differs between distributed and local: {drifted}"


class TestCrossSkillReferences:
    """All @skill-name references must point to real skill directories."""

    def test_all_refs_resolve(self, distributed_skill_files, repo_root):
        skill_dirs = {
            p.name
            for p in (repo_root / "claude-plugin" / "skills").iterdir()
            if p.is_dir()
        }
        broken = {}
        for path in distributed_skill_files:
            text = path.read_text()
            refs = extract_skill_refs(text)
            bad = refs - skill_dirs
            if bad:
                broken[_skill_name(path)] = bad
        assert not broken, f"Broken @skill references: {broken}"


class TestFrontmatterSemantics:
    """Frontmatter values should be consistent and well-formed."""

    # Skills where frontmatter name intentionally differs from directory name
    KNOWN_NAME_EXCEPTIONS = {"skill-development"}

    def test_name_matches_directory(self, distributed_skill_files):
        mismatched = []
        for path in distributed_skill_files:
            name = _skill_name(path)
            if name in self.KNOWN_NAME_EXCEPTIONS:
                continue
            fm = parse_frontmatter(path)
            if fm is None:
                continue
            if fm.get("name") != name:
                mismatched.append(f"{name}: name={fm.get('name')!r}")
        assert not mismatched, f"Frontmatter name doesn't match directory: {mismatched}"

    def test_version_is_semver(self, distributed_skill_files):
        invalid = []
        for path in distributed_skill_files:
            fm = parse_frontmatter(path)
            if fm is None or "version" not in fm:
                continue
            if not re.match(r"^\d+\.\d+\.\d+$", fm["version"]):
                invalid.append(
                    f"{_skill_name(path)}: version={fm['version']!r}"
                )
        assert not invalid, f"Non-semver version strings: {invalid}"


class TestImageCaptureSafety:
    """No skill should use the broken cmd.png(path, width, height) pattern."""

    def test_no_broken_cmd_png_signature(self, distributed_skill_files):
        # Match cmd.png calls with 3+ positional args (the broken pattern).
        # Allow cmd.png(path) and cmd.png(path, dpi=300) (keyword args are fine).
        # Exclude commented-out lines (skills may document the anti-pattern).
        pattern = re.compile(
            r"cmd\.png\(\s*"
            r"[^)]+,"   # first arg + comma
            r"\s*\d+"   # second arg is a bare number (width)
            r"\s*,"     # comma
            r"\s*\d+"   # third arg is a bare number (height)
        )
        violations = []
        for path in distributed_skill_files:
            text = path.read_text()
            for line in text.splitlines():
                stripped = line.lstrip()
                # Skip comment lines (documenting the anti-pattern)
                if stripped.startswith("#") or stripped.startswith("//"):
                    continue
                if pattern.search(line):
                    violations.append(_skill_name(path))
                    break
        assert not violations, (
            f"Skills using broken cmd.png(path, width, height) pattern "
            f"(causes view corruption): {violations}"
        )


class TestNoReinitializeExamples:
    """No skill should contain cmd.reinitialize() in executable code examples."""

    def test_distributed_skills(self, distributed_skill_files):
        violations = []
        for path in distributed_skill_files:
            text = path.read_text()
            for line in text.splitlines():
                stripped = line.lstrip()
                # Skip lines that are warnings/rules about reinitialize
                if stripped.startswith(("#", "-", ">", "*", "//", "`")):
                    continue
                if "cmd.reinitialize()" in line:
                    violations.append(_skill_name(path))
                    break
        assert not violations, (
            f"Skills containing cmd.reinitialize() in code examples "
            f"(destroys user state): {violations}"
        )
