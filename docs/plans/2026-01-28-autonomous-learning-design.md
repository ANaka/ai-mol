# Autonomous Learning Design: Claude-PyMOL Integration

## Vision

Build a robust, self-improving PyMOL integration that can bootstrap users into productive protein science work with Claude as a capable partner.

## Principles

- **Reliability first** - Bulletproof session management before capability expansion
- **Self-regulation** - Step back to fundamentals when hitting repeated failures
- **Capture learnings** - Skills, tests, and docs emerge from work, not as separate projects
- **Bootstrap-able** - Someone can clone and be productive in minutes

---

## Phase 1: Foundation - Session Management & Visual Feedback

**Goal:** Make PyMOL interaction bulletproof.

### Components

1. **Session lifecycle management** (`pymol_session.py`)
   - Launch PyMOL with plugin auto-loaded
   - Health check (is connection alive?)
   - Graceful close
   - Force kill for stuck processes
   - Process tracking to detect zombies
   - Automatic recovery: dead connection → kill stale → relaunch

2. **Visual feedback loop** (extend `pymol_view.py`)
   - `snapshot(name)` - capture current state, return path
   - Automatic scratch cleanup (keep last N images)
   - Standardized image sizes

3. **Connection health**
   - Heartbeat/ping command
   - Timeout handling with clear errors
   - Reconnection logic

### Tests

- Launch PyMOL, verify connection, close cleanly
- Kill PyMOL externally, verify detection and recovery
- Send command to dead connection, verify graceful failure + recovery
- Visual feedback produces viewable images

### Exit Criteria

- [ ] Can launch PyMOL programmatically
- [ ] Can detect when PyMOL dies
- [ ] Can recover from crashes automatically
- [ ] Can take snapshots reliably
- [ ] Tests pass

---

## Phase 2: Autonomous Learning System

**Goal:** Systematically build capabilities through curriculum work.

### Learning Loop

```
1. Pick task from curriculum (Tier 1 → 2 → 3 → 4)
2. Attempt the task
3. Record outcome:
   - Success → extract patterns, consider skill/test
   - Failure → diagnose, fix tooling or note gap
4. Update progress tracking
5. Repeat
```

### Progress Tracking

File: `docs/progress/curriculum-tracker.md`

Contents:
- Tasks attempted, passed, failed
- Blockers encountered
- Skills created
- Gaps identified (features requiring plugins, etc.)

### Skill Creation Triggers

- Same problem solved 2-3 times → extract to skill
- Workflow with 3+ steps that always go together → skill
- Non-obvious PyMOL behavior discovered → document in skill

### Self-Regulation Rules

- 3+ consecutive failures → step back, check fundamentals
- Same error pattern repeats → stop and fix tooling
- Task requires unavailable capability → note gap, skip, revisit

### Curriculum Sources

- `docs/curricula/compass_artifact_*.md` - 85 tasks across 4 tiers
- `docs/curricula/gemini_curriculum.md` - 100 tasks across 5 tiers

### Exit Criteria

- [ ] Tier 1 (Basic) tasks: >90% pass rate
- [ ] Tier 2 (Intermediate) tasks: >80% pass rate
- [ ] Core skills documented and tested
- [ ] Progress tracker maintained

---

## Phase 3: Polish & Bootstrap Experience

**Goal:** Make the repo clone-and-go for new users.

### Target Structure

```
pymol-mcp/
├── pymol_session.py      # Session lifecycle
├── pymol_connection.py   # Socket communication
├── pymol_view.py         # Visual feedback helpers
├── claude_socket_plugin.py
├── tests/
│   ├── test_session.py   # Reliability tests
│   └── test_capabilities.py  # Curriculum-derived
├── .claude/skills/       # Claude Code skills
├── docs/
│   ├── QUICKSTART.md     # Bootstrap guide
│   ├── COOKBOOK.md       # Patterns and recipes
│   ├── progress/         # Learning tracking
│   └── curricula/        # Reference curricula
└── scratch/              # Ephemeral (gitignored)
```

### Bootstrap Experience

1. Clone repo
2. Run `/pymol-setup`
3. Say "load 1ubq and show me" → works

### Exit Criteria

- [ ] QUICKSTART.md written and tested
- [ ] Fresh clone → working in <5 minutes
- [ ] Skills cover common workflows
- [ ] Tests provide confidence in reliability

---

## Session Log Format

For each autonomous session:

```markdown
## Session: YYYY-MM-DD-N

### Focus
What I'm working on this session

### Completed
- Task/improvement completed
- Another thing done

### Issues Encountered
- Problem → how resolved (or noted as blocker)

### Artifacts Created
- New/updated files

### Next Session
- What to pick up next
```

---

## Current Status

**Phase:** 1 - Foundation
**Started:** 2026-01-28
