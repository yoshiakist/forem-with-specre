---
id: "01KJ6QCAKAT1EKMN80R2KK58YZ"
name: "author_views_analytics_dashboard"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/concerns/api/analytics_controller.rb`
- `app/controllers/api/v0/analytics_controller.rb`
- `app/controllers/api/v1/analytics_controller.rb`
- `app/services/analytics_service.rb`
- `app/javascript/analytics/client.js`
- `app/javascript/analytics/dashboard.js`
- `app/javascript/packs/analyticsDashboard.js`
- `app/javascript/packs/analyticsArticle.js`
- `app/views/dashboards/analytics.erb` (Template)
- `spec/requests/api/v0/analytics_spec.rb` (Test)
- `spec/requests/api/v1/analytics_spec.rb` (Test)
- `spec/services/analytics_service_spec.rb` (Test)
- `spec/support/shared_examples/api_analytics.rb` (Test)

## Functional Overview

Authors and organization members can view an analytics dashboard that aggregates engagement metrics — page views, reactions, comments, and follows — for their published articles. The dashboard fetches data through JSON API endpoints (`/api/analytics/totals`, `/api/analytics/historical`, `/api/analytics/past_day`, `/api/analytics/referrers`) that require API key or session authentication. The `AnalyticsService` performs all data aggregation: it loads articles scoped to the requesting user or organization, joins related activity records filtered by an optional date range and optional single article, and returns either lifetime totals or per-day breakdowns cached for seven days. The frontend charts module (`dashboard.js`) calls the historical and referrers endpoints, renders line charts for three time-range presets (week, month, all-time), writes summary stat cards, and lists the top referrer domains.

## Key Members

- `start_date` / `end_date` — ISO 8601 date strings that bound the analytics window; `start_date` is required for the `/historical` endpoint and validated by regex `\d{4}-\d{1,2}-\d{1,2}`.
- `organization_id` — optional parameter; when present the dashboard shows org-level aggregates and requires that the requesting user is a member of that organization.
- `article_id` — optional parameter; when present metrics are scoped to a single article owned by the owner.
- Cache key — `AnalyticsService#grouped_by_day` caches results in Rails.cache for 7 days, keyed by date range, owner type/id, and optional article id.

## Scenarios

### Author views personal lifetime totals

1. An authenticated author opens the analytics dashboard without specifying a date range or article.
2. The frontend calls `GET /api/analytics/totals` with no extra parameters.
3. `AnalyticsService` loads all published articles belonging to the user, then counts comments with positive score, follows, reactions by category (like, readinglist, unicorn), and total page views with average read time.
4. The API responds with a JSON object containing `comments`, `follows`, `reactions`, and `page_views` totals.
5. The dashboard renders summary stat cards with those totals.

### Author views historical chart for a date range

1. The author selects a time-range preset (week, month, or all-time) on the dashboard.
2. The frontend calls `GET /api/analytics/historical?start=<date>` (and optionally `end=<date>`).
3. The controller validates that `start` is present and that both date strings match `YYYY-M-D` format, then delegates to `AnalyticsService#grouped_by_day`.
4. The service iterates each calendar day in the range and collects counts for comments, follows, reactions, and page views; the result is cached for 7 days.
5. The API responds with a JSON object keyed by ISO date, each value containing the four metric groups.
6. The frontend draws line charts for reactions, comments, and readers using the returned data.

### Author views referrer domains

1. Alongside the historical request, the frontend calls `GET /api/analytics/referrers?start=<date>`.
2. `AnalyticsService#referrers` groups page views by domain, orders by total view count descending, and returns the top 20 domains.
3. The dashboard renders the referrer list in a table.

### Organization member views org-level analytics

1. An authenticated user who belongs to an organization selects that organization in the dashboard's organization menu.
2. The frontend appends `organization_id=<id>` to all API calls.
3. The controller looks up the organization, runs a Pundit `analytics?` authorization check, and sets the owner to the organization.
4. `AnalyticsService` scopes all queries to articles whose `organization_id` matches, then returns the same metric structure as for personal analytics.
5. Non-members receive a 401 response.

### Author views analytics scoped to a single article

1. The author opens the per-article analytics view (initiated by `analyticsArticle.js`).
2. `article_id` and optionally `organization_id` are read from the article element's dataset and forwarded to all API calls.
3. `AnalyticsService` restricts `article_data` to that one article; if the article does not belong to the owner, an `ArgumentError` is raised and the API responds with 422.
4. Metrics are returned and rendered the same way as the full dashboard.

## Failures / Exceptions

- Missing `start` parameter on `/historical` — controller raises `ArgumentError` → 422 Unprocessable Entity with a localized message.
- Invalid date format on `/historical` — `valid_date_params?` returns false → same `ArgumentError` path → 422.
- Unauthenticated request — `authenticate_with_api_key_or_current_user!` halts → 401 Unauthorized.
- Organization analytics requested by non-member — Pundit `NotAuthorizedError` → 401.
- `article_id` belongs to a different owner — `AnalyticsService` raises `ArgumentError` ("no stats") → 422.
