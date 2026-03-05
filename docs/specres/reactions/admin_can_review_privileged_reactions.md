---
id: "01KHZ593PHDRQRWR1673HQ654Q"
name: "admin_can_review_privileged_reactions"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/privileged_reactions_controller.rb`
- `app/views/admin/privileged_reactions/index.html.erb`
- `app/models/privileged_reaction.rb`
- `spec/requests/admin/privileged_reactions_spec.rb` (Test)

## Functional Overview

Administrators can view a paginated, searchable list of privileged reactions (thumbsup, thumbsdown, vomit) cast by moderators and trusted users on articles, comments, and user profiles. The index page fetches all reactions belonging to privileged categories, ordered by most recent first, and supports filtering by the reacting user's username and by reaction category via Ransack-backed search. Each row links to the reacting user's admin profile page and to the content that was reacted upon.

## Scenarios

### Admin views the privileged reactions index

1. An authenticated admin navigates to `GET /admin/moderations/privileged_reactions`.
2. The system queries all `Reaction` records in privileged categories (thumbsup, thumbsdown, vomit), eager-loading the reacting user and the reactable target, ordered by creation date descending.
3. Results are paginated at 25 per page and rendered in a table showing the reaction ID, reacting username, reactable type, reaction category, a link to the reacted-upon content, and the reaction date.

### Admin filters reactions by username

1. The admin submits the search form with a username substring in the "User" field.
2. Ransack applies a `user_username_cont` filter and re-fetches the matching reactions.
3. The table refreshes to show only reactions cast by users whose usernames contain the entered text.

### Admin filters reactions by category

1. The admin selects a category (thumbsup, thumbsdown, or vomit) from the dropdown and submits the form.
2. Ransack applies a `category_eq` filter and re-fetches the matching reactions.
3. The table displays only reactions of the selected category.

### Non-admin user is blocked from the index

1. A regular (non-admin) user attempts to access `GET /admin/moderations/privileged_reactions`.
2. The system raises `Pundit::NotAuthorizedError`, blocking access to the page.

### Single-resource admin with ModeratorAction resource accesses the page

1. A user granted the single-resource admin role scoped to `ModeratorAction` signs in and requests the moderator actions index.
2. The system responds with HTTP 200, granting access within the permitted resource scope.

## Failures / Exceptions

- Accessing the index without admin privileges raises `Pundit::NotAuthorizedError`.
- Reactions whose reactable has been deleted are silently skipped in the view (the template guards with `reaction.reactable` presence before rendering the row).
