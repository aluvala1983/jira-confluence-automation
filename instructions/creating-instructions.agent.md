# Creating and Maintaining Project Instructions

Keep reusable workflow guidance platform-neutral in `instructions/`; use IDE-specific files only as thin adapters that point to the canonical instruction.

## Creating or Updating an Instruction

- Keep each instruction focused on one workflow and write it in actionable English.
- Before editing an existing instruction, read it and preserve useful guidance; make targeted changes rather than rewriting unrelated content.
- Prefer concise steps, explicit constraints, and useful examples. Avoid duplicating shared guidance.
- Use verb-first, hyphen-separated filenames with the `.agent.md` extension.
- Do not add IDE-specific frontmatter to canonical instruction files.
- Do not invent facts or silently change expected behavior.

## Catalog and Integration

- Add every canonical instruction to `instructions/main.agent.md` with its relative link, a one-line description, and useful routing keywords.
- For VS Code with GitHub Copilot, add a prompt under `.github/prompts/` that points to the canonical instruction.
- Keep `.github/copilot-instructions.md` as the entry point that tells Copilot to load the complete `instructions/main.agent.md` catalog on every prompt.
- Enable Copilot instruction-file support in `.vscode/settings.json`; preserve existing settings when updating it.
- Do not create integration files for other IDEs unless requested or already part of the project setup.

## Validation

- Verify all catalog and adapter links resolve to existing files.
- Check JSON settings syntax and YAML frontmatter when native adapter files use frontmatter.
- Confirm the adapter delegates to the canonical instruction instead of duplicating its rules.
