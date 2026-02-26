---
id: "01KJBN4DMMSF9BX518JG772WEB"
name: "moderator_approves_article_for_tag_restricted_publication"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/article_approvals_controller.rb`
- `spec/requests/article_approvals_spec.rb` (Test)

## Functional Overview

When a moderator submits an approval decision for an article, the system verifies that the requesting user is authorized to perform that approval. For non-admin users, it checks that the article can be moderated by the user, that at least one of the article's tags requires approval, and that the user holds the tag-moderator role for each tag that requires approval. If all checks pass, the article's `approved` flag is updated and the user is redirected to the article's mod view. Admin users bypass all tag-based authorization checks entirely.

## Design Intent

The approval gate is intentionally tied to individual tags rather than a flat moderator role. This allows fine-grained delegation: a user who moderates `tag-a` can approve articles tagged with `tag-a` but not articles tagged only with `tag-b`. The "at least one requires approval" guard prevents tag moderators from approving articles that were never subject to tag-restricted publication in the first place.

## Scenarios

### Non-moderator user attempts approval

1. A signed-in user who holds no moderator role sends a POST to `/article_approvals` for a tag-restricted article.
2. Pundit's `moderate?` policy denies the request.
3. A `Pundit::NotAuthorizedError` is raised and no update is persisted.

### Tag moderator approves an article with a matching tag

1. A user with the `tag_moderator` role for a tag that `requires_approval` and the `trusted` role signs in.
2. The user sends a POST to `/article_approvals` with `approved: true` for an article tagged with that tag.
3. The system confirms the user can moderate the article and that the tag requires approval.
4. The article's `approved` attribute is set to `true` and the user is redirected to the article's mod path.

### Tag moderator approves an article where only some tags require approval

1. An article carries two tags: one that `requires_approval` and one that does not.
2. A tag moderator for the requiring tag sends a POST to `/article_approvals` with `approved: true`.
3. The "at least one tag requires approval" check passes; the moderator is authorized for the requiring tag.
4. The article is approved and the user is redirected to the mod view.

### Tag moderator is blocked when no tags require approval

1. An article carries tags none of which have `requires_approval` set to `true`.
2. A tag moderator for one of those tags attempts to approve the article.
3. The system finds no tag that requires approval and raises `Pundit::NotAuthorizedError`.
4. The article's `approved` flag remains unchanged.

### Admin user approves any article unconditionally

1. A user with the `admin` role signs in and sends a POST to `/article_approvals` for any article.
2. The system detects `current_user.any_admin?` is truthy and skips all tag-based authorization checks.
3. The article's `approved` attribute is updated to the submitted value and the user is redirected to the mod path.

## Failures / Exceptions

- `Pundit::NotAuthorizedError` is raised when the user lacks the `moderate?` permission for the article, when no tag on the article requires approval, or when the user does not hold update permission for every tag that requires approval.
