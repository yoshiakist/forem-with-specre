---
description: "Generate specre cards for uncovered source files in a domain"
---

You are executing the specre-generate workflow. The user has optionally provided a domain or subdirectory as `$ARGUMENTS`.

Your goal: create specre specification cards for source files that currently lack specre coverage.

**Model strategy:** The main agent (Opus) handles Phase 0–2 (discovery and behavior classification — creative work requiring judgment) and Phase 4 (validation). Phase 3 (card generation — structured execution) is delegated to Sonnet subagents in parallel batches. This reduces cost and latency while preserving quality where it matters most.

## Phase 0: Setup

1. Read `specre.toml` to determine `specre_dir` and `source_dirs`.
2. If `$ARGUMENTS` is empty, ask the user which domain or subdirectory to target.
3. Confirm the target domain with the user before proceeding.

## Phase 1: Discovery

1. Run `specre coverage` (MCP tool) to identify uncovered source files.
   > **Fallback for large codebases:** If the MCP tool result exceeds the token limit (the output is saved to a temporary file instead of being returned inline), use the helper script instead:
   > ```bash
   > python3 .claude/commands/scripts/coverage-uncovered.py <domain_keyword>
   > ```
   > This runs `specre coverage --json` via CLI and filters uncovered files by a case-insensitive keyword match on file paths, avoiding MCP output size limits. The script outputs coverage stats (`coverage=`, `tagged=`, `total=`, `uncovered_count=`) followed by a `---` separator and the filtered file list.
2. Filter the **Uncovered files** list to only those belonging to the target domain.
   - "Domain" means the top-level functional directory within each `source_dirs` entry (e.g., `src/auth/`, `src/cart/`).
   - Exclude test files from the generation targets. Test files are used as evidence for status determination (Phase 3), not as specre subjects.
3. Identify the project's test file convention by examining the directory structure (e.g., `tests/<domain>/cli_*.rs`, `src/**/*.test.ts`, `spec/**/*_spec.rb`). Record this pattern for reuse in Phase 3b so that test discovery does not need to be re-explored for each card.
4. Log the filtered file list for your own reference and proceed directly to Phase 2. Do NOT pause for user approval here.

## Phase 2: Behavior Classification

**Purpose:** Build a complete picture of the domain's behaviors BEFORE creating any cards. This prevents duplicate cards, identifies cross-file behaviors, and establishes a logical generation order.

> **Prerequisite — load the specre-author skill.** Before classifying behaviors, read the specre-author skill (`SKILL.md`) to internalize naming conventions and writing guidelines. Every proposed card name MUST follow the subject + predicate sentence form defined there. Violations of naming conventions are the most common defect in generated cards.

> **Core principle — classify by observable behavior, not by code layer.** A specre card describes a behavior as experienced by a human user, or as observable at a system boundary. The subject is either a human actor (`user`, `admin`, `author`) or `system` when no human is in the loop (batch jobs, scheduled tasks, pub/sub handlers, webhook receivers). A single behavior typically spans multiple code layers — model, controller, service, frontend component, worker, and view template all participate in the same behavior. Do NOT create separate cards per layer (e.g., one for the model, one for the controller, one for the frontend). Instead, identify the observable behavior first, then gather all files across layers that implement it.
>
> **Litmus test — does this behavior deliver value on its own?** For each proposed card, ask: "If a system implemented exactly this behavior and nothing else, would it deliver value to a user?" If the answer is no, the card likely describes an implementation fragment, not a complete behavior. For example, "github_repo_stores_repository_metadata" alone delivers no value to anyone — a user needs to be able to *feature* repos on their profile, see them, and manage them. That end-to-end experience is the correct card scope.
>
> **Anti-pattern — layer-oriented cards (each fails the litmus test individually):**
> - `github_repo_stores_repository_metadata` (storing metadata alone delivers no user value)
> - `github_repos_controller_manages_user_repos` (an API endpoint alone is not a complete experience)
> - `github_repos_frontend_displays_repos` (a UI without a backend serves nothing)
>
> **Correct — behavior-oriented cards (each passes the litmus test):**
> - `user_can_feature_github_repos_on_profile` (spans model + controller + frontend + worker)
> - `author_can_embed_github_issue_in_article` (spans liquid tag + model + view)
> - `system_syncs_github_repos_periodically` (spans worker + model — no human in the loop, triggered by scheduler)
> - `system_notifies_user_on_new_comment` (spans pub/sub listener + mailer + template — system-initiated delivery)

> **Token-efficient analysis:** Do NOT read source files directly with the Read tool. Instead, use the map generator scripts (`.claude/commands/scripts/ruby-map-generator.py` and `.claude/commands/scripts/js-map-generator.py`) to extract structural metadata in a single batch per language. This dramatically reduces token consumption while providing sufficient context for behavior classification. The structural JSON is also passed to Phase 3 subagents so they can generate cards without reading source files.

### Step 1: Generate structural maps and build a file-role map

**Do NOT read source files with the Read tool.** Use the map generator scripts to extract structural metadata in a single batch per language. This provides all the context needed for behavior classification at a fraction of the token cost.

1. **Partition** the uncovered files by language:
   - `.rb` files → `ruby-map-generator.py`
   - `.js` / `.jsx` files → `js-map-generator.py`
   - Other files (`.erb`, `.jbuilder`, etc.) → identified by extension only (not parsed)
2. **Run the generators** via Bash, passing all files for each language at once:
   ```bash
   python3 .claude/commands/scripts/ruby-map-generator.py file1.rb file2.rb ...
   python3 .claude/commands/scripts/js-map-generator.py file1.js file2.jsx ...
   ```
   Each script outputs a compact JSON map keyed by relative file path containing:
   - **Ruby**: classes/modules, methods (params, returns, responses), callbacks, includes, associations, validations, scopes, delegates, attrs, class_refs (dependencies)
   - **JS/JSX**: imports, exports, functions (params, hooks, jsx_components), classes (methods, PropTypes, Stimulus metadata), constants
3. **Store the full JSON output** — this will be reused in Phase 3 when constructing subagent prompts. Each subagent receives only the subset of structural data relevant to its behavior's source files.
4. **Infer file roles** from the structural data — do not read the source:
   - **Controller**: has `callbacks` (before_action etc.) and methods with `responses` (render/redirect_to)
   - **Model**: has `associations`, `validations`, `scopes`
   - **Service/Worker**: class with focused method signatures, class_refs to models
   - **Frontend component**: has `hooks`, `jsx_components`, or `propTypes`
   - **View template** (`.erb`, `.jbuilder`): identified by file extension (not parsed by scripts — include by path convention)
5. **Identify tightly coupled files** from the structural data:
   - `class_refs` (Ruby) and `imports` (JS) reveal which files collaborate
   - `associations` and `includes` show model relationships
   - Method params and return patterns indicate data flow
6. **Search for existing specre cards** that may already cover this behavior:
   ```
   specre search "<subject> <action_verb>"
   ```
   Use AND-keyword queries combining the behavior's subject (noun) and action (verb).

### Step 2: Group files into user-facing behaviors

After analyzing all structural maps, shift perspective from individual files to **observable behaviors**. Ask two questions:

1. "What can a human user do in this domain?" — These become `user_can_*`, `admin_can_*`, etc.
2. "What does the system do autonomously (batch jobs, scheduled tasks, pub/sub, webhooks)?" — These become `system_*` cards.

Then assign each file to the behavior it participates in:

- A model, a controller, a frontend component, and a view template that all contribute to "user can feature GitHub repos on their profile" belong to **one** behavior, not four.
- A worker triggered by a scheduler, a pub/sub handler, or a webhook receiver is a system-initiated behavior (e.g., "system syncs GitHub repos periodically", "system notifies user on new comment").
- Infrastructure-only code with no direct observable effect (e.g., an API client wrapper, an error hierarchy) should be folded into the behavior(s) that depend on it, not given its own card.

### Step 3: Produce the behavior catalog

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
- **Proposed name**: subject + predicate sentence form (see specre-author skill for naming rules)
- **Source files**: which files this card will cover (expect files from multiple layers — model, controller, frontend, view, etc.)
- **Test files** (if any): corresponding test/spec files discovered in Phase 2
- **Template files** (if any): associated view/template files (`.erb`) discovered in Phase 2
- **Action**: `NEW` (create a new card) or `EXTEND` (tag source file to an existing card and update its Related Files)

**Classify by subject first, then by behavior.** Group related behaviors by their actor/subject (e.g., all `user_can_*` behaviors together, all `system_rejects_*` together). This produces a natural reading order and makes it easy to spot missing behaviors.

### Step 4: Validate the catalog

Before finalizing, review the catalog against these checks:

1. **Naming validation** — Every proposed name must have a human actor (`user`, `admin`, `author`) or `system` as the subject, never a code artifact. Reject names where the subject is a class name, layer name, or technical component (e.g., `*_controller_*`, `*_model_*`, `*_frontend_*`, `*_worker_*`, `*_service_*`). Refer to the specre-author skill's naming conventions for the definitive rules.
2. **Value litmus test** — For each entry, ask: "If a system implemented exactly this behavior and nothing else, would it deliver value to a user?" If not, the entry is an implementation fragment. Merge it into a broader behavior or reconsider the card boundary.
3. **Cross-layer check** — If multiple catalog entries cover the same observable behavior split by layer (e.g., a controller entry and a separate frontend entry for the same feature), merge them into a single entry.
4. **Granularity check** — Each entry should have 2–5 plausible scenarios. If you can only think of one scenario, the behavior is likely a fragment of a larger one; merge it. If you can think of more than 7, it may conflate multiple behaviors; consider splitting.

If the catalog passes all checks, proceed directly to Phase 3 without pausing for user approval.

Write the finalized catalog to `<specre_dir>/<domain>/_GENERATION_PLAN.md`. This file serves as a persistent reference during Phase 3 — if context compression causes the catalog to be summarized or lost, re-read this file to recover the full plan. This file is deleted in Phase 4 after all entries are processed.

## Phase 3: Delegated Card Generation

**Model strategy:** Phase 2 (behavior classification) is where creative judgment matters most — that work stays on the main agent (Opus). Phase 3 is structured execution following the catalog, so each card is delegated to a **Sonnet subagent** via the Task tool (`model: "sonnet"`, `subagent_type: "general-purpose"`). This reduces cost and latency without sacrificing quality.

Before starting, create a TodoWrite entry for each catalog item. If context compression occurs, re-read `<specre_dir>/<domain>/_GENERATION_PLAN.md` and the current TodoWrite state to recover your position.

### Dispatching subagents

Launch Sonnet subagents in **parallel batches of up to 3** for catalog entries whose source files do not overlap. Wait for all subagents in a batch to complete before launching the next batch. Update TodoWrite entries to `completed` as each subagent finishes.

For each catalog entry, construct a subagent prompt using the template below. Fill in all `<placeholders>` with concrete values from the catalog and Phase 1/2 context.

**Passing structural data:** For the `<structural_map_json>` placeholder, extract the subset of the Phase 2 JSON output that corresponds to the behavior's source files. Only include entries for the files listed in that catalog entry — do not pass the entire domain map. This keeps each subagent's prompt focused and compact.

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
- **Test convention pattern:** <glob pattern identified in Phase 1, e.g. "spec/models/*_spec.rb">
- **Today's date:** <YYYY-MM-DD>

## Structural map data

The following JSON contains structural metadata extracted by the map generator scripts (ruby-map-generator.py / js-map-generator.py). Use this as a **structural overview** before reading source files — it shows class/module structures, method signatures, params, return values, callbacks, associations, validations, dependencies (class_refs / imports), hooks, JSX components, and other metadata. Consult this first to understand the shape of the code, then read the source files for behavioral intent and detail.

```json
<structural_map_json>
```

## Instructions for NEW action

1. Review the structural map data above to understand the overall shape of the behavior — classes, methods, dependencies, and patterns. Then read the source files listed above to understand behavioral intent, branching logic, and design decisions that the structural data alone cannot capture.
2. Run `specre new` (MCP tool: mcp__specre__new) with target_dir=`<specre_dir>/<domain>` and name=`<behavior_name>`. Record the ULID from the created file's front-matter.
3. Fill in the card content:
   - **Related Files**: All source, test (`(Test)` suffix), and template (`(Template)` suffix) files. Use project-root-relative paths.
   - **Functional Overview**: One-paragraph summary derived from source code.
   - **Scenarios**: 2–5 step-by-step descriptions in natural language. Do NOT copy-paste code. Exception: use exact names for signals/events, class/type names, enum values, and API endpoints.
   - **Design Intent**: Include only if reasoning is apparent from code. Omit if unclear.
   - **Key Members**: Include only if there are important state variables or parameters.
   - **Failures / Exceptions**: Include only if code has explicit error handling.
4. Run `specre tag` (MCP tool: mcp__specre__tag) with the ULID and file path for **every file in Related Files EXCEPT `.jbuilder` files**. `.jbuilder` files must appear in Related Files for documentation but cannot be tagged.
5. **Test discovery and status determination:**
   - Search for test files matching the test convention pattern for the source files in this entry.
   - If matching tests exist: read them, add to Related Files with `(Test)` suffix, tag them, and compare assertions against the card's scenarios.
     - If they align: set `status` to `stable` and `last_verified` to today's date.
     - If they diverge: keep `status` as `draft`.
   - If no tests exist: keep `status` as `draft`. Do NOT create test files.
6. **Size check:** If the card body (excluding front-matter) exceeds ~120 lines, it likely covers more than one behavior. Report this issue in your result.
7. **Report your result** at the end of your response in this exact format:
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
2. Read the existing card (this is the specre card, not a source file) and add source/test/template file paths to the "Related Files" section.
3. Run `specre tag` (MCP tool: mcp__specre__tag) for each newly added file EXCEPT `.jbuilder` files.
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
3. If any subagent reported an issue:
   - **Oversized card (>120 lines):** Split the behavior into separate catalog entries and dispatch new subagents.
   - **Other issues:** Resolve directly or re-dispatch the subagent with corrected parameters.
4. Launch the next batch.

## Phase 4: Validation and Review

After all catalog entries are processed:

1. Delete `<specre_dir>/<domain>/_GENERATION_PLAN.md` (the generation plan is no longer needed).
2. Run `specre index` to regenerate the index.
3. Run `specre orphans` to verify there are no unlinked cards or dangling markers.
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

- **Autonomous within phases.** Do not pause for user input between individual card generations in Phase 3. The user approval point is the behavior catalog in Phase 2.
- **Delegate Phase 3 to Sonnet.** Always use `model: "sonnet"` and `subagent_type: "general-purpose"` for Phase 3 subagents. The main agent (Opus) handles Phase 0–2 (design) and Phase 4 (validation). Phase 3 (execution) is delegated to Sonnet subagents in parallel batches.
- **Follow the specre-author skill.** Load and follow the specre-author skill for all naming conventions, section structure, and writing guidelines. This is the authoritative source for card format — do not deviate from it.
- **Name by observable behavior, not by code artifact.** The subject of every card name must be a human actor (`user`, `admin`, `author`) or `system` (for batch jobs, scheduled tasks, pub/sub, webhooks), never a class name, layer name, or technical component. See the specre-author skill's Naming Conventions section.
- **One behavior = one card across all layers.** A user-facing behavior that spans model, controller, frontend, worker, and view is **one** specre card with multiple Related Files — not separate cards per layer. Infrastructure-only code (API clients, error hierarchies, base classes) should be folded into the behavior card(s) that consume it.
- **Write in natural language.** Scenarios must be written in natural language, not in code. See the specre-author skill for the code-independence principle and its exceptions.
- **Never create test files.** This workflow generates specre cards only.
- **Never modify source files** beyond inserting `@specre` markers via `specre tag`.
- **`.jbuilder` files are not taggable.** Include them in Related Files for documentation, but skip them when running `specre tag`.
