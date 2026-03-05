---
id: "01KJTZE81B7VMF20GAZPA9PSNF"
name: "author_deletes_article"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/controllers/articles_controller.rb`
- `app/models/article.rb`
- `app/policies/article_policy.rb`
- `app/services/articles/destroyer.rb`
- `app/views/articles/delete_confirm.html.erb` (Template)
- `spec/services/articles/destroyer_spec.rb` (Test)
- `spec/requests/articles/articles_destroy_spec.rb` (Test)
- `spec/system/articles/user_deletes_an_article_spec.rb` (Test)
- `spec/models/article_destroy_spec.rb` (Test)
- `spec/policies/article_policy_spec.rb` (Test)

## Functional Overview

An authenticated article author (or admin/org admin) can permanently delete one of their articles through a two-step confirmation flow. The author first visits a dedicated confirmation page (`delete_confirm`) that displays the article title and warns about permanence, then submits the deletion form. The `Articles::Destroyer` service performs the actual deletion: it caches comment IDs before calling `destroy!` on the article, removes all article-level notifications, and — if comments existed — removes their notifications as well. After deletion the user is redirected to their dashboard.

## Design Intent

Comment IDs are cached before the article is destroyed because ActiveRecord's `dependent: :nullify` association option severs the link between comments and the article at destroy time. Capturing the IDs in advance allows notification cleanup to proceed even though the association is no longer intact after the call to `destroy!`.

## Scenarios

### Author visits delete confirmation page

1. Author navigates to `/:username/:slug/delete_confirm` for one of their articles.
2. Policy (`delete_confirm?`, aliased to `destroy?`) confirms the requester is the article's author, an org admin of the article's org, or a site admin.
3. The confirmation page renders with the article title, a danger-styled "Delete" button, and alternative actions to edit or unpublish instead of deleting.

### Author confirms deletion

1. Author submits the delete form on the confirmation page (`DELETE /articles/:id`).
2. Policy (`destroy?`) re-authorises the request.
3. `Articles::Destroyer` caches all comment IDs, then permanently destroys the article record.
4. All notifications associated with the article are removed; if the article had comments, their notifications are removed too.
5. The author is redirected to `/dashboard` with a success notice.

### Deletion with comments triggers comment notification cleanup

1. The article being deleted has one or more comments.
2. `Articles::Destroyer` records the comment IDs before destroying the article.
3. After destroying the article, the service enqueues removal of article notifications and then enqueues removal of all comment notifications using the cached IDs.

### Unauthorised user attempts deletion

1. A signed-in user who is neither the article's author nor an admin tries to reach the confirmation page or submit the delete request.
2. The `ArticlePolicy` raises `Pundit::NotAuthorizedError`.
3. The article is not deleted.

### Article not found on confirmation page

1. A request is made to the `delete_confirm` path with a slug that does not match any article.
2. The controller calls `not_found`, raising `ActiveRecord::RecordNotFound`.

## Failures / Exceptions

- If the article cannot be found by slug, the controller raises `ActiveRecord::RecordNotFound` (404).
- If the requester is not the author, an org admin, or a site admin, Pundit raises `NotAuthorizedError` (403).
- `destroy!` (bang variant) will raise `ActiveRecord::RecordNotDestroyed` if the destroy is blocked by a callback; this is not explicitly rescued in the destroyer service.
