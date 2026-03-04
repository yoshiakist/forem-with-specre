---
id: "01KJCKB0GDJ4BTHW7NPDYBC25S"
name: "author_locks_article_discussion"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/discussion_locks_controller.rb`
- `app/controllers/articles_controller.rb`
- `app/models/discussion_lock.rb`
- `app/policies/discussion_lock_policy.rb`
- `app/views/articles/discussion_lock_confirm.html.erb`
- `app/views/articles/discussion_unlock_confirm.html.erb`
- `app/views/articles/_full_comment_area.html.erb`
- `spec/requests/discussion_locks_spec.rb` (Test)
- `spec/models/discussion_lock_spec.rb` (Test)
- `spec/policies/discussion_lock_policy_spec.rb` (Test)
- `spec/system/articles/user_discussion_locks_spec.rb` (Test)

## Functional Overview

An article author or admin can lock the discussion on their article to prevent new comments. The author navigates to a lock confirmation page that presents a form with optional "reason" and "notes" fields. On submission, a `DiscussionLock` record is created and associated with the article; the article cache is busted immediately. When a locked article's page renders, the comment form is replaced by a notice that displays the lock reason. The author may later visit an unlock confirmation page showing the current reason and notes, then submit a delete request to destroy the `DiscussionLock` record and restore the comment form. Authorization is enforced by `DiscussionLockPolicy`: only the article's own author and admins may create or destroy locks; suspended users are denied.

## Design Intent

Locking is modelled as a separate `DiscussionLock` record rather than a boolean flag on `Article` so that structured metadata (reason, notes, locking user) can be stored alongside the lock state. The uniqueness constraint on `article_id` ensures at most one active lock per article. Authorization is delegated entirely to Pundit so that the same policy governs both the confirmation views (via `authorize @article, :discussion_lock_confirm?`) and the create/destroy actions (via `authorize @discussion_lock`).

## Key Members

- `DiscussionLock#article_id` — foreign key to the locked article; must be unique
- `DiscussionLock#locking_user_id` — foreign key to the user who created the lock
- `DiscussionLock#reason` — optional public-facing explanation shown in the comment area
- `DiscussionLock#notes` — optional internal note visible only on the unlock confirmation page
- `@discussion_lock` (view) — when present in `_full_comment_area.html.erb`, triggers rendering of the lock-reason partial instead of the comment form

## Scenarios

### Author locks discussion

1. A signed-in author (or admin) visits `/:username/:slug/discussion_lock_confirm`.
2. The `discussion_lock_confirm` action in `ArticlesController` looks up the article by slug, authorizes the request, and initializes a blank `DiscussionLock` for the form.
3. The confirmation page renders, showing the article title and a form with "reason" and "notes" text fields.
4. The author fills in an optional reason and notes, then submits the form.
5. `DiscussionLocksController#create` receives the POST, authorizes the new lock record, persists it, busts the article cache, sets a success flash, and redirects to the article's manage page.

### Reader views a locked article

1. Any visitor loads an article page for which a `DiscussionLock` record exists.
2. `_full_comment_area.html.erb` detects the `@discussion_lock` instance variable is present.
3. Instead of the comment form, the partial `comments/discussion_lock_reason` is rendered, displaying the lock message and the stored reason.
4. No new-comment box or reply buttons are shown on the article, legacy comments, or individual comment pages.

### Author unlocks discussion

1. The author visits `/:username/:slug/discussion_unlock_confirm`.
2. The `discussion_unlock_confirm` action fetches the article by slug, authorizes the request, and loads the existing `DiscussionLock`.
3. The unlock confirmation page renders with the current reason and notes displayed for review.
4. The author submits the delete form.
5. `DiscussionLocksController#destroy` authorizes the lock record, destroys it, busts the article cache, sets a success flash, and redirects to the manage page.

### Unauthorized user attempts to lock

1. A signed-in user who is not the article author and is not an admin submits a POST to create a discussion lock for that article.
2. `DiscussionLockPolicy#create?` returns false.
3. Pundit raises `Pundit::NotAuthorizedError`; the lock is not created.

### Duplicate lock attempt

1. An author attempts to create a second `DiscussionLock` for an article that already has one.
2. The `article_id` uniqueness validation on `DiscussionLock` fails.
3. `DiscussionLocksController#create` does not persist the record, sets an error flash, and redirects back to the manage page.

## Failures / Exceptions

- **Non-author, non-admin user** — `DiscussionLockPolicy` denies `create?` and `destroy?`; `Pundit::NotAuthorizedError` is raised.
- **Suspended user** — Policy also denies create and destroy for users flagged as spam or suspended.
- **Article not found** — `discussion_lock_confirm` and `discussion_unlock_confirm` call `not_found` if no article matches the given slug.
- **Duplicate lock** — `DiscussionLock` validates uniqueness of `article_id`; saving fails and an error flash is shown.
- **Blank reason / notes** — `StringAttributeCleaner` converts empty strings and whitespace-only values to `nil` before validation.
