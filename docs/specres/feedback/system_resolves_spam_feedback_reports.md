---
id: "01KJ25Q4XMSVV0Y8FHDRRK1JYD"
name: "system_resolves_spam_feedback_reports"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/users/resolve_spam_reports.rb`
- `spec/services/users/resolve_spam_reports_spec.rb` (Test)

## Functional Overview

`Users::ResolveSpamReports` is a service object that bulk-resolves all open spam `FeedbackMessage` records associated with a given user. When called with a user, it finds every `FeedbackMessage` whose category is "spam" and status is "Open", then matches them against the user's profile URL, all of their article URLs, and all of their comment URLs — accepting both the canonical path form and the fully-qualified absolute URL form. All matched reports are updated to "Resolved" in a single bulk operation per content type.

## Scenarios

### No reports exist for the user

1. The service is called with a user who has no associated spam reports.
2. The system queries for open spam `FeedbackMessage` records matching the user's profile, articles, and comments.
3. No records are found; the service completes without error and without modifying any data.

### Resolving profile spam reports

1. One or more open spam `FeedbackMessage` records exist whose `reported_url` matches either the user's profile path or the fully-qualified profile URL.
2. The service is called with that user.
3. The system bulk-updates all matching profile reports to status "Resolved".

### Resolving article spam reports

1. One or more open spam `FeedbackMessage` records exist whose `reported_url` matches the path or fully-qualified URL of any article authored by the user.
2. The service is called with that user.
3. The system collects all article paths, expands each to its absolute URL form, and bulk-updates all matching article reports to status "Resolved".

### Resolving comment spam reports

1. One or more open spam `FeedbackMessage` records exist whose `reported_url` matches the path or fully-qualified URL of any comment authored by the user.
2. The service is called with that user.
3. The system collects all comment paths, expands each to its absolute URL form, and bulk-updates all matching comment reports to status "Resolved".

### Non-spam or other-user reports are not affected

1. Open `FeedbackMessage` records exist for the user's content but with a category other than "spam" (e.g., "other", "harassment"), or spam reports exist for a different user's content.
2. The service is called with the target user.
3. The system leaves all non-spam reports and all other-user reports unchanged in status "Open".

## Design Intent

Each content type (profile, articles, comments) is matched against both its relative path and its absolute URL form. This dual-form matching ensures reports are found regardless of which URL representation was used when the report was submitted.

## Key Members

- `user` — the `User` whose associated spam reports will be resolved; provides `.path`, `.articles`, and `.comments` for URL enumeration.
