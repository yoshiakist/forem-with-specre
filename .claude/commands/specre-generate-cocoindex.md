---
description: "Generate specre cards for uncovered source files in a domain (cocoindex-powered analysis)"
---

You are executing the specre-generate-cocoindex workflow. The user has optionally provided a domain or subdirectory as `$ARGUMENTS`.

Your goal: create specre specification cards for source files that currently lack specre coverage. This variant replaces the Python discovery and map-generator scripts with SQL queries against the cocoindex PostgreSQL database, enabling richer structural analysis and semantic search.

**Model strategy:** The main agent (Opus) handles Phase 0 (setup) and Phase 3–4 (card generation and validation). Phase 1–2 (discovery and behavior classification) is delegated to an **Opus subagent** via the Task tool. This isolates the heavy discovery context (SQL results, source file reads) from the main agent, significantly reducing token consumption in later phases. Phase 3 (card generation) is further delegated to Sonnet subagents in parallel batches.

**Skill loading protocol:**
This workflow references three skill files. Each is loaded **inside the agent that needs it**, never in the main agent. Skills are also loaded **one at a time, only at the exact moment they are needed** — not all at once at startup:

- `.claude/skills/specre-cocoindex-sql-cookbook/SKILL.md` → loaded by the Phase 1–2 subagent **only when Phase 1 Step 1 begins** (not at subagent startup)
- `.claude/skills/specre-behavior-classification/SKILL.md` → loaded by the Phase 1–2 subagent **only when Phase 2 begins** (not before)
- `.claude/skills/specre-card-generation-template/SKILL.md` → read by the main agent **only when Phase 3 begins** (not before)

**Loading a skill before its phase boundary is forbidden.** Pre-loading wastes context and contaminates the agent's reasoning before the relevant work has started.

**Prerequisites:**
- cocoindex must be installed and the `CodebaseIndex` flow must have been run (see `code_index.py`).
- PostgreSQL container `cocoindex_postgres` must be running.
- All SQL queries in this workflow use `docker exec cocoindex_postgres psql -U cocoindex -d cocoindex_db -c "..."` as the execution method.

## Phase 0: Setup

1. Read `specre.toml` to determine `specre_dir` and `source_dirs`.
2. If `$ARGUMENTS` is empty, ask the user which domain or subdirectory to target.
3. Confirm the target domain with the user before proceeding.
4. Verify cocoindex is ready:
   ```bash
   docker exec cocoindex_postgres psql -U cocoindex -d cocoindex_db -c "SELECT COUNT(*) FROM codebaseindex__code_embeddings;"
   ```
   If the table does not exist or is empty, instruct the user to run:
   ```bash
   source .venv/bin/activate
   COCOINDEX_DATABASE_URL="postgresql://cocoindex:password@localhost:5432/cocoindex_db" cocoindex update -f code_index
   ```
5. Record `specre_dir`, `source_dirs`, and the target domain for use in Phase 1–2.

## Phase 1–2: Delegated Discovery & Behavior Classification

Phase 1 (Discovery) and Phase 2 (Behavior Classification) are delegated entirely to an **Opus subagent**. This isolates all SQL query results, source file reads, and structural analysis from the main agent's context.

### Dispatch the subagent

Launch a single Task subagent with the following parameters:
- `model: "opus"`
- `subagent_type: "general-purpose"`
- `description: "Phase 1-2: discovery and classification"`

Use the following prompt template, replacing all `<placeholder>` values with actual data from Phase 0:

````
You are executing Phase 1–2 of the specre-generate-cocoindex workflow. Your job is to discover domain files and classify them into user-facing behaviors, producing a behavior catalog.

## SKILL LOADING RULES — READ BEFORE ANYTHING ELSE

> **CRITICAL: Do NOT read any skill file until you reach the exact step that requires it.**

You will need exactly two skill files during this workflow. They MUST be loaded one at a time, strictly at their phase boundary:

| Skill | When to load |
|---|---|
| `.claude/skills/specre-cocoindex-sql-cookbook/SKILL.md` | **Only when you begin Phase 1, Step 1** |
| `.claude/skills/specre-behavior-classification/SKILL.md` | **Only when you begin Phase 2** |

**Prohibited actions:**
- Reading both skills at startup or at the beginning of this prompt
- Reading `specre-behavior-classification` before Phase 1 is complete
- Reading any other skill file (e.g., `specre-card-generation-template` — that skill is for Phase 3, which this subagent never executes)

Loading a skill before its phase boundary wastes context and pollutes your reasoning. Treat early skill reads as a failure of execution.

## Context

- **Target domain:** <target_domain>
- **specre_dir:** <specre_dir>
- **source_dirs:** <source_dirs>
- **SQL execution method:** `docker exec cocoindex_postgres psql -U cocoindex -d cocoindex_db -c "..."`

## Phase 1: Discovery

> **SKILL LOAD — NOW (Phase 1 boundary):** You have reached Phase 1. Read `.claude/skills/specre-cocoindex-sql-cookbook/SKILL.md` **now and only now**. Do not read `specre-behavior-classification` yet — that skill is for Phase 2 only.

Phase 1 discovers all files related to the target domain using SQL queries against the cocoindex-indexed codebase. The indexed table `codebaseindex__code_embeddings` contains every source file's content (chunked), filename, detected language, and embedding vector.

### Step 1: Discover domain files

Run a SQL query to find all files related to the target domain. The key technique is combining **inclusion patterns** with **exclusion patterns** to isolate a domain precisely.

**Basic domain query:**
```sql
SELECT DISTINCT filename
FROM codebaseindex__code_embeddings
WHERE filename ~* '<domain_keyword>'
ORDER BY filename;
```

**With exclusions** (critical for domains that share naming with sub-domains):
```sql
SELECT DISTINCT filename
FROM codebaseindex__code_embeddings
WHERE filename ~* '<domain_keyword>'
  AND filename NOT ILIKE '%<excluded_sub_domain_1>%'
  AND filename NOT ILIKE '%<excluded_sub_domain_2>%'
ORDER BY filename;
```

Refer to the **specre-cocoindex-sql-cookbook** skill for advanced pattern techniques (word-boundary regex, compound exclusions, directory scoping) and for handling very large domains (>300 files).

### Step 2: Classify discovered files by architectural layer

Use the layer distribution query from the **specre-cocoindex-sql-cookbook** skill (Query C).

### Step 3: Identify existing specre tags

Use the tag extraction query from the **specre-cocoindex-sql-cookbook** skill (Query D).

**Partition** the discovered files into three groups:
- **Untagged source files** (no `@specre` match, not under `spec/`): Candidates for NEW specre cards.
- **Untagged test files** (no `@specre` match, under `spec/`): Evidence for status determination in Phase 3.
- **Already-tagged files** (`@specre` present): Belong to existing cards. Use `specre trace` (MCP tool: mcp__specre__trace) to look up which card each belongs to.

### Step 4: Estimate complexity by chunk count

Use the complexity ranking query from the **specre-cocoindex-sql-cookbook** skill (Query E). This helps prioritize which files to analyze more deeply in Phase 2.

### Step 5: Log the discovery summary

Log the total file count, layer distribution, tagged vs. untagged breakdown, and top-complexity files. Proceed directly to Phase 2.

## Phase 2: Behavior Classification

> **SKILL LOAD — NOW (Phase 2 boundary):** You have completed Phase 1. Read `.claude/skills/specre-behavior-classification/SKILL.md` **now and only now**. Do not read any other skill file — `specre-card-generation-template` is used in Phase 3, which this subagent never executes.

**Purpose:** Build a complete picture of the domain's behaviors BEFORE creating any cards. This prevents duplicate cards, identifies cross-file behaviors, and establishes a logical generation order.

Follow the **specre-behavior-classification** skill exactly for all steps in this phase:
1. Extract structural overview from cocoindex (Step 1)
2. Use semantic search for cross-domain discovery (Step 2)
3. Group files into user-facing behaviors (Step 3)
4. Produce the behavior catalog (Step 4)
5. Validate the catalog against all 9 checks (Step 5)

## Output

Write the finalized behavior catalog to `<specre_dir>/<target_domain>/_GENERATION_PLAN.md`.

After writing the file, return a summary in this exact format:

```
PHASE_1_2_RESULT:
domain: <target_domain>
plan_path: <full path to _GENERATION_PLAN.md>
total_files: <number of discovered files>
untagged_source_files: <number>
untagged_test_files: <number>
already_tagged_files: <number>
catalog_entries: <number of behaviors in the catalog>
new_cards: <number of NEW actions>
extend_cards: <number of EXTEND actions>
```

## Rules

- **Name by observable behavior, not by code artifact.** Subject must be a human actor or `system`.
- **One behavior = one card across all layers.** A behavior spanning model, controller, frontend, worker, and view is one card.
- **Never create test files.** This workflow generates specre cards only.
- **Never modify source files** beyond inserting `@specre` markers via `specre tag`.
- **Keep cocoindex updated.** If source files have changed significantly since the last index, advise the user to run `cocoindex update code_index` before proceeding.
````

### Process the subagent result

1. Parse the `PHASE_1_2_RESULT:` block from the subagent's response.
2. Read `<specre_dir>/<domain>/_GENERATION_PLAN.md` to verify it was written correctly.
3. Log the summary to the user (total files, catalog entries, NEW vs. EXTEND counts).
4. Proceed directly to Phase 3.

## Phase 3: Delegated Card Generation

> **MANDATORY SKILL LOAD — DO NOT SKIP.** You are now entering Phase 3. Read the `specre-card-generation-template` skill at `.claude/skills/specre-card-generation-template/SKILL.md` **now** (not before this point). This step is non-optional; skipping it will produce subagent prompts that lack the required structure and result format.

**Model strategy:** Phase 3 is structured execution following the catalog, so each card is delegated to a **Sonnet subagent** via the Task tool (`model: "sonnet"`, `subagent_type: "general-purpose"`).

Before starting, create a TodoWrite entry for each catalog item. If context compression occurs, re-read `<specre_dir>/<domain>/_GENERATION_PLAN.md` and the current TodoWrite state to recover your position.

Follow the **specre-card-generation-template** skill for:
- Retrieving code text for each subagent
- Constructing the subagent prompt from the template
- Dispatching subagents in parallel batches of up to 3
- Collecting and validating results after each batch

## Phase 4: Validation and Review

After all catalog entries are processed:

1. Delete `<specre_dir>/<domain>/_GENERATION_PLAN.md`.
2. Run `specre index` to regenerate the index.
3. Run `specre orphans` to verify no unlinked cards or dangling markers.
4. Run `specre coverage` and report the coverage change (before vs. after).
5. Present a summary to the user:

```
Generation complete.

Created: N new specre cards
Extended: M existing specre cards
Coverage: X% → Y%

Cards marked stable (auto-stabilized from tests):
  - docs/specres/domain/behavior_a.md
  - docs/specres/domain/behavior_b.md

Cards remaining as draft:
  - docs/specres/domain/behavior_c.md (no matching tests)
  - docs/specres/domain/behavior_d.md (test scenarios diverge)
```

6. **If any cards were auto-stabilized**, append this notice:

> Some cards were automatically set to `stable` because matching tests were found and their assertions align with the documented scenarios. We recommend reviewing these cards to confirm that the specification accurately reflects the intended behavior, not just the current implementation.

## Rules

- **Autonomous within phases.** Do not pause for user input between individual card generations in Phase 3.
- **Delegate Phase 1–2 to Opus subagent.** Always use `model: "opus"` and `subagent_type: "general-purpose"`.
- **Delegate Phase 3 to Sonnet.** Always use `model: "sonnet"` and `subagent_type: "general-purpose"`.
- **Follow the specre-author skill.** Load and follow the specre-author skill for all naming conventions and writing guidelines.
- **Name by observable behavior, not by code artifact.** Subject must be a human actor or `system`.
- **One behavior = one card across all layers.** A behavior spanning model, controller, frontend, worker, and view is one card.
- **Write in natural language.** Scenarios must not be code.
- **Never create test files.** This workflow generates specre cards only.
- **Never modify source files** beyond inserting `@specre` markers via `specre tag`.
- **`.jbuilder` files are not taggable.** Include in Related Files but skip `specre tag`.
- **Keep cocoindex updated.** If source files have changed significantly since the last index, advise the user to run `cocoindex update code_index` before proceeding.
- **Skill loads are strictly deferred.** The Phase 1–2 skill files are loaded inside the subagent. The Phase 3 skill file is loaded by the main agent only when Phase 3 begins. Do NOT pre-read any skill file before its phase boundary.
