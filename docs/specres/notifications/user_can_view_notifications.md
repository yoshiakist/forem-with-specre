---
id: "01KJ15MVQ9HCZ8PV80MQ828AQF"
name: "user_can_view_notifications"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/notifications_controller.rb`
- `app/controllers/notifications/counts_controller.rb`
- `app/controllers/notifications/reads_controller.rb`
- `app/decorators/notification_decorator.rb`
- `app/helpers/notifications_helper.rb`
- `app/models/notification.rb`
- `app/services/notifications.rb`
- `app/javascript/packs/initializers/initializeNotifications.js`
- `app/javascript/packs/notificationPage.js`
- `app/views/notifications/index.html.erb` (Template)
- `app/views/notifications/_notifications_list.html.erb` (Template)
- `app/views/notifications/_nav_menu.html.erb` (Template)
- `app/views/notifications/shared/_article_preview.html.erb` (Template)
- `app/views/notifications/shared/_comment_box.html.erb` (Template)
- `app/views/notifications/shared/_error.html.erb` (Template)
- `app/views/users/_notifications.html.erb` (Template)
- `spec/requests/notifications_spec.rb` (Test)
- `spec/requests/notification_counts_spec.rb` (Test)
- `spec/requests/notifications/reads_spec.rb` (Test)
- `spec/decorators/notification_decorator_spec.rb` (Test)
- `spec/helpers/notifications_helper_spec.rb` (Test)
- `spec/models/notification_spec.rb` (Test)
- `spec/system/notifications/notifications_page_spec.rb` (Test)
- `spec/system/link_for_tags_in_posts_in_notifications_spec.rb` (Test)
- `spec/factories/notifications.rb` (Test)

## Functional Overview

Authenticated users can view a paginated list of their notifications at `GET /notifications`, which renders notifications decorated via `NotificationDecorator` and filtered by type (posts, comments/mentions, or organization). Unauthenticated visitors are redirected to the magic link sign-in page. The page initially loads 8 notifications; the JavaScript client fetches subsequent batches using offset-based pagination driven by the last notification ID. Upon page load, the client automatically marks all unread notifications as read via `POST /notifications/reads`. A separate `GET /notifications/counts` endpoint returns the count of unread notifications for the current subforem, enabling the navigation bell badge to stay current without a full page reload.

## Design Intent

Offset-based pagination is used under the assumption that notification IDs correlate with `notified_at` timestamps, which keeps the query simple at the cost of possible edge-case ordering drift. The initial page renders server-side HTML for fast first paint; subsequent pages are fetched as HTML partials and appended to the DOM by the client, avoiding a separate JSON API layer. Marking notifications as read is deferred by 450 ms client-side to avoid marking items as read before the user has seen them.

## Scenarios

### Unauthenticated user visits the notifications page

1. User visits `GET /notifications` without being signed in.
2. The controller redirects them to the magic link sign-in page.

### Authenticated user views their personal notifications

1. Signed-in user visits `GET /notifications`.
2. The controller identifies the viewing user (defaulting to the current user; super admins may pass a `username` parameter to view another user's notifications).
3. The most recent 8 notifications scoped to the current subforem are fetched, decorated, and rendered in the `index` view.
4. The client automatically posts to `POST /notifications/reads` after a short delay, marking all unread notifications as read.

### User filters notifications by type

1. Signed-in user navigates to `/notifications` with a `filter` query parameter set to `posts` or `comments`.
2. When `filter=posts`, only notifications tied to published articles are shown.
3. When `filter=comments`, only comment and mention notifications are shown.
4. The filter dropdown in the nav menu fires a page navigation on change.

### User or org member views organization notifications

1. Signed-in user who is a member of an organization visits `GET /notifications` with `org_id` and `filter=org` (or `filter=comments` for comment/mention scope).
2. The controller verifies the user is an org member or a super admin before scoping notifications to the organization.
3. If neither condition is met, the org-scoped query is skipped and personal notifications are shown.
4. When org context is present, `POST /notifications/reads` with `org_id` also marks all unread organization notifications as read.

### User loads additional notifications via pagination

1. After the initial page renders, the client detects a `.notifications-paginator` element carrying the next-page URL (with an `offset` parameter equal to the last notification ID).
2. The client fetches the URL and receives an HTML partial rendered by the controller.
3. The partial is appended to the notifications container and reaction handlers are re-initialized.
4. When no further notifications exist, the load-more button is hidden.

### Client fetches unread notification count

1. When a logged-in user is on a page that is not the notifications page, the client calls `GET /notifications/counts`.
2. The endpoint returns a plain-text integer representing the number of unread notifications in the current subforem (returns `0` for unauthenticated requests).
3. The navigation bell badge displays this count and is hidden when the user clicks the notifications link.

## Failures / Exceptions

- If a notification rendering raises an error, `NotificationsHelper#render_notification_or_error` catches it, notifies Honeybadger, and renders the `shared/_error` partial in place of the broken notification so the rest of the list remains visible.
- `POST /notifications/reads` returns an empty `204 No Content` response when no authenticated user can be resolved (either no session or an invalid bearer token), leaving notification state unchanged.
- `NotificationDecorator#mocked_object` returns an empty stub struct when `json_data` is blank, preventing nil errors during template rendering of unsaved or incomplete notifications.
