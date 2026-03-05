---
id: "01KJ73NQSZ78M36BRBYEKY5VHJ"
name: "system_tracks_email_link_clicks"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/ahoy/email_clicks_controller.rb`
- `app/workers/billboards/track_email_click_worker.rb`
- `spec/requests/ahoy/email_clicks_spec.rb` (Test)
- `spec/requests/ahoy/external_email_clicks_spec.rb` (Test)

## Functional Overview

When a user clicks a tracked link in an email, the system verifies the request's HMAC signature before processing the event. On valid requests, it publishes a click event via `AhoyEmail::Utils`, optionally records a billboard click event and updates the billboard's aggregate counts, optionally records a feed event for articles linked in the email, and refreshes the user's presence timestamp based on the email token. External (redirect-based) click tracking enqueues a background job (`Billboards::TrackEmailClickWorker`) to handle billboard attribution asynchronously. Invalid signatures are rejected with a 403 Forbidden response.

## Design Intent

Signature verification (via `AhoyEmail::Utils.signature` and `ActiveSupport::SecurityUtils.secure_compare`) prevents forged click events. Billboard count updates happen synchronously in the inline path but are offloaded to a low-priority Sidekiq worker in the external redirect path to avoid blocking the redirect response. Both paths share the same `update_billboard_counts` logic, ensuring click-through-rate calculations remain consistent.

## Key Members

- `t` (token) — Email message token used to look up the recipient and verify the signature
- `c` (campaign) — Campaign identifier included in the click event payload
- `u` (url) — Destination URL; used to derive the article path for feed event recording
- `s` (signature) — HMAC signature that must match the expected value computed from token, campaign, and URL
- `bb` — Optional billboard ID; when present, triggers billboard click recording and count updates

## Scenarios

### Valid click with no optional parameters

1. Client POSTs to `/ahoy/email_clicks` with token, campaign, URL, and a valid signature
2. System verifies the signature matches the expected HMAC; verification passes
3. System publishes a `:click` event via `AhoyEmail::Utils` with the token, campaign, URL, and controller reference
4. System looks up the `EmailMessage` by token, finds the associated user, and updates their presence timestamp
5. System returns HTTP 200 with an empty body

### Valid click with billboard parameter

1. Client POSTs with a valid signature and an additional `bb` parameter containing a billboard ID
2. System verifies the signature and publishes the click event
3. System creates a `BillboardEvent` with category `click` and context type `email`, linked to the billboard and the current user (if signed in)
4. System recalculates the billboard's click-through rate from aggregate impression and click counts, then persists the updated values
5. System returns HTTP 200

### Valid click on an article URL

1. Client POSTs with a valid signature and a URL whose path matches a published article
2. System verifies the signature and publishes the click event
3. System parses the URL path, finds the matching article, and creates a `FeedEvent` with category `click` and context type `email`
4. System returns HTTP 200

### External redirect click with billboard attribution

1. Client GETs `/ahoy/click` (the Ahoy redirect endpoint) with a destination URL that contains a `bb` query parameter
2. System enqueues a `Billboards::TrackEmailClickWorker` job carrying the `bb` value and the current user's ID
3. System redirects the client to the destination URL
4. Worker runs asynchronously, creates the `BillboardEvent`, and updates billboard aggregate counts inside a synchronous-commit-off transaction

### Invalid signature

1. Client POSTs with a signature that does not match the expected HMAC
2. System rejects the request with HTTP 403 and the body `"Invalid signature"`
3. No click event is published and no side effects occur

## Failures / Exceptions

- Billboard click recording and feed event recording each rescue `StandardError` and log the error to `Rails.logger`, allowing the main click acknowledgment (HTTP 200) to succeed even when these secondary writes fail
- `Billboards::TrackEmailClickWorker` is configured with `retry: 10` to handle transient failures in the asynchronous attribution path
