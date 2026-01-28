---
name: Skill Development
description: This skill should be used when the user asks to "create a skill", "build a skill", "develop a skill for Claude Code", or mentions "skill structure", "SKILL.md", or "progressive disclosure".
version: 0.1.0
---

# Skill Development for Claude Code Plugins

This skill provides guidance for creating effective skills for Claude Code plugins.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. They transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex tasks

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

- **SKILL.md** (required) - Contains YAML frontmatter metadata and markdown instructions
- **scripts/** (optional) - Executable code for deterministic tasks
- **references/** (optional) - Documentation loaded as needed into context
- **assets/** (optional) - Files used in output like templates or icons

## Skill Creation Process

### Step 1: Understanding Concrete Examples

Identify concrete examples of how the skill will be used. Ask clarifying questions about functionality and usage patterns. Conclude when there is clear understanding of what the skill should support.

### Step 2: Planning Reusable Contents

Analyze each example to identify what scripts, references, and assets would help when executing workflows repeatedly. Create a list of reusable resources needed.

### Step 3: Create Skill Structure

For Claude Code plugins, create the skill directory structure:

```bash
mkdir -p plugin-name/skills/skill-name/{references,examples,scripts}
touch plugin-name/skills/skill-name/SKILL.md
```

### Step 4: Edit the Skill

**Writing Style:** Use imperative/infinitive form (verb-first instructions), not second person. Write objectively and instructionally.

**Description:** Use third-person format with specific trigger phrases showing when the skill should be used.

**Body Content:** Keep SKILL.md lean (1,500-2,000 words). Move detailed content to references/.

### Step 5: Validate and Test

Check structure, SKILL.md validity, trigger phrases, writing style, progressive disclosure, and ensure all referenced files exist.

### Step 6: Iterate

Use the skill on real tasks and improve based on what works well and what struggles occur.

## Plugin-Specific Considerations

### Skill Location

Plugin skills live in the plugin's `skills/` directory and are automatically discovered by Claude Code.

### Auto-Discovery

Claude Code scans the `skills/` directory, finds subdirectories containing SKILL.md, loads metadata always, and loads body and references when needed.

### No Packaging Required

Plugin skills are distributed as part of the plugin. Users get skills when they install the plugin.

## Writing Style Requirements

### Imperative/Infinitive Form

Write using verb-first instructions:
- "To create a hook, define the event type"
- "Configure the MCP server with authentication"
- NOT "You should create..." or "You need to..."

### Third-Person in Description

Use third person in frontmatter: "This skill should be used when the user asks to..."

### Objective Language

Focus on what to do: "Parse the frontmatter using sed" rather than "You can parse..."

## Best Practices

**DO:**
- Use third-person in description
- Include specific trigger phrases
- Keep SKILL.md lean (1,500-2,000 words)
- Use progressive disclosure
- Write in imperative form
- Reference supporting files clearly
- Provide working examples
- Create utility scripts for common operations

**DON'T:**
- Use second person anywhere
- Have vague trigger conditions
- Put everything in SKILL.md
- Leave resources unreferenced
- Include broken examples
- Skip validation

## Additional Resources

Study existing plugin-dev skills as templates:
- `hook-development/` - Progressive disclosure, utilities
- `agent-development/` - AI-assisted creation
- `plugin-settings/` - Real-world examples
