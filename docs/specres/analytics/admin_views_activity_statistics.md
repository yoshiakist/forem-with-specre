---
id: "01KJ6QD968CHB6HNK748HR81KV"
name: "admin_views_activity_statistics"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/views/admin/overview/_analytics.html.erb` (Template)
- `spec/system/admin/admin_visits_overview_spec.rb` (Test)

## Functional Overview

The admin overview page renders an Activity Statistics panel that displays four platform-wide engagement metrics — Published Posts, Comments, Public Reactions, and New Users — each loaded asynchronously via a `data-stat` attribute. The panel includes a dropdown calendar button that lets the admin switch the reporting time period between the last 7, 30, or 90 days. All stat values begin as "Loading..." placeholders until a JavaScript handler populates them after the page mounts.

## Design Intent

Stat values are deliberately rendered as placeholders (`Loading...`) rather than server-rendered numbers to keep the initial page response fast and avoid heavy database aggregation on every admin page visit. The `js-period-selector` radio inputs and `js-loading-placeholder` spans serve as stable JavaScript hooks, keeping HTML semantics and JS targeting decoupled from CSS class naming.

## Scenarios

### Admin opens the Activity Statistics panel

1. A super admin navigates to the admin overview page.
2. The Activity Statistics section header is visible.
3. Four stat cards are present: Published Posts, Comments, Public Reactions, and New Users.
4. Each card initially displays "Loading..." while waiting for the asynchronous data fetch.
5. Once the data loads, each card displays the count for the currently selected time period.

### Admin changes the time period

1. The admin clicks the calendar icon button next to the "Activity Statistics" heading.
2. A dropdown appears containing three radio options: Last 7 days, Last 30 days, and Last 90 days.
3. "Last 7 days" is selected by default (checked on first render).
4. The admin selects a different period (e.g., Last 30 days).
5. The stat cards update to reflect counts for the chosen time window.

## Failures / Exceptions

- If the asynchronous data request fails, the "Loading..." placeholder remains visible with no automatic retry or error message in the template itself.
