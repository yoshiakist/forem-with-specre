---
id: "01KJ9N2FZZB07P8ZDF61M9Y9CJ"
name: "admin_can_view_user_detail_page"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `app/javascript/admin/controllers/user_controller.js`
- `app/javascript/admin/controllers/users/tools/ajax_controller.js`
- `app/javascript/packs/admin/editUser.jsx`
- `app/javascript/packs/admin/users/editUserModals.js`
- `app/javascript/packs/admin/users/gdprDeleteRequests.jsx`
- `app/views/admin/users/show.html.erb`
- `app/views/admin/users/show/_tabs.html.erb`
- `app/views/admin/users/show/overview/_stats.html.erb`
- `app/views/admin/users/show/articles/_index.html.erb`
- `app/views/admin/users/show/comments/_index.html.erb`
- `app/views/admin/users/show/flags/_index.html.erb`
- `app/views/admin/users/show/notes/_form.html.erb`
- `app/views/admin/users/show/notes/_index.html.erb`
- `app/views/admin/users/show/reports/_index.html.erb`
- `app/views/admin/users/show/unpublish_logs/_index.html.erb`
- `spec/requests/admin/users_spec.rb` (Test)

## Functional Overview

When an admin navigates to a user's detail page (`GET /admin/member_manager/users/:id`), the system loads the user record along with supporting data — articles, comments, notes, feedback reports, vomit reactions, unpublish-all audit logs, organizations, and organization memberships — and renders the page organized into a horizontal tab navigation bar. The active tab is determined by the `tab` query parameter; any unrecognized value defaults to `overview`. Each tab shows a distinct slice of information: overview presents aggregate stats and role/organization/credit/tag-moderation panels; notes allows viewing and submitting admin notes; emails shows email history; articles and comments list published content; flags shows vomit reactions against the user; reports shows feedback messages; and unpublish_logs appears only when a prior "unpublish all" action exists. The `edit` action additionally loads the most recent ten notes and the related feedback data for a sidebar edit form. Adding a note is handled as part of the `update` action when a `new_note` parameter is present.

## Design Intent

The tabbed layout keeps the detail page lightweight by loading all data server-side in a single request and conditionally rendering sections based on `@current_tab`. This avoids separate AJAX requests for each tab while still maintaining a clear separation of concern in the view layer. The `unpublish_logs` tab is intentionally hidden from the navigation when no audit log record exists, reducing visual noise for users who have never had a bulk unpublish. The `set_banishable_user` helper applies a business rule — a user is only eligible for banishment if they are new (account and comments both within 100 days), unless the acting admin is a super_admin or support_admin.

## Key Members

- `@current_tab: String` — the active tab name, derived from the `tab` query parameter; validated against `Constants::UserDetails::TAB_LIST`; defaults to `"overview"`
- `@notes: ActiveRecord::Relation` — up to 10 most recent admin notes for the user, ordered by creation date descending
- `@articles: ActiveRecord::Relation` — all of the user's articles ordered by creation date descending
- `@comments: ActiveRecord::Relation` — all of the user's comments ordered by creation date descending
- `@organizations: ActiveRecord::Relation` — the user's organizations ordered by name
- `@organization_memberships: ActiveRecord::Relation` — the user's organization memberships joined and ordered by organization name
- `@related_reports: ActiveRecord::Relation` — up to 15 most recent feedback messages where the user is reporter, affected party, or offender
- `@related_vomit_reactions: ActiveRecord::Relation` — up to 15 most recent vomit reactions on the user's articles, comments, or user record directly
- `@user_vomit_reactions: ActiveRecord::Relation` — vomit reactions directly against the user record; used to calculate `@countable_flags`
- `@countable_flags: Integer` — count of non-invalid vomit reactions against the user
- `@unpublish_all_data` — either an `AuditLog::UnpublishAllsQuery` result set (when on the `unpublish_logs` tab) or a boolean-like existence check (on all other tabs)
- `@banishable_user: Boolean` — whether the banish action is available for this user given their account age and comment history
- `@last_email_verification_date: Date` — the date of the user's last email verification, sourced from `EmailAuthorization`

## Scenarios

### Viewing the overview tab (default)

1. Admin navigates to `/admin/member_manager/users/:id` without a `tab` parameter (or with an unrecognized value).
2. System finds the user by ID, resolves `@current_tab` to `"overview"`, and loads all supporting data.
3. The page renders a profile header, the horizontal tab navigation with "Overview" highlighted, and an overview panel.
4. The overview panel shows aggregate stats (comments count, articles count, reactions count, followers, following, badges) followed by panels for roles, tag moderation, organizations, and credits.

### Switching between tabs

1. Admin clicks a tab link (e.g., "Articles") in the horizontal navigation bar.
2. The browser navigates to `/admin/member_manager/users/:id?tab=articles`.
3. System validates the `tab` parameter against the allowed tab list; if valid, sets `@current_tab` accordingly.
4. Only the content section corresponding to the active tab is rendered; all other sections are suppressed.
5. The active tab link receives the `crayons-navigation__item--current` class and an `aria-current="page"` attribute.

### Viewing the notes tab and reading existing notes

1. Admin clicks the "Notes" tab, navigating to `?tab=notes`.
2. The system renders two side-by-side panels: a write-note form on the left and a list of up to 10 existing notes on the right.
3. Each existing note displays its content, the reason it was created, the author's username, and its timestamp.
4. If no notes exist, an empty-state message is shown indicating that no notes have been written for this user yet.

### Adding a new note from the notes tab

1. Admin fills in the text area on the "Write a note" form and submits.
2. The form sends a PATCH request to `/admin/member_manager/users/:id` with a `user[new_note]` parameter.
3. The `update` action detects the `new_note` parameter and calls `add_note`, which creates a `Note` record with `reason: "misc_note"` attributed to the current admin.
4. The system redirects back to the user detail page, where the new note appears at the top of the notes list.

### Viewing published articles

1. Admin clicks the "Articles" tab, navigating to `?tab=articles`.
2. The system renders a list of the user's published articles, each shown as a link with its publication date.
3. If the user has no published articles, an empty-state message "No Published Articles" is shown.
4. A link to the user's dashboard is provided so the admin can also view unpublished posts.

### Viewing comments

1. Admin clicks the "Comments" tab, navigating to `?tab=comments`.
2. The system renders a list of all the user's comments, each shown as a truncated link to the comment's page.
3. If the user has no comments, an empty-state message "No Comments" is shown.

### Viewing flags

1. Admin clicks the "Flags" tab, navigating to `?tab=flags`.
2. The system renders a summary showing the count of non-invalid vomit reactions (`@countable_flags`) and the user's overall score.
3. Below the summary, a table of up to 15 vomit reactions against the user's articles, comments, or user record is shown with the reactors and timestamps.
4. If no vomit reactions exist, a message "No flags received against this user" is shown.

### Viewing reports

1. Admin clicks the "Reports" tab, navigating to `?tab=reports`.
2. The system renders a list of up to 15 feedback messages in which the user is the reporter, the affected party, or the offender.
3. Each report shows its category, status indicator (open in red, resolved in green), message, reported URL, and timestamp.
4. If no reports exist, an empty-state message is shown.

### Viewing unpublish logs (conditional tab)

1. The "Unpublish Logs" tab link appears in the navigation only when an "unpublish all articles" audit log exists for the user.
2. Admin clicks the tab, navigating to `?tab=unpublish_logs`.
3. The system queries the full unpublish audit log for this user and renders a list of the articles that were unpublished, with links and an edit link for each.
4. Articles that have since been republished are marked with a "(was republished)" label.
5. The associated comments from the same bulk-unpublish event are listed below the articles.

## Failures / Exceptions

- Navigating to the detail page for a non-existent user ID raises `ActiveRecord::RecordNotFound`, which the application handles as a 404.
- Accessing the page as a non-admin raises `Pundit::NotAuthorizedError`.
- If the `tab` query parameter contains an unrecognized value, it is silently ignored and the `overview` tab is displayed instead.
- The "Unpublish Logs" tab link is hidden entirely when no audit log record exists, preventing the admin from navigating to an empty tab.
