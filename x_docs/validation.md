# Validation Principles

> When building the CLI with Claude Code (for Claude Code), how do I build in testing and verification so Claude Code can check itself as it builds?

The unique thing about this project: **Claude Code is both the builder and the consumer.** Validation isn't just "do the tests pass?" — it's "can Claude Code actually use what it just built?"

Six layers, from foundational to advanced:

<details>
<summary><h2>🟣 Layer 1: TDD (pytest)</h2></summary>

Write tests first. They verify the code logic works. Pre-commit hooks run them on every commit.

```bash
uv run pytest                              # Does the code work?
uv run pre-commit run --all-files          # Does it pass all quality checks?
```

This is the foundation — every other layer builds on it.

</details>

<details>
<summary><h2>🟣 Layer 2: Smoke Tests — Run the CLI After Every Change</h2></summary>

After modifying any command, Claude Code should **immediately run the CLI** and check the output. Not via pytest — literally run the built CLI:

```bash
uv run cat-facts random                          # Does it produce output?
uv run cat-facts random --type dog --count 3     # Do flags work?
uv run cat-facts random --help                   # Is help text useful?
uv run cat-facts get nonexistent-id              # Does error handling work?
```

This catches issues that unit tests miss: broken entry points, import errors, typos in Typer decorators, unhelpful error messages.

**CLAUDE.md directive:**

```
After modifying any CLI command, run it with representative inputs and verify:
1. The command produces valid JSON on stdout
2. --help text is clear and complete
3. Error cases print to stderr and return non-zero exit code
```

</details>

<details>
<summary><h2>🟣 Layer 3: Schema Validation — Does the Output Have the Right Shape?</h2></summary>

Define expected JSON output shapes in pytest. Verify the CLI output matches after changes.

```python
def test_random_output_shape(capsys):
    """CLI random command returns expected JSON shape."""
    result = runner.invoke(app, ["random"])
    data = json.loads(result.stdout)
    assert "text" in data
    assert "type" in data
    assert data["type"] in ("cat", "dog", "snail", "horse")
```

This catches regressions where a refactor accidentally changes the output structure — which would break Claude Code's ability to parse it.

</details>

<details>
<summary><h2>🟣 Layer 4: Scenarios File — Behaviour-Driven Validation</h2></summary>

A `scenarios.md` file describes expected CLI behaviours in a structured, readable format. Think of it as BDD (Behaviour-Driven Development) written for Claude Code to execute.

### Why a Scenarios File?

- **Tests verify code logic.** Scenarios verify **behaviour from the user's perspective.**
- **Tests are in Python.** Scenarios are in plain English — readable by anyone, executable by Claude Code.
- **Tests run automatically.** Scenarios are a checklist Claude Code works through after completing a feature.

The scenarios file is not a replacement for pytest. It's a complement — a higher-level verification that the CLI does what a user (or Claude Code) would expect.

### Structure

Each scenario has four parts:

```markdown
## Scenario: [descriptive name]
Command: [exact shell command to run]
Expected:
- [observable outcome 1]
- [observable outcome 2]
Why: [what this validates — helps Claude Code understand the intent]
```

### Complete Example

See [scenarios.md](scenarios.md) for the full set of scenarios. Here are a few illustrative ones:

**Happy path:**

```markdown
## Scenario: Get a random cat fact (default)

Command: `uv run cat-facts random`
Expected:
- Exit code 0
- stdout is valid JSON (parseable with `json.loads`)
- JSON object has keys: `text`, `type`, `id`
- `type` is `"cat"` (the default when no `--type` flag is given)
- `text` is a non-empty string
Why: This is the most basic use case. If this doesn't work, nothing does.
```

**Flags working together:**

```markdown
## Scenario: Get multiple facts for a specific animal

Command: `uv run cat-facts random --type dog --count 3`
Expected:
- Exit code 0
- stdout is a JSON array with exactly 3 items
- Each item has keys: `text`, `type`, `id`
- Each item's `type` is `"dog"`
Why: Validates that `--type` and `--count` flags work together correctly.
```

**Error handling:**

```markdown
## Scenario: Get fact by invalid ID

Command: `uv run cat-facts get nonexistent-id-12345`
Expected:
- Exit code 1
- stderr contains "not found" or similar
- stdout is empty (no partial data)
Why: Validates error handling for missing resources.
```

**Discoverability:**

```markdown
## Scenario: Help text is discoverable

Command: `uv run cat-facts --help`
Expected:
- Lists all available commands with one-line descriptions
- Shows project description
Why: Claude Code reads `--help` to discover what a CLI can do. If help text is
poor, Claude Code can't use the CLI effectively.
```

### How Claude Code Uses This

Add to CLAUDE.md:

```
After completing a feature, read x_docs/scenarios.md and verify all relevant
scenarios pass by running the commands and checking the expected outcomes.
```

</details>

<details>
<summary><h2>🟣 Layer 5: Agentic Self-Testing — Claude Code as Consumer</h2></summary>

This is the most novel layer. After building a feature, Claude Code should **use the CLI the way it would in production** — not just verify it works, but verify it's *useful*.

### The Problem Standard Tests Don't Catch

A command can pass every test and still be useless:

```bash
# Technically correct output:
$ uv run cat-facts random
{"_id": "591f98803b90f7150a19c229", "v": 0, "__v": 0, "text": "Cats sleep 70% of their lives.", "src": "api", "upd": "2018-01-04T01:10:54.673Z", "tp": "cat", "sts": {"v": true, "c": 1}, "usr": "5a9ac18c7478810ea6c06381", "del": false}

# This is parseable JSON and has the fact text. But:
# - Field names are cryptic (tp? sts? v? c?)
# - Includes internal DB fields (_id, __v, del, usr)
# - Claude Code would struggle to know which fields matter
```

A better output:

```bash
$ uv run cat-facts random
{"text": "Cats sleep 70% of their lives.", "type": "cat", "id": "591f98803b90f7150a19c229"}
```

Unit tests can't easily catch this difference. Both outputs are valid JSON with the required keys. But one is far more useful to Claude Code.

### The Self-Test Protocol

After building or modifying a command, Claude Code should:

**Step 1: Run the command**

```bash
uv run cat-facts random --type dog --count 2
```

**Step 2: Read the output as if it were a consumer**

Ask: "A user asked me: 'Tell me some dog facts.' Can I answer well with this output?"

Check:

- Are the field names self-explanatory? Would another developer (or AI) know what each field means without reading the code?
- Is there enough information? If the user asked a follow-up ("Which fact is that?"), could I reference a specific fact by ID?
- Is there unnecessary noise? Internal fields, metadata, or formatting that adds no value?
- Is the output structure consistent? Does `--count 1` return the same shape as `--count 3`?

**Step 3: Try edge cases as a consumer**

- "What animal facts do you have?" → run `uv run cat-facts random --type cat`, then `--type dog`, etc. Does the output distinguish them?
- "Tell me fact abc123 again" → run `uv run cat-facts get abc123`. Does the output match what `random` returned earlier?
- "Give me ALL the cat facts" → run `uv run cat-facts random --count 500`. Does the output stay manageable?

**Step 4: Verify error messages are useful**

- "Tell me a unicorn fact" → run `uv run cat-facts random --type unicorn`. Does the error message tell Claude Code what values ARE valid?
- "Get fact xyz" → run `uv run cat-facts get nonexistent`. Does the error say "not found" clearly, or does it dump a traceback?

### What Makes This Different from Scenarios?

Scenarios are **scripted** — specific commands with specific expected outcomes. Agentic self-testing is **exploratory** — Claude Code freely uses the CLI and assesses whether the experience is good.

Think of it this way:

- **Scenarios** = acceptance tests (do the specified behaviours work?)
- **Agentic self-test** = usability testing (is this actually pleasant/effective to use?)

### CLAUDE.md Directive

```
## Self-Test Protocol

After building or modifying a CLI command:
1. Run the command with typical inputs
2. Read the output as a consumer — ask "Could I answer a user's question with this?"
3. Try 2-3 edge cases (missing data, invalid input, large output)
4. Verify error messages tell the caller what went wrong AND what to do instead
5. If any step reveals a problem, fix it before marking the task complete
```

</details>

<details>
<summary><h2>🟣 Layer 6: Contract Testing Against the Live API</h2></summary>

Since the CLI wraps a real API, you need to verify the API actually returns what you expect. This is different from unit tests (which can mock the API):

```python
# tests/test_integration.py (run manually, not in pre-commit)
@pytest.mark.integration
def test_live_api_random_fact():
    """Verify the live API returns expected shape."""
    response = httpx.get("https://catfacts.wohlbruck.dev/facts/random")
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
```

Run these separately from unit tests (they depend on network):

```bash
uv run pytest -m integration    # Only when checking API compatibility
```

</details>

## 🟢 Summary: The Validation Stack

| Layer | What It Validates | When | How |
|-------|-------------------|------|-----|
| **1. TDD** | Code logic works | Every commit | `uv run pytest` (pre-commit) |
| **2. Smoke test** | CLI runs and produces output | After every change | Run CLI manually |
| **3. Schema** | Output has correct shape | In pytest suite | Assert on JSON keys/types |
| **4. Scenarios** | Expected behaviours work | After features | Run through `scenarios.md` |
| **5. Agentic self-test** | Output is *useful* to Claude Code | After features | Use CLI as a consumer |
| **6. Contract tests** | Live API matches expectations | Periodically | `pytest -m integration` |
