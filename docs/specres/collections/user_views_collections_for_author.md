---
id: "01KJ6BZ9FHN72VNWP7JGG6DWBZ"
name: "user_views_collections_for_author"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/collections_controller.rb`
- `app/models/collection.rb`
- `app/views/collections/index.html.erb` (Template)
- `app/views/collections/_meta.html.erb` (Template)
- `spec/requests/collections_spec.rb` (Test)
- `spec/system/collections/user_views_collections_spec.rb` (Test)
- `spec/factories/collections.rb` (Test)

## Functional Overview

When a visitor navigates to an author's series page (`/:username/series`), the system looks up the author by username and retrieves all of that author's collections that contain at least one article, ordered from newest to oldest. The page renders each collection as a linked card. If no non-empty collections exist, an empty-state message is shown. Page metadata including Open Graph and Twitter Card tags is populated with a title and description derived from the author's display name.

## Design Intent

Only non-empty collections are surfaced to avoid presenting empty series to readers. The `non_empty` scope uses a SQL join to enforce this at the database level, keeping the controller simple and avoiding N+1 loading of article counts.

## Scenarios

### Author has collections with articles

1. A visitor navigates to `/:username/series` for an author who owns one or more collections that each contain at least one article.
2. The system locates the author by username, then fetches that author's non-empty collections in descending creation order.
3. The page displays each collection as a card with a link whose text includes the collection slug and the number of published articles in the series.

### Author has collections but none contain articles

1. A visitor navigates to `/:username/series` for an author whose collections all have no articles.
2. The system fetches the author's non-empty collections, which returns an empty set.
3. The page displays an empty-state message instead of any collection cards.

### Page metadata is populated

1. The page sets a title of the form "Series by [Author Name]" derived from the author's display name.
2. Open Graph and Twitter Card meta tags are rendered with that title, a descriptive summary, and the site's main social image.
3. The canonical URL is set to `/:username/series/`.

### Username does not match any user

1. A visitor navigates to `/:username/series` where the username does not exist in the system.
2. The system raises a `ActiveRecord::RecordNotFound` error (via `find_by!`), resulting in a 404 response.
