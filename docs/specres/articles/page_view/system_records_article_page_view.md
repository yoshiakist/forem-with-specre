---
id: "01KJBV508Z7X8FZ7BZP7XQNTN1"
name: "system_records_article_page_view"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/javascript/packs/baseTracking.js`
- `app/controllers/page_views_controller.rb`
- `app/models/page_view.rb`
- `app/workers/articles/update_page_views_worker.rb`
- `app/workers/articles/update_organic_page_views_worker.rb`
- `spec/models/page_view_spec.rb` (Test)
- `spec/requests/page_views_spec.rb` (Test)
- `spec/workers/articles/update_page_views_worker_spec.rb` (Test)
- `spec/factories/page_views.rb` (Test)

## Functional Overview

When a visitor loads an article page, the browser sends a POST to `/page_views` containing the article ID, referrer URL, and user agent. For authenticated users every impression is forwarded; for unauthenticated visitors only 1-in-10 impressions are sampled, and each recorded impression is credited as ten views. The controller enqueues `Articles::UpdatePageViewsWorker` to fire two minutes later. That worker creates a `PageView` record (skipping unpublished articles and the article's own author), updates the article's `page_views_count` in place, and—when the referrer is Google—schedules `Articles::UpdateOrganicPageViewsWorker` 25 minutes out to recount Google-sourced views for the past month. On creation the `PageView` model parses the referrer URL to extract and persist its domain and path, and triggers an activity update for authenticated users.

## Design Intent

The 1-in-10 sampling for anonymous visitors avoids recording every impression while still producing accurate aggregate counts: each sampled impression carries a `counts_for_number_of_views` of 10 to compensate for the 90% that are dropped. Deferring `PageView` creation to a background worker decouples the HTTP response time from database writes, and the `until_executing` / `replace` Sidekiq lock prevents duplicate jobs from racing to create the same record.

## Key Members

- `counts_for_number_of_views` — integer stored on each `PageView`; 1 for authenticated users, 10 for anonymous visitors; summed to derive `article.page_views_count`.
- `VISITOR_IMPRESSIONS_AGGREGATE_COUNTS_FOR_NUMBER_OF_VIEWS` — constant (value: 10) in `PageViewsController` that pairs with the client-side 1-in-10 sampling rate.
- `GOOGLE_REFERRER` — constant (`"https://www.google.com/"`) used in both workers to identify organic search traffic.

## Scenarios

### Authenticated user views an article

1. The browser detects an article page and, after a 1.8-second delay, confirms the user is logged in.
2. The browser POSTs article ID, referrer, and user agent to `POST /page_views` with the CSRF token.
3. The controller attaches the session user ID to the parameters and enqueues `Articles::UpdatePageViewsWorker` to run two minutes later.
4. The worker verifies the article is published and that the viewer is not the article's author, then creates a `PageView` with `counts_for_number_of_views` of 1.
5. The worker sums all page view counts for the article and updates `article.page_views_count` if the total has increased.

### Anonymous visitor views an article (sampled impression)

1. The browser detects an article page and confirms the visitor is not logged in.
2. The browser generates a random number from 0–9; only when it equals 1 does the impression proceed.
3. The browser POSTs article ID, referrer, and user agent to `POST /page_views`.
4. The controller sets `counts_for_number_of_views` to 10 (compensating for the 9 dropped impressions) and enqueues `Articles::UpdatePageViewsWorker`.
5. The worker creates the `PageView` and updates `article.page_views_count` using the weighted sum.

### Page view arrives from Google search

1. A user (authenticated or anonymous sampled) views an article referred from `https://www.google.com/`.
2. After the `PageView` record is created and the article count updated, the worker detects the Google referrer.
3. `Articles::UpdateOrganicPageViewsWorker` is scheduled to run 25 minutes later.
4. That worker counts all Google-referred page views created in the past month and writes the result to `article.organic_page_views_past_month_count`.

### Page view is skipped for unpublished or self-authored article

1. The worker receives parameters for an article that is either unpublished or authored by the same user who viewed it.
2. The worker exits without creating a `PageView` or updating any counts.

## Failures / Exceptions

- If the article ID is not found, the worker exits immediately without creating a record.
- A duplicate `PageView` caused by a race condition (two jobs executing simultaneously) raises `ActiveRecord::RecordNotUnique`; the worker catches it and exits silently, since the first job already recorded the view.
- A validation failure raises `ActiveRecord::RecordInvalid`; the worker logs the error with the offending parameters and exits without updating counts.
