# Cat Facts CLI

![Banner showing a cat terminal icon with the text "CLI for Claude Code on the Cat Facts API — A learning project"](x_docs/images/readme-banner.jpg)

A CLI tool that wraps the [Cat Facts API](https://github.com/alexwohlbruck/cat-facts/), designed to be invoked by [Claude Code](https://claude.ai/code) as a shell command. Built as a learning project to explore creating CLI tools that Claude Code can use — a lightweight alternative to building an MCP server. Perhaps more effective - we'll see.

## Why?

Many apps have APIs — Gmail ([REST API](https://developers.google.com/gmail/api)), Microsoft Outlook ([Microsoft Graph](https://learn.microsoft.com/en-us/graph/overview)), [Gamma](https://developers.gamma.app/docs/getting-started), etc. Some have official MCPs, some don't. Either way, writing a small CLI to wrap the API directly may be simpler and more effective.

Why not create an MCP instead of a CLI?

An MCP is itself a wrapper on an API — an extra layer of indirection. Tool definitions and intermediate results flow through the context window, flooding it if you have not used a subagent.

A CLI skips all of that. Claude Code just runs a command and reads stdout — no protocol layer, no tool schemas, no discovery handshake. And Claude Code is already very good with CLIs and Bash.

**Hypothesis:** I think Claude Code will be more effective with a CLI for the tools I want to use.

## Setup

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/) and Python 3.14+.

```bash
git clone https://github.com/michellepace/cat-facts-cli.git
cd cat-facts-cli
uv sync
uv run pre-commit install
```

## References

[Code execution with MCP: Building more efficient agents | Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)

## Personal Notes

<personal_notes>

**The CLI-for-Claude-Code Concept**

Claude Code runs your CLI as a shell command and reads stdout. The flow is: user asks Claude a question → Claude decides it needs data → runs `cat-facts random --type cat` → reads the JSON output → uses it to answer. Your CLI is a translator between Claude Code and the API.

**It's NOT a 1:1 Mapping — You're Right**

A good CLI wrapper exposes use cases, not endpoints. Key principles:

1. Use cases, not routes — `cat-facts random` not `cat-facts get-random-fact`. Hide the API structure.
2. JSON output by default — Claude Code parses JSON far better than prose. Add a `--human` flag for people.
3. Combine API calls — One CLI command can make multiple API calls, merge results, add computed fields.
4. Good `--help` text — Claude Code reads `--help` to discover what your CLI can do. Write it for a developer audience.
5. Errors on stderr, data on stdout — So Claude can distinguish success from failure.

**Why Cat Facts Is Limited**

It's not just "fewer endpoints." Without auth, you can only read facts. You can't practise:

- Write operations (`cat-facts submit "Dogs wag tails" --type dog`)
- CRUD patterns (create/update/delete)
- Confirmation prompts ("Delete this? [y/N]")
- Multi-step workflows
- Session management

The Google OAuth flow could be implemented in the CLI (like `gh auth login` does), but that's a significant undertaking for a learning project.

**Other CLI ideas**

[Free APIs](https://free-apis.github.io/):

- Documents & Productivity: I love PDF
- Business: Logo dev
- Universities
- Transportation: (looking for flights)
- Food & Drink: Whiskey Hunter

**End Target:** Gamma, Outlook email traiage al la Claude Code

</personal_notes>

## Validation Principles

See [Validation Principles](x_docs/validation.md) for the full testing and verification strategy.
