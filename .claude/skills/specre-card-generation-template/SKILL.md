---
name: specre-card-generation-template
description: "Subagent prompt template and result collection procedure for Phase 3 (Delegated Card Generation) of the specre-generate-cocoindex workflow. Use this skill when dispatching Sonnet subagents to generate or extend specre cards. Contains the full prompt template for NEW and EXTEND actions, code retrieval queries, and the batch result collection protocol."
---

# Card Generation Subagent Template

This skill provides the subagent prompt template and result collection procedure used during Phase 3 of the specre-generate-cocoindex workflow.

## Retrieving Code Text for a Subagent

Before dispatching a subagent, retrieve the indexed code text for the behavior's source files:

```sql
SELECT filename, text
FROM codebaseindex__code_embeddings
WHERE filename IN ('<file1>', '<file2>', ...)
ORDER BY filename, location;
```

Pass the result as the `<source_code_text>` placeholder in the subagent prompt below.

## Subagent Prompt Template

Use this template verbatim when constructing the `prompt` parameter for each Task tool call. Replace all `<placeholder>` values with actual data from the behavior catalog.

````
You are generating a specre specification card. Follow these instructions exactly.

**First**, read the specre-author skill at `.claude/skills/specre-author/SKILL.md` and follow all naming conventions, section structure, and writing guidelines defined there.

## Critical tagging rules — read before doing anything else

> 1. **Every file in "Related Files" MUST be tagged.** Do not skip any file. Every source file, every test file, every template file that participates in this behavior must receive a `@specre` marker linking to this card's ULID — the only exception is `.jbuilder` files.
> 2. **A file may already have `@specre` markers from other behaviors. That is correct and expected.** Adding another `@specre` marker to an already-tagged file does NOT overwrite existing markers. Controllers, models, and concerns routinely carry multiple markers — one per behavior they implement. Do NOT skip tagging a file just because it already has a `@specre` line.

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
4. Run `specre tag` (MCP tool: mcp__specre__tag) with the ULID and file path for **every file in Related Files EXCEPT `.jbuilder` files**. This means you must call `mcp__specre__tag` once per file — controllers, models, services, workers, views, AND test files all get tagged. If a file already has `@specre` markers from other behaviors, adding this card's marker is correct and expected; do not skip it.
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

## Dispatching Subagents

Launch Sonnet subagents in **parallel batches of up to 3** for catalog entries whose source files do not overlap. Wait for all subagents in a batch to complete before launching the next batch.

Each subagent is dispatched via the Task tool with:
- `model: "sonnet"`
- `subagent_type: "general-purpose"`

## Collecting Results

After each batch of subagents completes:

1. Parse the `RESULT:` block from each subagent's response.
2. Mark the corresponding TodoWrite entries as `completed`.
3. If any subagent reported an issue (oversized card, etc.), resolve and re-dispatch.
4. Launch the next batch.
