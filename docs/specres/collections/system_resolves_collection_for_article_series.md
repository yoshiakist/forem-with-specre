---
id: "01KJ6C4VF5JP25A07CJA19PQHX"
name: "system_resolves_collection_for_article_series"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/collection.rb`
- `spec/models/collection_spec.rb` (Test)
- `spec/factories/collections.rb` (Test)

## Functional Overview

The `Collection` model represents an article series and provides the `find_series` class method to look up or create a collection by slug in a given scope. For personal collections, the lookup is scoped to a specific user with no organization. For organization collections, the lookup is scoped solely to the organization, so the same collection is reused regardless of which user triggers the request. Slug uniqueness is validated within the appropriate scope: per-user for personal collections and per-organization for organization collections. When a touching event is received, the collection cascades the touch to all associated articles. A `non_empty` scope filters out collections that have no articles.

## Design Intent

The organization-vs-personal distinction in `find_series` reflects how series ownership works in Forem. A personal series belongs exclusively to one user, so two users can have series with the same slug independently. An organization series is shared across the organization, so it should be reused regardless of which member triggers its creation. Scoping the lookup by `organization_id` only (ignoring `user_id`) ensures that the same canonical collection is returned to every member.

The `ActiveRecord::RecordNotUnique` rescue inside the organization branch guards against a race condition: if two requests concurrently attempt to create the same organization series, the second one will hit a unique constraint violation and gracefully fall back to fetching the already-created record.

## Key Members

- `find_series(slug, user, organization: nil)` — class method that returns an existing collection matching the slug in the appropriate scope, or creates a new one if none exists.
- `slug_uniqueness_within_scope` — custom validation that enforces slug uniqueness either within a user's personal collections or within an organization's collections, depending on whether `organization_id` is present.
- `touch_articles` — private after-touch callback that propagates a touch to all articles belonging to the collection, keeping their `updated_at` timestamps current.
- `non_empty` scope — filters collections to only those that have at least one associated article.
- `path` — returns the URL path for the collection as `/<username>/series/<id>`.

## Scenarios

### Resolving a personal series

1. A request provides a slug and a user with no organization.
2. The system searches for a collection matching both the slug and the user with no organization set.
3. If a matching collection exists, it is returned without creating a new record.
4. If no match is found, a new collection is created for that user and slug, then returned.

### Resolving an organization series (reuse across users)

1. A request provides a slug, a user, and an organization.
2. The system searches for a collection matching the slug and the organization, ignoring which user is making the request.
3. If a matching collection exists, it is returned regardless of whether the requesting user originally created it.
4. If no match is found, a new collection is created with the provided user and organization, then returned.

### Handling a race condition when creating an organization series

1. Two concurrent requests both attempt to create a new organization series with the same slug.
2. One request succeeds and inserts the record; the other triggers a unique constraint violation.
3. The system rescues the `ActiveRecord::RecordNotUnique` error and re-fetches the collection that the first request created.
4. Both requests ultimately return the same canonical collection.

### Enforcing slug uniqueness within scope

1. A user attempts to save a collection whose slug already exists within their personal scope (same user, no organization) or within the same organization.
2. The custom validation detects the conflict by querying the relevant scope, excluding the current record if it is already persisted.
3. An error is added to the slug field, and the record is not saved.
4. The same slug is permitted if it belongs to a different user (for personal collections) or a different organization.

### Cascading touch to articles after collection is touched

1. An external event touches the collection record (e.g., an article is published or updated within the series).
2. The after-touch callback fires and calls `touch_all` on the collection's articles.
3. All associated articles receive an updated `updated_at` timestamp reflecting the current time.

## Failures / Exceptions

- **Slug already taken (personal):** When a personal collection's slug duplicates another collection owned by the same user, validation fails with the error "has already been taken" on the `slug` attribute.
- **Slug already taken (organization):** When an organization collection's slug duplicates another collection in the same organization, validation fails with "has already been taken for this organization" on the `slug` attribute.
- **Race condition on organization series creation:** If two processes simultaneously try to create the same organization collection, the second insert raises `ActiveRecord::RecordNotUnique`; the rescue block re-fetches the existing record instead of propagating the error.
- **Missing slug:** A collection without a slug fails the presence validation and cannot be saved.
