---
id: "01KJ7FK7N2EJG4M5C7JYHGZGJ0"
name: "admin_views_overview_dashboard"
status: "draft"
---

## Related Files

- `app/controllers/admin/overview_controller.rb`
- `app/views/admin/overview/index.html.erb` (Template)
- `spec/requests/admin/overview_spec.rb` (Test)

## Functional Overview

The admin overview dashboard is the landing page of the admin panel. It displays two main areas: a deployment information card showing the last deploy time and the latest commit ID sourced from `ForemInstance`, and a help section listing getting-started links and external guides for Forem administrators. The page also renders notices and an analytics partial that are each covered by separate specre cards. Stats data is loaded asynchronously via a dedicated `stats` endpoint rather than inline.

## Design Intent

The `index` action is intentionally empty — it performs no database queries. All heavy data (community statistics) is deferred and loaded client-side via the separate `stats` endpoint, which accepts a `period` parameter and delegates to `Admin::StatsData`. This keeps the initial page load fast and avoids blocking on potentially slow aggregation queries.

## Scenarios

### Admin views the overview dashboard page

1. An authenticated admin navigates to the admin overview path.
2. The page renders the "Overview" heading, notices partial, and analytics partial.
3. The deployment information card is displayed, showing the last deploy time from `ForemInstance.deployed_at` and the latest commit ID from `ForemInstance.latest_commit_id` (falling back to "Not Available" if absent).
4. The help section is displayed with an ordered list of onboarding recommendations linking to admin documentation, the config section, welcome thread creation, tags management, pages and navigation, and external Forem admin guides.

### Admin views deployment info when a deploy timestamp is available

1. The environment variable `HEROKU_RELEASE_CREATED_AT` is set to a non-empty value.
2. An admin requests the overview page.
3. The deployment card shows that timestamp as the last deploy time.

### Admin views deployment info when no deploy timestamp is available

1. The environment variable `HEROKU_RELEASE_CREATED_AT` is not set.
2. An admin requests the overview page.
3. The deployment card shows the fallback value (nil or blank) for last deploy time.
4. The latest commit ID shows "Not Available" when `ForemInstance.latest_commit_id` returns nil.

### Admin requests stats data for a given period

1. An admin (or background client-side script) sends a GET request to the stats endpoint with an optional `period` parameter (7, 30, or 90 days).
2. The controller validates the period, defaulting to 7 if the value is not one of the allowed options.
3. `Admin::StatsData` is instantiated with the validated period and called; the resulting data is rendered as JSON.
