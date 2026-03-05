---
id: "01KJVP4KGZFT0V02XDF80Y8517"
name: "system_quarantines_spam_email_domain"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/workers/spam/block_domain_and_suspend_users_worker.rb`
- `app/services/spam/domain_detector.rb`
- `app/models/blocked_email_domain.rb`
- `spec/models/user_spam_detection_spec.rb` (Test)
- `spec/services/spam/domain_detector_spec.rb` (Test)

## Functional Overview

When a user receives a spam or suspended role, the system checks whether their email domain exhibits a spam pattern: three or more recently registered users (within the last two weeks) from that domain already carry spam or suspended roles, and no user on that domain registered more than two weeks ago. Popular shared email providers (gmail.com, yahoo.com, etc.) are always excluded. If the pattern is confirmed, a background job (`Spam::BlockDomainAndSuspendUsersWorker`) is enqueued to add the domain to the `BlockedEmailDomain` blocklist and apply the `suspended` role to every not-yet-suspended or not-yet-spam user sharing that domain, recording an automatic-suspension note on each affected account.

## Design Intent

The two-step design — a synchronous `DomainDetector` that decides whether to act, plus an asynchronous worker that performs the writes — keeps role-assignment callbacks fast and avoids holding locks inside the request cycle. A Redis `NX` lock with a short TTL (300 s) prevents the worker from running concurrently for the same domain if multiple role events arrive in quick succession. Skipping popular shared domains prevents mass false positives on gmail.com or similar providers.

## Key Members

- `POPULAR_SHARED_DOMAINS` — hardcoded allowlist of shared email providers that are never treated as spam domains.
- `spam_pattern_detected?` — requires at least 3 recently registered users (within 2 weeks) with spam or suspended roles on the same domain, and no older legitimate accounts on that domain.
- `lock_key` — Redis key (`spam:block_domain_and_suspend:<domain>`) used to ensure only one worker execution per domain at a time, with a 300-second expiry.

## Scenarios

### Domain is a popular shared provider

1. User is assigned a spam or suspended role.
2. System extracts the email domain and checks it against the `POPULAR_SHARED_DOMAINS` allowlist.
3. Domain is found in the allowlist; detection exits immediately without enqueuing any job.

### Spam pattern detected — domain quarantined

1. User with a custom email domain is assigned a spam or suspended role.
2. System queries all users on that domain registered within the last two weeks.
3. At least three of those users already carry spam or suspended roles, and no user on the domain registered earlier than two weeks ago.
4. `Spam::BlockDomainAndSuspendUsersWorker` is enqueued with the lowercase-stripped domain as its argument.
5. Worker acquires a Redis lock for the domain, creates a `BlockedEmailDomain` record (idempotent), then iterates every user with a matching email address and applies the `suspended` role to any who are not already spam or suspended, attaching an automatic-suspension `Note` to each.

### Domain has a legitimate older user — no action taken

1. User with a custom email domain is assigned a spam or suspended role.
2. System finds that at least one user on that domain registered more than two weeks ago.
3. Domain is treated as having a legitimate user base; detection returns false and no job is enqueued.

### Fewer than three recent spam/suspended users — threshold not met

1. User with a custom email domain is assigned a spam or suspended role.
2. Fewer than three recently registered users on that domain carry spam or suspended roles.
3. Threshold is not met; detection returns false and no job is enqueued.

### Non-spam/suspended role assigned — detection not triggered

1. User is assigned any role other than spam or suspended (e.g., trusted).
2. `Spam::DomainDetector` is never invoked; no domain check or job enqueue occurs.

## Failures / Exceptions

- If the email domain is blank, the worker returns immediately without touching the database or Redis.
- If the Redis `NX` lock cannot be acquired (another execution is already in progress for the same domain), the worker exits without performing any writes.
- The Redis lock is released in an `ensure` block, guaranteeing cleanup even if an unexpected error is raised during bulk suspension.
