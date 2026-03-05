# CLAUDE.md — forem

## What is specre?

Atomic, living specification cards for AI-agent-friendly development. A Rust CLI toolkit for Spec-Driven Development (SDD). Each specre is a single Markdown file describing exactly one behavior, with YAML front-matter for lifecycle tracking and bidirectional traceability.

**Core philosophy:** One specre card = one behavior. Sized for a single LLM context window.

## CLI Commands

| Command | Status | Description |
|---------|--------|-------------|
| `specre init` | Implemented | Initialize project (creates `specre.toml` and specre directory) |
| `specre new <dir> --name <name>` | Implemented | Scaffold a new specre card with auto-generated ULID |
| `specre index` | Implemented | Generate `index.json` and per-domain `_INDEX.md` |
| `specre status` | Implemented | Report specre counts by status, flag stale `last_verified` |
| `specre trace` | Implemented | Bidirectional traceability lookup by ULID or file path |
| `specre orphans` | Implemented | Detect unlinked specres or dangling markers |
| `specre tag` | Implemented | Insert `@specre` markers into source files |
| `specre search` | Implemented | Full-text + filter search with JSON output |
| `specre coverage` | Implemented | Report percentage of source files covered by `@specre` tags |
| `specre health-check` | Implemented | Comprehensive health check for AI agent preflight |
| `specre mcp` | Implemented | Start MCP server (stdio transport) |
| `specre drift` | Not yet | Detect drift between spec and implementation |
| `specre ci` | Not yet | CI integration (non-zero exit on drift/orphans) |
