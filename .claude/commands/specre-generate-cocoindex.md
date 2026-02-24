---
description: "Generate specre cards for uncovered source files in a domain (cocoindex-powered analysis)"
---

You are executing the specre-generate-cocoindex workflow. The user has optionally provided a domain or subdirectory as `$ARGUMENTS`.

Your goal: create specre specification cards for source files that currently lack specre coverage. This variant replaces the Python discovery and map-generator scripts with SQL queries against the cocoindex PostgreSQL database, enabling richer structural analysis and semantic search.

**Model strategy:** The main agent (Opus) handles Phase 0–2 (discovery and behavior classification — creative work requiring judgment) and Phase 4 (validation). Phase 3 (card generation — structured execution) is delegated to Sonnet subagents in parallel batches. This reduces cost and latency while preserving quality where it matters most.

**Skill loading protocol — STRICTLY DEFERRED:**
This workflow references three skill files. You MUST NOT read any of them until the specific phase that requires it. Do NOT pre-load, pre-read, or "skim" skill files at the start of the workflow. Each skill file is loaded exactly once, at the phase boundary where its `MANDATORY SKILL LOAD` directive appears. Reading a skill file before reaching its phase wastes context window space and degrades performance in later phases.

- `.claude/skills/specre-cocoindex-sql-cookbook/SKILL.md` → read only when you reach **Phase 1**
- `.claude/skills/specre-behavior-classification/SKILL.md` → read only when you reach **Phase 2**
- `.claude/skills/specre-card-generation-template/SKILL.md` → read only when you reach **Phase 3**

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

## Phase 1: Discovery

> **MANDATORY SKILL LOAD — DO NOT SKIP.** You are now entering Phase 1. Read the `specre-cocoindex-sql-cookbook` skill at `.claude/skills/specre-cocoindex-sql-cookbook/SKILL.md` **now** (not before this point). This step is non-optional; skipping it will produce incorrect domain isolation queries and miss edge cases for large domains.

Phase 1 replaces the `domain-discovery.py` script with SQL queries against the cocoindex-indexed codebase. The indexed table `codebaseindex__code_embeddings` contains every source file's content (chunked), filename, detected language, and embedding vector.

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
- **Already-tagged files** (`@specre` present): Belong to existing cards. Use `specre trace` to look up which card each belongs to.

### Step 4: Estimate complexity by chunk count

Use the complexity ranking query from the **specre-cocoindex-sql-cookbook** skill (Query E). This helps prioritize which files to analyze more deeply in Phase 2.

### Step 5: Log the discovery summary and proceed

Log the total file count, layer distribution, tagged vs. untagged breakdown, and top-complexity files. Proceed directly to Phase 2 without pausing for user approval.

## Phase 2: Behavior Classification

> **MANDATORY SKILL LOAD — DO NOT SKIP.** You are now entering Phase 2. Read the `specre-behavior-classification` skill at `.claude/skills/specre-behavior-classification/SKILL.md` **now** (not before this point). This step is non-optional; skipping it will produce cards that are incorrectly scoped by code layer instead of by observable behavior, miss the 9-point validation checklist, and use prohibited naming patterns.

**Purpose:** Build a complete picture of the domain's behaviors BEFORE creating any cards. This prevents duplicate cards, identifies cross-file behaviors, and establishes a logical generation order.

Follow the **specre-behavior-classification** skill exactly for all steps in this phase:
1. Extract structural overview from cocoindex (Step 1)
2. Use semantic search for cross-domain discovery (Step 2)
3. Group files into user-facing behaviors (Step 3)
4. Produce the behavior catalog (Step 4)
5. Validate the catalog against all 9 checks (Step 5)

If the catalog passes all checks, proceed directly to Phase 3 without pausing for user approval.

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
- **Delegate Phase 3 to Sonnet.** Always use `model: "sonnet"` and `subagent_type: "general-purpose"`.
- **Follow the specre-author skill.** Load and follow the specre-author skill for all naming conventions and writing guidelines.
- **Name by observable behavior, not by code artifact.** Subject must be a human actor or `system`.
- **One behavior = one card across all layers.** A behavior spanning model, controller, frontend, worker, and view is one card.
- **Write in natural language.** Scenarios must not be code.
- **Never create test files.** This workflow generates specre cards only.
- **Never modify source files** beyond inserting `@specre` markers via `specre tag`.
- **`.jbuilder` files are not taggable.** Include in Related Files but skip `specre tag`.
- **Keep cocoindex updated.** If source files have changed significantly since the last index, advise the user to run `cocoindex update code_index` before proceeding.
- **Skill loads are mandatory and strictly deferred.** Every `MANDATORY SKILL LOAD` directive in this workflow MUST be executed — but only when that phase is reached. Do NOT pre-read or pre-load any skill file before arriving at its phase boundary. Reading skills early wastes context window space and causes instructions in later phases to be ignored.
