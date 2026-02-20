---
description: "Generate specre cards for uncovered source files in a domain"
---

You are executing the specre-generate workflow. The user has optionally provided a domain or subdirectory as `$ARGUMENTS`.

Your goal: create specre specification cards for source files that currently lack specre coverage, working through them **one card at a time** in a structured sequence.

**Critical constraint — sequential generation:** Do NOT attempt to draft or hold multiple card contents in your context simultaneously. Each card must be fully created, written to disk, and tagged before you begin analyzing the next behavior. This prevents context-window saturation from degrading the quality of later cards.

## Phase 0: Setup

1. Read `specre.toml` to determine `specre_dir` and `source_dirs`.
2. If `$ARGUMENTS` is empty, ask the user which domain or subdirectory to target.
3. Confirm the target domain with the user before proceeding.

## Phase 1: Discovery

1. Run `specre coverage` to identify uncovered source files.
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

> **Large domain shortcut:** If the domain contains more than 15 uncovered files, use the Task tool with `subagent_type=Explore` to read and classify files in batches. This protects the main context window from saturation while still building a complete catalog.

### Step 1: Read all uncovered files and build a file-role map

For each uncovered file in the list:

1. **Read the source file** and note its role — model, controller, service, worker, frontend component, view template, etc.
2. **Identify tightly coupled files** that participate in the same user-facing behavior:
   - Base classes or traits that the file extends/implements
   - Types that the file instantiates or depends on directly
   - Files where the file's public interface is consumed extensively
   - Template/view files that render the behavior's output (e.g., `.erb`)
   - Test/spec files that verify the behavior (e.g., `spec/**/*_spec.rb`, `test/**/*_test.rb`)
3. **Search for existing specre cards** that may already cover this behavior:
   ```
   specre search "<subject> <action_verb>"
   ```
   Use AND-keyword queries combining the behavior's subject (noun) and action (verb). For example: `specre search "order approve"`, `specre search "token validate"`.

### Step 2: Group files into user-facing behaviors

After reading all files, shift perspective from individual files to **observable behaviors**. Ask two questions:

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

## Phase 3: Sequential Card Generation

Before starting, create a TodoWrite entry for each catalog item (use the catalog entry name as the task content). Mark each entry as `in_progress` when you begin processing it, and `completed` when the card is fully written, tagged, and status-determined. If context compression occurs, re-read `<specre_dir>/<domain>/_GENERATION_PLAN.md` and the current TodoWrite state to recover your position.

Process the approved catalog entries **one at a time, in order**. For each entry:

### Step 3a: Create or Extend

**If action is `NEW`:**

1. Run `specre new <specre_dir>/<domain> --name "<behavior_name>"` to scaffold the card.
2. Fill in the card content following these authoring rules:
   - **Related Files**: The source files listed in the catalog entry, plus any tightly coupled files identified in Phase 2 — including test/spec files and template/view files. Use project-root-relative paths. Suffix test files with `(Test)`. Suffix template/view files with `(Template)`.
   - **Functional Overview**: A one-paragraph summary of the behavior, derived from the source code.
   - **Scenarios**: Step-by-step behavior descriptions in **natural language**. Do NOT copy-paste code into scenarios. Exception: use exact names for signals/events, class/type names, enum values, and API endpoints. Aim for 2–5 scenarios per card — fewer suggests the card is a fragment of a larger behavior, more suggests it conflates multiple behaviors.
   - **Design Intent**: Include if the reasoning is apparent from the code. Omit if unclear — do not fabricate rationale.
   - **Key Members**: Include if there are important state variables or parameters. Omit otherwise.
   - **Failures / Exceptions**: Include if the code has explicit error handling paths. Omit otherwise.
3. Run `specre tag <ULID> <file>` for **every file listed in Related Files** — source files, test/spec files, and template files alike — **except `.jbuilder` files**. The `specre tag` command does not support the `.jbuilder` extension. `.jbuilder` files should still be included in the Related Files section for documentation purposes, but must be skipped during tagging.

**If action is `EXTEND`:**

1. Add the source file path (and any associated test/template files) to the existing specre card's "Related Files" section.
2. Run `specre tag <existing_ULID> <file>` for each file added to Related Files — source, test, and template files alike — **except `.jbuilder` files** (same rule as above).
3. Mark this TodoWrite entry as `completed` and move to the next catalog entry. **Skip Steps 3b and 3c for EXTEND actions.**

### Step 3b: Test Discovery and Status Determination (NEW actions only)

1. Search for test files corresponding to the source files in this entry, using the test convention identified in Phase 1 step 3. Apply the recorded glob pattern within the target domain's test directory.
2. **If matching tests exist:**
   - Add the test file paths to the card's "Related Files" section with a `(Test)` suffix.
   - Run `specre tag <ULID> <test_file>` for each discovered test file (if not already tagged in Step 3a).
   - Compare the test assertions against the card's scenarios.
     - **If they align**: Set `status` to `stable` and `last_verified` to today's date. Mark this card internally as **auto-stabilized** for the review prompt in Phase 4.
     - **If they diverge**: Keep `status` as `draft`.
3. **If no matching tests exist:**
   - Keep `status` as `draft`.
   - Do NOT create test files. This workflow only generates specre cards.

### Step 3c: Size Check

After writing the card, check its length. If the card body (excluding front-matter) exceeds roughly 120 lines, it likely covers more than one behavior. Split it into separate cards and re-run Steps 3a–3b for each.

**Confirm completion of this entry before moving to the next one.**

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
- **Follow the specre-author skill.** Load and follow the specre-author skill for all naming conventions, section structure, and writing guidelines. This is the authoritative source for card format — do not deviate from it.
- **Name by observable behavior, not by code artifact.** The subject of every card name must be a human actor (`user`, `admin`, `author`) or `system` (for batch jobs, scheduled tasks, pub/sub, webhooks), never a class name, layer name, or technical component. See the specre-author skill's Naming Conventions section.
- **One behavior = one card across all layers.** A user-facing behavior that spans model, controller, frontend, worker, and view is **one** specre card with multiple Related Files — not separate cards per layer. Infrastructure-only code (API clients, error hierarchies, base classes) should be folded into the behavior card(s) that consume it.
- **Write in natural language.** Scenarios must be written in natural language, not in code. See the specre-author skill for the code-independence principle and its exceptions.
- **Never create test files.** This workflow generates specre cards only.
- **Never modify source files** beyond inserting `@specre` markers via `specre tag`.
- **`.jbuilder` files are not taggable.** Include them in Related Files for documentation, but skip them when running `specre tag`.
