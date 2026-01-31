# `x_docs/`

Working documentation folder — a scratch space for notes, specs, and handover files used during development with Claude Code.

Not part of the project's source code or official documentation. Contents may be messy, incomplete, or temporary.

To exclude from Claude Code, add these to the deny list in `.claude/settings.json`:

```json
"Read(x_docs/**)", "Grep(x_docs/**)", "Glob(x_docs/**)", "Edit(x_docs/**)"
```
