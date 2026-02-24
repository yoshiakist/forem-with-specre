---
id: "01KJ6QD968CHB6HNK748HR81KV"
name: "admin_views_activity_statistics"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/views/admin/overview/_analytics.html.erb` (Template)
- `app/controllers/admin/overview_controller.rb`
- `app/services/admin/stats_data.rb`
- `app/javascript/packs/admin/overview.jsx`
- `spec/system/admin/admin_visits_overview_spec.rb` (Test)
- `spec/services/admin/stats_data_spec.rb` (Test)
- `spec/requests/admin/overview_spec.rb` (Test)

## Functional Overview

The admin overview page renders an Activity Statistics panel that displays four platform-wide engagement metrics — Published Posts, Comments, Public Reactions, and New Users — each loaded asynchronously via a `data-stat` attribute. The panel includes a dropdown calendar button that lets the admin switch the reporting time period between the last 7, 30, or 90 days. All stat values begin as "Loading..." placeholders until a JavaScript handler populates them after the page mounts. On the backend, the `GET /admin/stats` endpoint is handled by `Admin::OverviewController#stats`, which delegates to the `Admin::StatsData` service. That service accepts a period parameter (7, 30, or 90 days), queries the relevant models over the corresponding time window, and returns a JSON object containing the four metric counts along with the resolved period value.

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

### Stats API returns counts for the requested period

1. The browser issues a `GET /admin/stats?period=<n>` request with a period value of 7, 30, or 90.
2. The controller validates and passes the period to `Admin::StatsData`.
3. The service queries Articles, Comments, Reactions, and Users created within the time window starting at the beginning of the day `n` days ago through the current moment.
4. The endpoint responds with JSON containing `published_posts`, `comments`, `public_reactions`, `new_users`, and the resolved `period`.

### Stats API defaults to 7 days when no period is supplied

1. The browser issues a `GET /admin/stats` request without a `period` parameter.
2. The controller treats the missing parameter as period 7.
3. The response contains counts for the last 7 days and `"period": 7`.

### Stats API rejects an unrecognised period value

1. The browser issues a `GET /admin/stats?period=14` (or any value not in 7, 30, 90).
2. The controller falls back to the default period of 7.
3. The response contains counts for the last 7 days and `"period": 7`.

## Failures / Exceptions

- If the asynchronous data request fails (network error or non-OK response), the JavaScript `showError` function replaces the stats container content with an inline error message styled in the danger accent colour. No automatic retry is performed.
- If the asynchronous data request fails before the stats have loaded, the "Loading..." placeholder may remain visible until the error handler fires.
