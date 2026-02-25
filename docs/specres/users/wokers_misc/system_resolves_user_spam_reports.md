---
id: "01KJ9R606N0EG98CQ1X82ECHHN"
name: "system_resolves_user_spam_reports"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/workers/users/resolve_spam_reports_worker.rb`
- `spec/workers/users/resolve_spam_reports_worker_spec.rb` (Test)

## Functional Overview

This background worker processes spam report resolution for a given user. When enqueued with a user ID, it looks up the user and, if found, delegates to `Users::ResolveSpamReports` to perform the actual resolution logic. The worker runs on the medium-priority queue with up to 10 retries and uses an until-executing lock to prevent duplicate concurrent executions for the same job arguments.

## Design Intent

The until-executing lock prevents redundant enqueuing: if the same worker is already waiting to execute, additional enqueues are dropped. This is appropriate here because resolving spam reports is idempotent — running it multiple times for the same user is safe, but wasteful. The explicit user lookup with an early return guards against stale IDs that may have been enqueued before the user was deleted.

## Scenarios

### Worker resolves spam reports for a valid user

1. The worker is called with a valid user ID.
2. The system looks up the user by that ID.
3. The system delegates to `Users::ResolveSpamReports` with the found user to carry out resolution.

### Worker is called with a non-existent user ID

1. The worker is called with a user ID that does not correspond to any user (e.g., after a user has been deleted or an invalid ID is passed).
2. The system attempts to look up the user and finds none.
3. The worker exits early without raising an error and without calling the resolver.

## Failures / Exceptions

- If the user is not found by the given ID, the worker returns silently. No exception is raised and no retry is triggered by this condition.
