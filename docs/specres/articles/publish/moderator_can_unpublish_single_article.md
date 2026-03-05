---
id: "01KJBWZ3J5DHQXJ25C977K5D9H"
name: "moderator_can_unpublish_single_article"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/articles/unpublish.rb`
- `app/controllers/concerns/api/articles_controller.rb`
- `app/controllers/api/v1/articles_controller.rb`
- `app/views/api/v1/articles/unpublish.json.jbuilder`
- `spec/services/articles/unpublish_spec.rb` (Test)
- `spec/requests/articles/articles_admin_unpublish_spec.rb` (Test)
- `spec/requests/api/v1/articles_spec.rb` (Test)
- `spec/requests/api/v1/docs/articles_spec.rb` (Test)

## Functional Overview

A moderator (or super admin) can unpublish a single published article by invoking the `Articles::Unpublish` service. The service inspects whether the article uses YAML front-matter: if it does, the body markdown is rewritten to change `published: true` to `published: false`; if the article has no front-matter, the `published` attribute is set directly to `false`. The update is applied through `Articles::Updater`, ensuring any associated side effects (such as removing published notifications) are handled consistently.

## Design Intent

The dual-path logic (front-matter vs. attribute) preserves the canonical source of truth for each article format. For front-matter articles, the published state lives inside the markdown body, so editing the markdown keeps the body and database record in sync. For non-front-matter articles, a simple attribute update is sufficient.

## Scenarios

### Unpublish an article without front-matter

1. A moderator selects a published article that has no YAML front-matter block.
2. The system sets the article's `published` attribute to `false` and saves it via `Articles::Updater`.
3. The article is no longer publicly visible.

### Unpublish an article with front-matter

1. A moderator selects a published article whose body contains a YAML front-matter block with `published: true`.
2. The system rewrites the front-matter line to `published: false` within the body markdown.
3. The updated markdown is saved via `Articles::Updater`.
4. The article is no longer publicly visible.

### Admin unpublishes via HTTP endpoint

1. A super admin sends a PATCH request to `/articles/:id/admin_unpublish` with the article id, username, and slug.
2. The system unpublishes the article and removes any "Published" notifications associated with it.
3. The article's `published` flag is `false` after the request completes.
