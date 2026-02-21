---
id: "01KHZ30Q1RW1G4QRNXNKQTQ9NM"
name: "system_executes_due_automations_on_schedule"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/workers/scheduled_automations/process_worker.rb`
- `app/services/scheduled_automations/executor.rb`
- `app/models/scheduled_automation.rb`
- `spec/workers/scheduled_automations/process_worker_spec.rb` (Test)
- `spec/services/scheduled_automations/executor_spec.rb` (Test)

## Functional Overview

The system periodically processes scheduled automations that are due for execution. A Sidekiq worker (`ProcessWorker`) runs every 10 minutes via cron, finds all enabled and active automations whose `next_run_at` falls within the last 10 minutes, and delegates each to the `Executor` service. The executor manages concurrency guards (prevents re-entry if already running), dispatches to the appropriate handler based on the automation's action type (AI-powered article generation or badge awarding), manages state transitions (`active` → `running` → `active`/`failed`), and schedules the next run. For AI-powered actions, the executor calls the configured AI service, optionally augments the output with additional instructions, and creates an article as either a draft or a published post.

## Design Intent

The worker uses Sidekiq throttling with a concurrency limit of 1 to ensure only one processing cycle runs at a time. The 10-minute lookback window on `next_run_at` prevents missed automations due to timing drift. The executor's `running?` guard prevents concurrent execution of the same automation. State transitions are explicit (`mark_as_running!`, `mark_as_completed!`, `mark_as_failed!`) to maintain clear audit trail and enable recovery from failures.

## Key Members

- `ScheduledAutomation.due_for_execution` — scope returning enabled, active automations with `next_run_at <= Time.current`
- `state` — one of `active`, `running`, `completed`, `failed`; tracks execution lifecycle
- `next_run_at` — timestamp for next scheduled execution
- `last_run_at` — timestamp of most recent execution
- `Executor::Result` — struct with `success?`, `article`, and `error_message` fields

## Scenarios

### Worker finds and executes due automations

1. ProcessWorker runs on the cron schedule
2. System queries for enabled, active automations with `next_run_at` in the past 10 minutes
3. For each due automation, system calls `Executor.call`
4. Executor marks the automation as `running`
5. Executor dispatches to the appropriate handler based on the action type
6. On success, executor marks automation as `active` with updated `last_run_at` and recalculated `next_run_at`

### Executor generates an article via AI service

1. Executor receives an automation with action `create_draft` or `publish_article` and service `github_repo_recap`
2. System instantiates the `Ai::GithubRepoRecap` service with the configured repository name and lookback days
3. Service generates content (title and body)
4. If additional instructions are present, system appends them as an "Additional Context" section
5. System creates an `Article` with the generated content, configured tags, organization, and subforem
6. For `create_draft`, the article is saved as unpublished; for `publish_article`, it is published with `published_at` set

### Executor dispatches to badge awarding actions

1. Executor receives an automation with a badge-awarding action (`award_first_org_post_badge`, `award_warm_welcome_badge`, or `award_article_content_badge`)
2. System calls the corresponding badge awarder service directly, bypassing the AI service path
3. On success, executor marks the automation as completed and schedules the next run
4. On failure, executor returns the error message from the badge awarder

### Executor prevents concurrent execution

1. Executor receives an automation that is already in `running` state
2. Executor immediately returns a failure result with message "Automation is already running"
3. No state changes or service calls are made

### Executor handles failures gracefully

1. An error occurs during execution (e.g., API error, unknown service name, missing configuration)
2. Executor catches the error and marks the automation as `failed`
3. Error details are logged and returned in the result
4. No article is created

### Worker auto-creates warm welcome automation

1. ProcessWorker checks if a badge with slug `warm-welcome` exists
2. If the badge exists and no `award_warm_welcome_badge` automation exists yet, the worker creates one
3. The automation is configured as weekly on Fridays at 9 AM, enabled and active, assigned to a community bot user
4. If no community bot user exists, the worker logs a warning and skips creation

## Failures / Exceptions

- Returns failure if the automation is already in `running` state (concurrency guard)
- Returns failure for unknown `service_name` values (raises `ArgumentError`)
- Returns failure if `repo_name` is missing from `action_config` for the `github_repo_recap` service
- Marks automation as `failed` on any unhandled `StandardError` during execution
- Worker logs warnings when no community bot exists for warm welcome automation auto-creation
