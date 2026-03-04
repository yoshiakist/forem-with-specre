---
id: "01KJVGE8NSPTAPX0HVKBT09C6D"
name: "system_enforces_rate_limits_on_user_actions"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/rate_limit_checker.rb`
- `app/helpers/rate_limit_checker_helper.rb`
- `spec/services/rate_limit_checker_spec.rb` (Test)
- `spec/helpers/rate_limit_checker_helper_spec.rb` (Test)

## Functional Overview

`RateLimitChecker` enforces per-user, per-action rate limits across a defined set of user actions (article creation, comments, reactions, follows, image uploads, etc.). Each action has a configured `retry_after` window in seconds. On each action attempt, the service checks a Rails cache counter or a database query against a configurable threshold from `Settings::RateLimit`; if the threshold is exceeded, it raises `LimitReached` with the `retry_after` value so callers can surface a user-facing message. The service also supports tracking increments into the cache, checking email recipient flood limits, and bypassing all limits in end-to-end test environments. `RateLimitCheckerHelper` complements the service by providing structured metadata (title, description, min, placeholder, enabled) for every configurable limit, used in the admin UI.

## Design Intent

Rate limit thresholds are stored in `Settings::RateLimit` (a site-settings table), making them adjustable by admins without a code deploy. Cache-backed counters (with expiry matching `retry_after`) handle the hot path for most actions, while database queries are used for actions where in-DB records are the authoritative source of truth (comment creation, published article creation, follow counts). The E2E bypass prevents test suites from being blocked by limits during automated runs.

## Key Members

- `ACTION_LIMITERS` — frozen hash mapping each action symbol to its `retry_after` value in seconds; defines the universe of rate-limited actions
- `LimitReached` — `StandardError` subclass carrying `retry_after`; raised by `check_limit!` when a limit is exceeded
- `Settings::RateLimit.<action>` — admin-configurable integer threshold for each action
- `configurable_rate_limits` (helper) — returns a hash keyed by action with `:title`, `:description`, `:min`, `:placeholder`, and `:enabled` for admin UI rendering

## Scenarios

### Checking whether a limit has been reached (cache-backed action)

1. A controller or service calls `limit_by_action(:image_upload)` on a `RateLimitChecker` instance initialized with the current user.
2. The service builds a cache key from the user's ID (or IP address if no ID is available) and the action name.
3. It reads the current counter from Rails cache and compares it against the configured threshold for that action.
4. If the counter exceeds the threshold, the service records the action, logs a rate-limit hit to Datadog, and returns `true`.
5. If the counter is at or below the threshold, it returns `false` and no action is taken.

### Raising an error when a limit is exceeded

1. A caller invokes `check_limit!(:reaction_creation)` on a checker instance.
2. Internally, `limit_by_action` is called; if it returns `true`, the service raises `LimitReached` with the action's `retry_after` value.
3. The caller catches `LimitReached` and uses `retry_after` to construct a response (e.g., a 429 status with a Retry-After header and a localized message).
4. If `limit_by_action` returns `false`, `check_limit!` returns `nil` and the action proceeds normally.

### Tracking an action increment into the cache

1. After a user successfully completes a rate-limited action, a service calls `track_limit_by_action(:image_upload)`.
2. The service increments the cache counter for the user/action key, setting the expiry to the action's `retry_after` duration so the counter auto-expires after the window.

### Checking comment and article creation limits against the database

1. When `limit_by_action` is called for `comment_creation`, `published_article_creation`, or `published_article_antispam_creation`, the check queries the database for records created within the relevant time window rather than reading from the cache.
2. If the count of recent records exceeds the configured threshold, the limit is considered reached.

### Checking email recipient flood limits

1. A caller invokes `limit_by_email_recipient_address(address)` to check whether too many emails have recently been sent to a specific address.
2. The service queries `EmailMessage` for records sent to that address within the last 2 minutes.
3. If the count exceeds `Settings::RateLimit.email_recipient`, the method returns `true` to prevent further email sending.

## Failures / Exceptions

- If neither a user ID nor an IP address is available when building a cache key, `limit_cache_key` raises an `I18n`-translated error ("Invalid Cache Key: no unique component present").
- In end-to-end test environments (`ApplicationConfig["E2E"]` is truthy), both `check_limit!` and `limit_by_action` short-circuit and return `nil`/`false` respectively, bypassing all limits.
- Calling `limit_by_action` with an action name that has no corresponding `check_<action>_limit` method returns `false` without raising an error.
