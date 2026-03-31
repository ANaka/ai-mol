"""Integration tests that exercise skills against a real PyMOL instance.

These tests require:
- pymol-agent-bridge installed and configured
- PyMOL running (or launchable via pymol-agent-bridge launch)
- claude-agent-sdk installed

They are marked @pytest.mark.slow (excluded from default pytest runs).
"""

import ast
import os
import subprocess
import tempfile

import pytest

sdk = pytest.importorskip("claude_agent_sdk")

BRIDGE = os.path.expanduser("~/.pymol-agent-bridge/bin/pymol-agent-bridge")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def bridge_exec(cmd: str, timeout: int = 60) -> str:
    """Send a command to PyMOL via the bridge and return stdout.

    Default timeout is 60s to accommodate slow network fetches (e.g., cmd.fetch
    from RCSB).
    """
    result = subprocess.run(
        [BRIDGE, "exec", cmd],
        capture_output=True, text=True, timeout=timeout,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Bridge exec failed: {result.stderr}")
    return result.stdout.strip()


def bridge_status() -> bool:
    """Check if PyMOL bridge is reachable."""
    result = subprocess.run(
        [BRIDGE, "status"],
        capture_output=True, text=True, timeout=10,
    )
    return "OK" in result.stdout


def pymol_get_names() -> list[str]:
    """Get list of loaded object names in PyMOL."""
    # Use ast.literal_eval to handle edge cases (names with commas, extra
    # whitespace, etc.) — the output is always a Python list literal from
    # cmd.get_names().
    raw = bridge_exec("print(cmd.get_names())")
    if not raw or raw == "[]":
        return []
    try:
        return ast.literal_eval(raw)
    except (ValueError, SyntaxError):
        # Fallback: naive split
        return [s.strip().strip("'\"") for s in raw.strip("[]").split(",")]


def pymol_reinitialize():
    """Clear all objects from PyMOL."""
    bridge_exec("cmd.reinitialize()")


async def ask_agent(prompt: str, options) -> str:
    """Run a Claude Agent SDK query and return the final result text."""
    result = ""
    async for message in sdk.query(prompt=prompt, options=options):
        if isinstance(message, sdk.ResultMessage):
            result = message.result or ""
    return result


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module", autouse=True)
def require_pymol():
    """Skip all tests in this module if PyMOL bridge is not available."""
    if not os.path.exists(BRIDGE):
        pytest.skip("pymol-agent-bridge not installed")
    if not bridge_status():
        pytest.skip("PyMOL not running")


@pytest.fixture(autouse=True)
def clean_pymol():
    """Reinitialize PyMOL before each test for a clean state."""
    pymol_reinitialize()
    yield


@pytest.fixture
def agent_options(repo_root):
    """Agent options for integration tests - allowed to use Bash for bridge exec."""
    return sdk.ClaudeAgentOptions(
        cwd=str(repo_root),
        allowed_tools=["Read", "Glob", "Grep", "Bash"],
        setting_sources=["project"],
        max_turns=5,
        model="claude-haiku-4-5",
    )


# ---------------------------------------------------------------------------
# Test: Fetch and verify a structure loads
# ---------------------------------------------------------------------------

@pytest.mark.slow
class TestFetchStructure:
    """Agent fetches a protein structure and we verify it loaded in PyMOL."""

    async def test_fetch_loads_object(self, agent_options):
        await ask_agent(
            "Fetch PDB structure 1ubq into PyMOL. Just fetch it, nothing else.",
            agent_options,
        )
        names = pymol_get_names()
        assert "1ubq" in [n.lower() for n in names], (
            f"Expected '1ubq' in PyMOL objects, got: {names}"
        )

    async def test_fetch_has_atoms(self, agent_options):
        await ask_agent(
            "Fetch PDB structure 1ubq into PyMOL.",
            agent_options,
        )
        count = bridge_exec("print(cmd.count_atoms('all'))")
        assert int(count) > 0, "Fetched structure should have atoms"


# ---------------------------------------------------------------------------
# Test: Representation changes
# ---------------------------------------------------------------------------

@pytest.mark.slow
class TestRepresentations:
    """Agent applies different representations and we verify via PyMOL state."""

    async def test_cartoon_representation(self, agent_options):
        bridge_exec("cmd.fetch('1ubq')")

        await ask_agent(
            "Show 1ubq as cartoon only in PyMOL. Hide all other representations.",
            agent_options,
        )
        cartoon_count = bridge_exec("print(cmd.count_atoms('rep cartoon'))")
        assert int(cartoon_count) > 0, "Cartoon representation should be visible"

    async def test_surface_representation(self, agent_options):
        bridge_exec("cmd.fetch('1ubq')")

        await ask_agent(
            "Show the surface of 1ubq in PyMOL.",
            agent_options,
        )
        surface_count = bridge_exec("print(cmd.count_atoms('rep surface'))")
        assert int(surface_count) > 0, "Surface representation should be visible"


# ---------------------------------------------------------------------------
# Test: Image export (publication figures skill)
# ---------------------------------------------------------------------------

@pytest.mark.slow
class TestImageExport:
    """Agent creates a figure and we verify the PNG file exists."""

    async def test_ray_trace_and_save(self, agent_options):
        bridge_exec("cmd.fetch('1ubq')")

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_figure.png")
            # Give Claude the exact output path. This works because PyMOL runs
            # locally and has access to the same filesystem. The agent sends
            # cmd.png(path) through pymol-agent-bridge exec.
            await ask_agent(
                f"Ray trace 1ubq at 800x600 and save as a PNG to {output_path}. "
                "Use white background.",
                agent_options,
            )
            assert os.path.exists(output_path), (
                f"Expected PNG at {output_path} but file not found"
            )
            with open(output_path, "rb") as f:
                magic = f.read(4)
            assert magic == b"\x89PNG", "File should be a valid PNG"


# ---------------------------------------------------------------------------
# Test: Structure alignment (structure-alignment-analysis skill)
# ---------------------------------------------------------------------------

@pytest.mark.slow
class TestStructureAlignment:
    """Agent aligns two structures and we verify RMSD is reasonable."""

    async def test_align_two_structures(self, agent_options):
        bridge_exec("cmd.fetch('1ubq')")
        bridge_exec("cmd.fetch('1ubi')")

        result = await ask_agent(
            "Align 1ubi onto 1ubq in PyMOL and tell me the RMSD.",
            agent_options,
        )
        # Verify at least 2 objects still loaded (agent may rename them)
        names = pymol_get_names()
        assert len(names) >= 2, f"Expected at least 2 objects after alignment, got: {names}"

        # Verify total atom count is reasonable (both structures present)
        total = int(bridge_exec("print(cmd.count_atoms('all'))"))
        assert total > 1000, f"Expected >1000 atoms (two structures), got: {total}"

        # Verify the agent mentioned RMSD in the response
        assert "rmsd" in result.lower(), "Agent should report the RMSD value"
