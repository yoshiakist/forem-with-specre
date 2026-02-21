---
id: "01KHZ2Z99S4SW3W9QJMSMZTZR0"
name: "admin_can_manage_scheduled_automations"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/scheduled_automations_controller.rb`
- `app/helpers/scheduled_automations_helper.rb`
- `app/models/scheduled_automation.rb`
- `app/views/admin/scheduled_automations/index.html.erb` (Template)
- `app/views/admin/scheduled_automations/new.html.erb` (Template)
- `app/views/admin/scheduled_automations/edit.html.erb` (Template)
- `spec/requests/admin/scheduled_automations_controller_spec.rb` (Test)
- `spec/helpers/scheduled_automations_helper_spec.rb` (Test)
- `spec/factories/scheduled_automations.rb` (Test)

## Functional Overview

An admin can create, view, edit, delete, and toggle the enabled state of scheduled automations for a community bot through the admin panel. Each automation is configured with a frequency (hourly, daily, weekly, or custom interval), an AI service to call, an action to perform (create draft, publish article, or award badges), and optional additional instructions. The admin UI displays a list of all automations with their scheduling details, status, and action configuration, and presents human-readable frequency descriptions (e.g., "Every Friday at 09:00 AM UTC").

## Design Intent

Scheduled automations are scoped to community bots via `CommunityBotPolicy` authorization, ensuring only admins with the appropriate permissions can manage them. The controller is nested under the subforem and community bot routes to enforce this ownership hierarchy. Frequency configuration is normalized from form string values to integers on validation to ensure consistent scheduling calculations.

## Key Members

- `frequency` — one of `daily`, `weekly`, `hourly`, `custom_interval`
- `frequency_config` — JSON hash with scheduling parameters (e.g., `hour`, `minute`, `day_of_week`, `interval_days`)
- `action` — one of `create_draft`, `publish_article`, `award_first_org_post_badge`, `award_warm_welcome_badge`, `award_article_content_badge`
- `service_name` — identifies the AI service or badge automation to invoke
- `action_config` — JSON hash with action-specific parameters (e.g., `repo_name`, `badge_slug`, `tags`)
- `enabled` — boolean toggle controlling whether the automation executes on schedule

## Scenarios

### Admin lists all automations for a bot

1. Admin navigates to the scheduled automations index page for a community bot
2. System displays all automations ordered by creation date (newest first)
3. Each automation shows the service name, action, frequency in human-readable format, next run time, last run time, enabled/disabled status, running/failed state, and action configuration

### Admin creates a new automation

1. Admin navigates to the new automation form
2. Admin selects an AI service, action, and frequency, and configures frequency-specific parameters
3. Admin optionally fills in service-specific configuration and additional instructions
4. Admin submits the form
5. System validates the automation (frequency config must match the selected frequency's requirements)
6. System normalizes frequency config string values to integers, calculates the next run time, and saves the automation
7. Admin is redirected to the index page with a success message

### Admin creates an automation with invalid parameters

1. Admin submits the new automation form with missing or invalid frequency configuration
2. System validates the automation and finds errors (e.g., missing `hour` for daily frequency, minute out of 0–59 range)
3. System re-renders the new form with error messages displayed

### Admin updates an existing automation

1. Admin navigates to the edit form for an existing automation
2. Admin modifies the frequency, action, or other settings
3. Admin submits the form
4. System validates and saves the changes
5. If the frequency or frequency config changed, the system recalculates the next run time
6. Admin is redirected to the index page with a success message

### Admin deletes an automation

1. Admin clicks the delete button on an automation
2. Browser presents a confirmation dialog
3. On confirmation, system destroys the automation
4. Admin is redirected to the index page with a success message

### Admin toggles an automation's enabled state

1. Admin clicks the Enable/Disable button on an automation
2. System flips the `enabled` boolean
3. Admin is redirected to the index page with a message indicating the new state

## Failures / Exceptions

- Validation fails if `frequency_config` is missing required keys for the selected frequency (e.g., `minute` for hourly, `hour` and `minute` for daily, `day_of_week`, `hour` and `minute` for weekly)
- Validation fails if numeric values are out of range (minute 0–59, hour 0–23, day_of_week 0–6, interval_days >= 1)
- Validation fails if the associated user is neither a community bot nor an admin
- Authorization fails if the current admin lacks permission via `CommunityBotPolicy`
