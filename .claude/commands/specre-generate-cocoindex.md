---
description: "Generate specre cards for uncovered source files in a domain (cocoindex-powered analysis)"
---

You are executing the specre-generate-cocoindex workflow. The user has optionally provided a domain or subdirectory as `$ARGUMENTS`.

Your goal: create specre specification cards for source files that currently lack specre coverage. This variant replaces the Python discovery and map-generator scripts with SQL queries against the cocoindex PostgreSQL database, enabling richer structural analysis and semantic search.

**Model strategy:** The main agent (Opus) handles Phase 0–2 (discovery and behavior classification — creative work requiring judgment) and Phase 4 (validation). Phase 3 (card generation — structured execution) is delegated to Sonnet subagents in parallel batches. This reduces cost and latency while preserving quality where it matters most.

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

#### SQL pattern techniques for domain isolation

Choose the right pattern operator depending on the precision needed:

| Technique | SQL | Use case |
|---|---|---|
| Simple substring | `filename ILIKE '%tag%'` | Broad match — catches `tag`, `tags`, `tagging`, `tag_adjustment` |
| Word-boundary regex | `filename ~* '(^|/)tags?[_/.]'` | Precise — matches `tag.rb`, `tags_controller.rb` but not `liquid_tag` |
| Multi-keyword AND | `filename ~* 'tag' AND filename ~* 'moderator'` | Intersection — files that involve both concepts |
| Compound exclusion | `AND filename NOT ILIKE '%liquid_tag%'` | Filter out a known sub-domain |
| Directory scoping | `AND (filename LIKE 'app/%' OR filename LIKE 'spec/%')` | Restrict to specific source directories |
| Extension filtering | `AND filename ~ '\.(rb|js|jsx)$'` | Limit to specific file types |

**Common exclusion patterns for large domains:**

When a domain keyword appears in multiple qualitatively different sub-domains (e.g., `tag` appears in `tags`, `liquid_tags`, `tag_adjustments`, `tag_moderators`), build exclusions systematically:

```sql
-- Step 1: Identify all sub-domain patterns first
SELECT
  CASE
    WHEN filename ~* 'liquid_tag' THEN 'liquid_tags'
    WHEN filename ~* 'tag_adjustment' THEN 'tag_adjustments'
    WHEN filename ~* 'tag_moderator' THEN 'tag_moderators'
    WHEN filename ~* 'tag_subforem' THEN 'tag_subforem'
    ELSE 'tag_core'
  END AS subdomain,
  COUNT(DISTINCT filename) AS file_count
FROM codebaseindex__code_embeddings
WHERE filename ~* 'tag'
GROUP BY subdomain
ORDER BY file_count DESC;

-- Step 2: Target only the desired sub-domain
SELECT DISTINCT filename
FROM codebaseindex__code_embeddings
WHERE filename ~* '(^|/)tags?[_/.]'
  AND filename NOT ILIKE '%liquid_tag%'
ORDER BY filename;
```

#### Handling very large domains (>300 files)

If the initial query returns more than 300 distinct files, do NOT attempt to process the full domain. Instead:

1. Run the sub-domain breakdown query (the Step 1 CASE query above) to identify natural splits.
2. Present the sub-domain split to the user with file counts.
3. Stop execution. The user will run `/specre-generate-cocoindex <sub-domain>` for each independently.

### Step 2: Classify discovered files by architectural layer

```sql
SELECT
  CASE
    WHEN filename LIKE 'app/models/%' THEN 'Models'
    WHEN filename LIKE 'app/controllers/admin/%' THEN 'Admin Controllers'
    WHEN filename LIKE 'app/controllers/api/%' THEN 'API Controllers'
    WHEN filename LIKE 'app/controllers/concerns/%' THEN 'Controller Concerns'
    WHEN filename LIKE 'app/controllers/%' THEN 'Controllers'
    WHEN filename LIKE 'app/services/%' THEN 'Services'
    WHEN filename LIKE 'app/policies/%' THEN 'Policies'
    WHEN filename LIKE 'app/views/%' THEN 'Views'
    WHEN filename LIKE 'app/workers/%' THEN 'Workers'
    WHEN filename LIKE 'app/lib/%' THEN 'Lib'
    WHEN filename LIKE 'app/decorators/%' THEN 'Decorators'
    WHEN filename LIKE 'app/queries/%' THEN 'Queries'
    WHEN filename LIKE 'app/sanitizers/%' THEN 'Sanitizers'
    WHEN filename LIKE 'app/serializers/%' THEN 'Serializers'
    WHEN filename LIKE 'app/uploaders/%' THEN 'Uploaders'
    WHEN filename LIKE 'app/assets/%' OR filename LIKE 'app/javascript/%' THEN 'Frontend (JS/JSX)'
    WHEN filename LIKE 'spec/%' THEN 'Specs'
    ELSE 'Other'
  END AS layer,
  COUNT(DISTINCT filename) AS file_count
FROM codebaseindex__code_embeddings
WHERE <domain_filter>  -- reuse the WHERE clause from Step 1
GROUP BY layer
ORDER BY file_count DESC;
```

### Step 3: Identify existing specre tags

Query the indexed text to find files that already have `@specre` markers:

```sql
SELECT DISTINCT filename,
  (regexp_matches(text, '@specre\s+([A-Z0-9]{26})', 'g'))[1] AS ulid
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND text ~ '@specre\s+[A-Z0-9]{26}';
```

**Partition** the discovered files into three groups:
- **Untagged source files** (no `@specre` match, not under `spec/`): Candidates for NEW specre cards.
- **Untagged test files** (no `@specre` match, under `spec/`): Evidence for status determination in Phase 3.
- **Already-tagged files** (`@specre` present): Belong to existing cards. Use `specre trace` to look up which card each belongs to.

### Step 4: Estimate complexity by chunk count

Chunk count serves as a proxy for file complexity — more chunks = larger/more complex file:

```sql
SELECT filename, COUNT(*) AS chunks,
  string_agg(DISTINCT language, ', ') AS lang
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND filename NOT LIKE 'spec/%'
GROUP BY filename
ORDER BY chunks DESC
LIMIT 20;
```

This helps prioritize which files to analyze more deeply in Phase 2.

### Step 5: Log the discovery summary and proceed

Log the total file count, layer distribution, tagged vs. untagged breakdown, and top-complexity files. Proceed directly to Phase 2 without pausing for user approval.

## Phase 2: Behavior Classification

**Purpose:** Build a complete picture of the domain's behaviors BEFORE creating any cards. This prevents duplicate cards, identifies cross-file behaviors, and establishes a logical generation order.

> **Prerequisite — load the specre-author skill.** Before classifying behaviors, read the specre-author skill (`SKILL.md`) to internalize naming conventions and writing guidelines. Every proposed card name MUST follow the subject + predicate sentence form defined there. Violations of naming conventions are the most common defect in generated cards.

> **Core principle — classify by observable behavior, not by code layer.** A specre card describes a behavior as experienced by a human user, or as observable at a system boundary. A single behavior typically spans multiple code layers — model, controller, service, frontend component, worker, and view template all participate in the same behavior. Do NOT create separate cards per layer.
>
> **Multiple markers per file are the norm.** A single source file (especially controllers and models) typically participates in multiple behaviors and therefore receives multiple `@specre` markers — one per behavior it contributes to. For example, a `CommentsController` handling `create`, `update`, and `destroy` actions would carry three separate `@specre` markers, each linking to a different specre card. Do not assume one-file-one-marker; the number of markers on a file should correspond to the number of distinct behaviors it implements.
>
> **Litmus test:** "If a system implemented exactly this behavior and nothing else, would it deliver value to a user?" If not, the card describes an implementation fragment.
>
> **`manage` verb prohibition:** Never use `manage`/`manages`/`managing` in card names. Decompose into specific action verbs: `view`, `create`, `edit`, `delete`, etc.

### Step 1: Extract structural overview from cocoindex

Instead of running map-generator scripts, retrieve the code text directly from cocoindex. The indexed chunks contain the full source, making structural analysis possible via SQL.

**Retrieve model structure** (associations, validations, scopes — the domain's data model is the best starting point):

```sql
SELECT filename, text
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND filename LIKE 'app/models/%'
ORDER BY filename, location;
```

**Retrieve controller actions** (what user-facing operations exist):

```sql
SELECT filename, text
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND (filename LIKE 'app/controllers/%')
  AND filename NOT LIKE 'spec/%'
ORDER BY filename, location;
```

**Retrieve service/worker logic** (system-initiated behaviors):

```sql
SELECT filename, text
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND (filename LIKE 'app/services/%' OR filename LIKE 'app/workers/%')
ORDER BY filename, location;
```

> **Token efficiency:** For large domains, avoid retrieving ALL chunks for ALL files. Start with models and controllers (the behavior boundaries), then selectively query services/workers/views only for files referenced by the behaviors you identify. Use the chunk count from Phase 1 Step 4 to gauge which files are worth retrieving in full.

> **When to fall back to Read tool:** If a file's indexed chunks are incomplete or the chunking splits critical logic across boundaries, use the Read tool to read the original file. This should be rare — most structural analysis can be done from the indexed text.

### Step 2: Use semantic search for cross-domain discovery

This is a capability unique to cocoindex — use vector similarity to find related code that conventional grep-based discovery would miss.

**Find files semantically similar to a domain concept:**

```sql
SELECT filename, text,
  1 - (embedding <=> (
    SELECT embedding FROM codebaseindex__code_embeddings
    WHERE filename = 'app/models/<domain>.rb'
    ORDER BY location LIMIT 1
  )) AS similarity
FROM codebaseindex__code_embeddings
WHERE filename NOT LIKE 'spec/%'
  AND filename != 'app/models/<domain>.rb'
ORDER BY embedding <=> (
  SELECT embedding FROM codebaseindex__code_embeddings
  WHERE filename = 'app/models/<domain>.rb'
  ORDER BY location LIMIT 1
)
LIMIT 20;
```

This can surface files that are conceptually related to the domain model even if they don't contain the domain keyword in their filename — e.g., a shared utility used primarily by this domain, or a concern mixed into the domain model.

**Evaluate whether cross-domain hits are relevant:** Not all semantically similar files belong to this domain. Files with similarity < 0.5 are unlikely to be relevant. Files from clearly different domains (e.g., a user model appearing similar to an article model because both use `acts_as_followable`) should be excluded.

### Step 3: Group files into user-facing behaviors

After analyzing the structural data, shift perspective from individual files to **observable behaviors**:

1. "What can a human user do in this domain?" → `user_can_*`, `admin_can_*`, `author_can_*`
2. "What does the system do autonomously?" → `system_*`

Assign each file to the behavior it participates in. A model + controller + frontend + view that all contribute to one user action belong to **one** behavior.

### Step 4: Produce the behavior catalog

Produce a **behavior catalog** — a numbered list of proposed specre cards:

```
Behavior Catalog for domain: <domain>

 1. [subject]_[predicate]
    Source files: src/domain/file_a.ext, src/domain/file_b.ext
    Test files: spec/domain/file_a_spec.rb
    Template files: app/views/domain/_partial.html.erb
    Action: NEW — no existing specre covers this behavior

 2. [subject]_[predicate]
    Source files: src/domain/file_c.ext
    Action: EXTEND — add to existing specre [ULID] ([existing_name])

 3. ...
```

Each entry must specify:
- **Proposed name**: subject + predicate sentence form (see specre-author skill)
- **Source files**: which files this card will cover (files from multiple layers)
  - For untagged files: plain path
  - For already-tagged files: path + `(Tagged: ULID)` suffix
- **Test files** (if any): corresponding test/spec files
- **Template files** (if any): associated view/template files (`.erb`)
- **Action**: `NEW`, `EXTEND`, or `SKIP`

### Step 5: Validate the catalog

Before finalizing, review the catalog against these checks:

1. **Naming validation** — Subject must be a human actor or `system`, never a code artifact.
2. **`manage` verb prohibition** — Reject any name containing `manage`/`manages`/`managing`.
3. **Value litmus test** — Would this behavior deliver value on its own?
4. **Cross-layer check** — Merge entries that cover the same behavior split by layer.
5. **Granularity check** — Each entry should have 2–5 plausible scenarios.
6. **File-count check** — If >15 related files, evaluate whether it conflates multiple behaviors.
7. **Subject balance check** — If all `system_*`, search for user-facing entry points. If all `user_*`, search for autonomous processing.
8. **Model lifecycle check** — Verify the catalog accounts for how records are created, not just read.
9. **Related-file completeness check** — Verify that each behavior entry lists files spanning the full stack, from frontend to backend. Apply these sub-checks:
   - **Controller / model marker density:** Controllers and models are behavioral hubs. The number of catalog entries referencing a given controller or model should approximate the number of distinct actions or responsibilities it implements. If a controller with 5 actions is only referenced by 1 catalog entry, the remaining actions are likely missing from the catalog.
   - **Full-stack traceability:** A typical user-facing behavior touches files across multiple layers (e.g., route → controller → service → model → serializer → view/frontend component). If a catalog entry only lists a model file with no controller, or only a controller with no frontend component, investigate whether related files are missing. Every behavior should be traceable from the user-facing entry point (frontend or API endpoint) down to the data layer (model).
   - **Shared-file awareness:** When a file (e.g., a model or a concern) appears in multiple catalog entries, this is expected and correct — it means the file participates in multiple behaviors. Confirm that each entry lists the file, not just one of them.

If the catalog passes all checks, proceed directly to Phase 3 without pausing for user approval.

Write the finalized catalog to `<specre_dir>/<domain>/_GENERATION_PLAN.md`.

## Phase 3: Delegated Card Generation

**Model strategy:** Phase 3 is structured execution following the catalog, so each card is delegated to a **Sonnet subagent** via the Task tool (`model: "sonnet"`, `subagent_type: "general-purpose"`).

Before starting, create a TodoWrite entry for each catalog item. If context compression occurs, re-read `<specre_dir>/<domain>/_GENERATION_PLAN.md` and the current TodoWrite state to recover your position.

### Dispatching subagents

Launch Sonnet subagents in **parallel batches of up to 3** for catalog entries whose source files do not overlap. Wait for all subagents in a batch to complete before launching the next batch.

For each catalog entry, construct a subagent prompt using the template below. Instead of passing structural map JSON (from the old map-generator scripts), pass the **indexed code text** retrieved from cocoindex for the behavior's source files.

**Retrieving code text for a subagent:**
```sql
SELECT filename, text
FROM codebaseindex__code_embeddings
WHERE filename IN ('<file1>', '<file2>', ...)
ORDER BY filename, location;
```

Pass the result as the `<source_code_text>` placeholder in the subagent prompt.

### Subagent prompt template

````
You are generating a specre specification card. Follow these instructions exactly.

**First**, read the specre-author skill at `.claude/skills/specre-author/SKILL.md` and follow all naming conventions, section structure, and writing guidelines defined there.

## Card details

- **Behavior name:** <behavior_name>
- **Action:** <NEW or EXTEND>
- **Existing ULID (EXTEND only):** <ULID_if_extending, or omit this line>
- **Source files:** <comma-separated list of source file paths>
- **Test files:** <comma-separated list of test file paths, or "none">
- **Template files:** <comma-separated list of template file paths, or "none">
- **specre_dir:** <specre_dir from specre.toml>
- **Domain:** <target domain>
- **Test convention pattern:** <glob pattern, e.g. "spec/models/*_spec.rb">
- **Today's date:** <YYYY-MM-DD>

## Source code text (from cocoindex)

The following is the indexed source code for the files in this behavior, retrieved from the cocoindex database. Use this as your primary reference for understanding the code structure and behavior. If any chunk boundaries split critical logic, read the original file with the Read tool.

<source_code_text>

## Instructions for NEW action

1. Review the source code text above to understand the behavior's structure, logic, and design intent.
2. Run `specre new` (MCP tool: mcp__specre__new) with target_dir=`<specre_dir>/<domain>` and name=`<behavior_name>`. Record the ULID from the created file's front-matter.
3. Fill in the card content:
   - **Related Files**: All source, test (`(Test)` suffix), and template (`(Template)` suffix) files.
   - **Functional Overview**: One-paragraph summary derived from source code.
   - **Scenarios**: 2–5 step-by-step descriptions in natural language. Do NOT copy-paste code.
   - **Design Intent**: Include only if reasoning is apparent from code.
   - **Key Members**: Include only if there are important state variables or parameters.
   - **Failures / Exceptions**: Include only if code has explicit error handling.
4. Run `specre tag` (MCP tool: mcp__specre__tag) with the ULID and file path for **every file in Related Files EXCEPT `.jbuilder` files**.
5. **Test discovery and status determination:**
   - Search for test files matching the test convention pattern.
   - If matching tests exist: read them, add to Related Files with `(Test)` suffix, tag them, and compare assertions against scenarios.
     - If aligned: set `status` to `stable` and `last_verified` to today's date.
     - If diverged: keep `status` as `draft`.
   - If no tests: keep `status` as `draft`. Do NOT create test files.
6. **Size check:** If card body exceeds ~120 lines, report the issue.
7. **Report your result:**
   ```
   RESULT:
   action: NEW
   card_path: <path to created .md file>
   ulid: <ULID>
   status: <draft or stable>
   auto_stabilized: <true or false>
   files_tagged: <number>
   issue: <none, or description of problem>
   ```

## Instructions for EXTEND action

1. Use `specre trace` (MCP tool: mcp__specre__trace) with the existing ULID to locate the card file.
2. Read the existing card and add source/test/template file paths to "Related Files".
3. Run `specre tag` for each newly added file EXCEPT `.jbuilder` files.
4. **Report your result:**
   ```
   RESULT:
   action: EXTEND
   card_path: <path to existing .md file>
   ulid: <existing ULID>
   files_tagged: <number>
   issue: <none, or description of problem>
   ```
````

### Collecting results

After each batch of subagents completes:

1. Parse the `RESULT:` block from each subagent's response.
2. Mark the corresponding TodoWrite entries as `completed`.
3. If any subagent reported an issue (oversized card, etc.), resolve and re-dispatch.
4. Launch the next batch.

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

## Appendix: SQL Cookbook

### A. Domain discovery with complex exclusions

```sql
-- Discover "comment" domain, excluding comments_admin, comment_scoring, etc.
SELECT DISTINCT filename
FROM codebaseindex__code_embeddings
WHERE filename ~* '(^|/)comments?[_/.]'
  AND filename NOT ILIKE '%comments_admin%'
  AND filename NOT ILIKE '%comment_scor%'
  AND filename NOT ILIKE '%comment_subscription%'
ORDER BY filename;
```

### B. Sub-domain breakdown for split decisions

```sql
-- Identify natural sub-domains within a large domain
SELECT
  CASE
    WHEN filename ~* 'liquid_tag' THEN 'liquid_tags'
    WHEN filename ~* 'tag_adjustment' THEN 'tag_adjustments'
    WHEN filename ~* 'tag_moderator' THEN 'tag_moderators'
    WHEN filename ~* 'tag_subforem' THEN 'tag_subforem'
    ELSE 'tag_core'
  END AS subdomain,
  COUNT(DISTINCT filename) AS file_count,
  COUNT(DISTINCT CASE WHEN filename LIKE 'spec/%' THEN filename END) AS spec_count,
  COUNT(DISTINCT CASE WHEN filename NOT LIKE 'spec/%' THEN filename END) AS src_count
FROM codebaseindex__code_embeddings
WHERE filename ~* 'tag'
GROUP BY subdomain
ORDER BY file_count DESC;
```

### C. Layer distribution analysis

```sql
SELECT
  CASE
    WHEN filename LIKE 'app/models/%' THEN 'Models'
    WHEN filename LIKE 'app/controllers/admin/%' THEN 'Admin Controllers'
    WHEN filename LIKE 'app/controllers/api/%' THEN 'API Controllers'
    WHEN filename LIKE 'app/controllers/concerns/%' THEN 'Controller Concerns'
    WHEN filename LIKE 'app/controllers/%' THEN 'Controllers'
    WHEN filename LIKE 'app/services/%' THEN 'Services'
    WHEN filename LIKE 'app/policies/%' THEN 'Policies'
    WHEN filename LIKE 'app/views/%' THEN 'Views'
    WHEN filename LIKE 'app/workers/%' THEN 'Workers'
    WHEN filename LIKE 'app/lib/%' THEN 'Lib'
    WHEN filename LIKE 'app/decorators/%' THEN 'Decorators'
    WHEN filename LIKE 'app/queries/%' THEN 'Queries'
    WHEN filename LIKE 'app/sanitizers/%' THEN 'Sanitizers'
    WHEN filename LIKE 'app/serializers/%' THEN 'Serializers'
    WHEN filename LIKE 'app/uploaders/%' THEN 'Uploaders'
    WHEN filename LIKE 'app/assets/%' OR filename LIKE 'app/javascript/%' THEN 'Frontend (JS/JSX)'
    WHEN filename LIKE 'spec/%' THEN 'Specs'
    ELSE 'Other'
  END AS layer,
  COUNT(DISTINCT filename) AS file_count
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
GROUP BY layer
ORDER BY file_count DESC;
```

### D. Existing @specre tag extraction

```sql
SELECT DISTINCT filename,
  (regexp_matches(text, '@specre\s+([A-Z0-9]{26})', 'g'))[1] AS ulid
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND text ~ '@specre\s+[A-Z0-9]{26}';
```

### E. Complexity ranking by chunk count

```sql
SELECT filename, COUNT(*) AS chunks,
  string_agg(DISTINCT language, ', ') AS lang
FROM codebaseindex__code_embeddings
WHERE <domain_filter>
  AND filename NOT LIKE 'spec/%'
GROUP BY filename
ORDER BY chunks DESC
LIMIT 20;
```

### F. Semantic similarity search

```sql
-- Find code semantically similar to a given file's first chunk
SELECT filename, LEFT(text, 100) AS preview,
  1 - (embedding <=> (
    SELECT embedding FROM codebaseindex__code_embeddings
    WHERE filename = '<reference_file>'
    ORDER BY location LIMIT 1
  )) AS similarity
FROM codebaseindex__code_embeddings
WHERE filename NOT LIKE 'spec/%'
  AND filename != '<reference_file>'
ORDER BY embedding <=> (
  SELECT embedding FROM codebaseindex__code_embeddings
  WHERE filename = '<reference_file>'
  ORDER BY location LIMIT 1
)
LIMIT 20;
```

### G. Full code text retrieval for subagent context

```sql
SELECT filename, text
FROM codebaseindex__code_embeddings
WHERE filename IN ('<file1>', '<file2>', '<file3>')
ORDER BY filename, location;
```

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
