---
id: "01KJBWND9NFMH316PP8N7MXRRS"
name: "system_caches_article_author_entity"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/models/articles/cached_entity.rb`
- `spec/models/articles/cached_entity_spec.rb` (Test)
- `spec/lib/data_update_scripts/update_articles_cached_entities_spec.rb` (Test)

## Functional Overview

The system represents a cached snapshot of an article's author — either a user or an organization — as a unified value object called `Articles::CachedEntity`. This struct captures the attributes needed to display the author on an article (name, username, slug, profile images, and subscriber status) without querying the author table at render time. A factory method, `from_object`, normalises the differences between users and organizations (notably, organizations carry a `slug` while users do not), so callers always receive the same structure regardless of the author type. The entity also includes profile-image URL helpers via the `Images::Profile` module.

## Design Intent

Users and organizations are both valid article authors but expose slightly different interfaces. By normalising them into a single struct at cache time, article rendering code is decoupled from author type and avoids runtime polymorphism. Using a named `Struct` rather than `OpenStruct` provides a stable, serializable shape that survives schema migrations and gives type-level clarity when deserialising cached data.

## Key Members

- `name` — display name of the user or organization
- `username` — login handle of the user or organization
- `slug` — URL segment; falls back to `username` when the author object does not have a dedicated slug (i.e., users)
- `profile_image_90` — URL of the 90 px profile image variant
- `profile_image_url` — URL of the full-size profile image
- `cached_base_subscriber?` — boolean flag indicating whether the author holds a base-level subscription

## Scenarios

### Building a cached entity from a user

1. The system calls `Articles::CachedEntity.from_object` with a user object.
2. The system reads the user's name, username, profile image URLs, and subscriber status.
3. Because users do not have a dedicated slug, the system uses the user's username as the slug.
4. The system returns a `CachedEntity` struct with all fields populated and profile-image URL helpers available.

### Building a cached entity from an organization

1. The system calls `Articles::CachedEntity.from_object` with an organization object.
2. The system reads the organization's name, username, slug, profile image URLs, and subscriber status.
3. Because organizations respond to `slug`, the system uses that slug directly.
4. The system returns a `CachedEntity` struct with all fields populated and profile-image URL helpers available.

### Migrating existing cached author data from OpenStruct to CachedEntity

1. An article's `cached_user` or `cached_organization` column holds a serialized `OpenStruct` from a previous implementation.
2. The data update script reads each affected article.
3. The script rebuilds the cached value by calling `from_object` on the corresponding author record, producing an `Articles::CachedEntity`.
4. The script persists the new struct, replacing the `OpenStruct` in the column.
5. Subsequent reads of the article return an `Articles::CachedEntity` instance rather than an `OpenStruct`.
