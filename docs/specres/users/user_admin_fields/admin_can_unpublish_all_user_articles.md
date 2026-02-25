---
id: "01KJ9N9GCJGH8BYDJ7Y3QJ140H"
name: "admin_can_unpublish_all_user_articles"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/admin/users_controller.rb`
- `app/views/admin/users/modals/_unpublish_modal.html.erb` (Template)
- `spec/requests/admin/users_spec.rb` (Test)

## Functional Overview

An authorized admin or moderator can unpublish all of a target user's articles in a single action. When the action is triggered, the system enqueues a background job (`Moderator::UnpublishAllArticlesWorker`) to process the unpublishing asynchronously. A `Note` record is created on the target user to log who performed the action and why. The action is available to moderator-role users via the `unpublish_all_articles?` policy, which is resolved through `MODROLE_ACTIONS_TO_POLICIES` rather than the standard admin authorization path. The action responds to both HTML and JSON formats.

## Design Intent

The unpublishing is performed asynchronously via a background worker to avoid blocking the web request when a user has many articles. Creating a `Note` record provides an audit trail visible on the admin user detail page. The policy delegation via `MODROLE_ACTIONS_TO_POLICIES` allows moderators (who do not hold full admin access) to perform this specific action without granting broader admin privileges.

## Key Members

- `Moderator::UnpublishAllArticlesWorker` — background job that unpublishes all articles and deletes all comments belonging to the target user; called with `(target_user.id, current_user.id, "moderator")`
- `Note` with `reason: "unpublish_all_articles"` — audit record created on the target user linking the action to the performing admin
- `params[:note][:content]` — optional custom note text; falls back to `"<admin_username> unpublished all articles"` when absent
- `unpublish_all_articles?` policy — Pundit policy checked via `authorize_admin` before the action runs

## Scenarios

### Successful unpublish via HTML

1. An authorized admin opens the unpublish modal on the target user's admin detail page and submits the form without entering a custom note.
2. The system looks up the target user by `params[:id]`.
3. `Moderator::UnpublishAllArticlesWorker` is enqueued with the target user's ID, the current admin's ID, and the role string `"moderator"`.
4. A `Note` is created on the target user with `reason: "unpublish_all_articles"` and the default content `"<admin_username> unpublished all articles"`.
5. A success flash message is set and the admin is redirected to the target user's admin detail page.

### Successful unpublish via JSON

1. An authorized client sends a POST request to `/admin/member_manager/users/:id/unpublish_all_articles` with `Accept: application/json`.
2. The system looks up the target user by `params[:id]`.
3. `Moderator::UnpublishAllArticlesWorker` is enqueued with the target user's ID, the current admin's ID, and the role string `"moderator"`.
4. A `Note` is created on the target user with `reason: "unpublish_all_articles"` and the default content.
5. The system responds with a JSON body containing `{ message: "<localized success message>" }`.

### Successful unpublish with custom note

1. An authorized admin opens the unpublish modal and enters custom text in the note field before submitting.
2. `Moderator::UnpublishAllArticlesWorker` is enqueued as in the HTML scenario.
3. A `Note` is created on the target user with `reason: "unpublish_all_articles"` and `content` set to the custom text provided by the admin.
4. The admin is redirected to the target user's admin detail page with a success flash message.

## Failures / Exceptions

- If the requesting user does not satisfy the `unpublish_all_articles?` policy, authorization fails before any work is performed (handled by `authorize_admin` via Pundit).
- If `params[:id]` does not correspond to an existing user, `User.find` raises `ActiveRecord::RecordNotFound`, which Rails resolves to a 404 response.
