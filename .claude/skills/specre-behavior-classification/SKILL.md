---
name: specre-behavior-classification
description: "Guidelines for classifying source code into user-facing behaviors and producing a behavior catalog during specre card generation. Use this skill when executing Phase 2 (Behavior Classification) of the specre-generate-cocoindex workflow. Covers core classification principles, structural analysis from cocoindex, semantic cross-domain discovery, behavior grouping, catalog format, and the 9-point validation checklist."
---

# Behavior Classification for Specre Card Generation

This skill defines how to analyze source code and classify it into observable, user-facing behaviors suitable for specre cards. It is used during Phase 2 of the specre-generate-cocoindex workflow.

## Prerequisite

Before classifying behaviors, read the **specre-author** skill at `.claude/skills/specre-author/SKILL.md` to internalize naming conventions and writing guidelines. Every proposed card name MUST follow the subject + predicate sentence form defined there. Violations of naming conventions are the most common defect in generated cards.

## Core Principles

### Classify by observable behavior, not by code layer

A specre card describes a behavior as experienced by a human user, or as observable at a system boundary. A single behavior typically spans multiple code layers — model, controller, service, frontend component, worker, and view template all participate in the same behavior. Do NOT create separate cards per layer.

### Multiple markers per file are the norm

A single source file (especially controllers and models) typically participates in multiple behaviors and therefore receives multiple `@specre` markers — one per behavior it contributes to. For example, a `CommentsController` handling `create`, `update`, and `destroy` actions would carry three separate `@specre` markers, each linking to a different specre card. Do not assume one-file-one-marker; the number of markers on a file should correspond to the number of distinct behaviors it implements.

### Litmus test

"If a system implemented exactly this behavior and nothing else, would it deliver value to a user?" If not, the card describes an implementation fragment.

### `manage` verb prohibition

Never use `manage`/`manages`/`managing` in card names. Decompose into specific action verbs: `view`, `create`, `edit`, `delete`, etc.

## Step 1: Extract Structural Overview from CocoIndex

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

## Step 2: Use Semantic Search for Cross-Domain Discovery

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

## Step 3: Group Files into User-Facing Behaviors

After analyzing the structural data, shift perspective from individual files to **observable behaviors**:

1. "What can a human user do in this domain?" → `user_can_*`, `admin_can_*`, `author_can_*`
2. "What does the system do autonomously?" → `system_*`

Assign each file to the behavior it participates in. A model + controller + frontend + view that all contribute to one user action belong to **one** behavior.

## Step 4: Produce the Behavior Catalog

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

## Step 5: Validate the Catalog

Before finalizing, review the catalog against these 9 checks:

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
