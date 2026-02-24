---
id: "01KJ71NMHAZE5XNJDG4DDR4DW4"
name: "system_determines_digest_email_send_eligibility"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/email_digest_article_collector.rb`
- `spec/services/email_digest_article_collector_spec.rb` (Test)

## Functional Overview

`EmailDigestArticleCollector#should_receive_email?` decides whether a given user is eligible to receive a digest email at the moment it is called. The decision is driven by the timestamp of the user's most recent digest email and whether the user has recently clicked a digest email link. A user is always eligible when they have never received a digest email. If the last email was sent within the past 18 hours, the user is blocked regardless of click activity. Beyond the 18-hour floor, the system consults the configurable `periodic_email_digest` window (stored in `Settings::General`): a user who clicked the last email is immediately eligible again, while a user without a recent click (within 30 days) must wait until that window has elapsed before receiving another email.

## Design Intent

The multi-layered gate prevents inbox flooding while rewarding engaged users. The hard 18-hour cooldown stops accidental re-sends; the click-based fast path re-engages users who have demonstrated interest; the periodic window (site-configurable) lets operators tune cadence without code changes. The 30-day `CLICK_LOOKBACK` constant prevents very old clicks from unfairly accelerating future sends.

## Key Members

- `CLICK_LOOKBACK` — constant (30 days): the window within which a clicked digest email counts as a "recent" click for eligibility purposes.
- `force_send` — constructor parameter: reserved for forced sends; not consulted by `should_receive_email?` in the current implementation.
- `Settings::General.periodic_email_digest` — site-wide setting (days): the minimum gap between digest emails for users without a recent click.

## Scenarios

### User has never received a digest email

1. The system checks whether any digest email has ever been sent to the user.
2. No record is found, so `last_email_sent` returns nil.
3. The system immediately returns eligible (true).

### Last email was sent within 18 hours

1. The system retrieves the timestamp of the most recent digest email sent to the user.
2. The timestamp falls within the past 18 hours.
3. The system returns ineligible (false) regardless of click state.

### Last email was sent more than 18 hours ago and the most recent email was clicked

1. The system confirms the last email was sent more than 18 hours ago.
2. The system checks whether the user's most recent digest email has a `clicked_at` value; it does.
3. The system returns eligible (true) without consulting the periodic window.

### Last email was sent more than 18 hours ago, not clicked, but outside the periodic window

1. The system confirms the last email was sent more than 18 hours ago.
2. The most recent email was not clicked, so the click fast-path is skipped.
3. The system compares the last send timestamp against the configured `periodic_email_digest` window.
4. The last send falls outside (older than) that window, so the periodic threshold is not blocking.
5. The system also checks whether any digest email was clicked within the past 30 days (`CLICK_LOOKBACK`); the result does not change eligibility at this stage.
6. The system returns eligible (true).

### Last email was sent more than 18 hours ago, not clicked, and within the periodic window

1. The system confirms the last email was sent more than 18 hours ago.
2. The most recent email was not clicked, so the click fast-path is skipped.
3. The system compares the last send timestamp against the configured `periodic_email_digest` window.
4. The last send falls within that window, so the system checks for a recent tracked click within the 30-day lookback.
5. No clicked digest email is found within the past 30 days.
6. The system returns ineligible (false).
