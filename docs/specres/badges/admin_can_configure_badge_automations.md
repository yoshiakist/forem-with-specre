---
id: "01KJ6FF3R4FQCEVGKVPFYYPY8Y"
name: "admin_can_configure_badge_automations"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/badge_automations_controller.rb`
- `app/views/admin/badge_automations/index.html.erb` (Template)
- `app/views/admin/badge_automations/new.html.erb` (Template)
- `app/views/admin/badge_automations/edit.html.erb` (Template)
- `spec/requests/admin/badge_automations_controller_spec.rb` (Test)

## Functional Overview

Admins can create, edit, enable/disable, and delete scheduled automations that automatically award a specific badge to users meeting defined criteria. Two automation types are supported: "first org post" (awards the badge to a user who publishes their first article under a selected organization) and "article content quality" (awards the badge to authors whose articles satisfy AI-assessed quality criteria including optional keywords and a lookback window). Each automation is scoped to a single badge, runs on a configurable schedule (hourly, daily, weekly, or custom interval), and records the creating admin as its owner. The controller enforces that only super-admins may access these routes.

## Design Intent

Automations are stored as `ScheduledAutomation` records rather than a badge-specific model so that the scheduling and execution infrastructure can be shared across different automation use cases. The `action` and `service_name` fields on the record are set server-side based on the chosen `automation_type` parameter to prevent clients from injecting arbitrary action names. Scoping the index query to the badge's slug ensures an admin managing one badge cannot accidentally view or modify automations belonging to another badge.

## Key Members

- `action_config["badge_slug"]` — always forced to the parent badge's slug on create and update, ensuring cross-badge isolation
- `action_config["organization_id"]` — required for `award_first_org_post_badge`; set from a top-level `organization_id` param rather than nested inside the permitted `scheduled_automation` params
- `action_config["criteria"]` — required free-text quality description for `award_article_content_badge`
- `action_config["keywords"]` — optional comma-separated string converted to an array on save; used to filter candidate articles
- `frequency` / `frequency_config` — control when the automation runs; changing either triggers recalculation of `next_run_at`

## Scenarios

### Admin lists automations for a badge

1. Admin navigates to the badge automations index for a specific badge.
2. The system queries only `ScheduledAutomation` records whose `action_config` badge slug matches the badge and whose action is one of the two supported badge-award actions.
3. The page displays each automation with its type, creator, schedule, next run time, and enable/disable state.
4. Automations belonging to other badges are not shown.

### Admin creates a "first org post" automation

1. Admin opens the new automation form for a badge and selects automation type "First Post Under Organization".
2. Admin selects an organization from the dropdown, sets a frequency and time, and submits the form.
3. The system sets the action to `award_first_org_post_badge`, stores the badge slug and organization ID in `action_config`, assigns the current admin as the owner, calculates the first `next_run_at`, and saves the record.
4. Admin is redirected to the badge's automation index with a success message.

### Admin creates an "article content quality" automation

1. Admin opens the new automation form for a badge and selects automation type "Article Content Quality".
2. Admin provides quality criteria text, optional keywords, an optional lookback window in hours, a frequency, and submits.
3. The system sets the action to `award_article_content_badge`, stores the criteria (and keywords as an array) in `action_config`, calculates `next_run_at`, and saves.
4. Admin is redirected to the badge's automation index with a success message.

### Admin edits an existing automation

1. Admin opens the edit form for an automation linked to a badge.
2. Admin updates the frequency, organization, criteria, or other fields and submits.
3. The system updates the record, re-stamps `action_config["badge_slug"]` to ensure it stays correct, and recalculates `next_run_at` if the frequency or frequency config changed.
4. Admin is redirected to the badge's automation index with a success message.

### Admin toggles or deletes an automation

1. Admin clicks "Enable" or "Disable" on an automation in the index; the system flips the `enabled` flag and redirects back with a confirmation message.
2. Admin clicks "Delete" and confirms the prompt; the system destroys the record and redirects to the index.

## Failures / Exceptions

- Creating a "first org post" automation without selecting an organization adds an error and re-renders the new form without saving.
- Creating an "article content quality" automation without providing quality criteria adds an error and re-renders the new form.
- Submitting invalid schedule parameters (e.g., blank frequency) causes model validation to fail and re-renders the appropriate form with error messages.
- Attempting to access an automation whose `action_config["badge_slug"]` does not match the URL badge raises `ActiveRecord::RecordNotFound`.
- Non-admin users attempting to access any action receive a `Pundit::NotAuthorizedError`.
