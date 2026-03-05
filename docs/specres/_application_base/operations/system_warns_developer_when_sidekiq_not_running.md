---
id: "01KJXS5KFKXR5ATWMC60V4695E"
name: "system_warns_developer_when_sidekiq_not_running"
status: "draft"
---

## Related Files

- `app/controllers/concerns/development_dependency_checks.rb`

## Functional Overview

`DevelopmentDependencyChecks` is a Rails concern included exclusively in the development environment. It registers a `before_action` that runs before `index` and `show` actions to confirm that at least one Sidekiq process is registered. The check attempts up to three times with a brief pause between retries to tolerate timing windows where Sidekiq has not yet fully registered. If no running process is detected after all retries, a flash notice is set to inform the developer that Sidekiq is not running and instructs them to use `bin/startup-local` to start the application correctly.

## Design Intent

The retry loop with short sleeps exists to handle race conditions that can occur during development server startup, when Sidekiq may not have registered itself with Redis at the exact moment the first request arrives. Limiting the check to `index` and `show` only, and to the development environment only, keeps the overhead out of production and mutation actions.

## Scenarios

### Sidekiq is running when the request arrives

1. A developer sends a GET request that routes to an `index` or `show` action.
2. The concern's before-action runs and queries the Sidekiq process set.
3. At least one process is found on the first, second, or third attempt.
4. The before-action returns without setting any flash message and the controller action proceeds normally.

### Sidekiq is not running after all retries

1. A developer sends a GET request that routes to an `index` or `show` action.
2. The concern's before-action runs and queries the Sidekiq process set up to three times, pausing briefly between each attempt.
3. No running Sidekiq process is detected on any attempt.
4. A global flash notice is set instructing the developer to start Sidekiq via `bin/startup-local`.
5. The controller action still executes but the page is rendered with the warning visible.

### Sidekiq becomes available on a retry

1. A developer starts the application and immediately opens a page.
2. The first or second Sidekiq check returns zero processes.
3. After the short delay, a subsequent attempt detects a running process.
4. No flash message is set and the request proceeds normally.

## Failures / Exceptions

- If any attempt to query the Sidekiq process set raises a `StandardError` (for example, because Redis is unavailable), the error is logged at debug level and the loop continues to the next retry; after all retries are exhausted without a successful positive result, the flash warning is shown as if Sidekiq were not running.
