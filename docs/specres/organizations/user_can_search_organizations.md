---
id: "01KJ02HC7CPXANNH4W8KJWYC61"
name: "user_can_search_organizations"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/services/search/organization.rb`
- `app/serializers/search/organization_serializer.rb`
- `spec/services/search/organization_spec.rb` (Test)
- `spec/serializers/search/organization_serializer_spec.rb` (Test)

## Functional Overview

When a user searches for organizations, the system accepts an optional text term along with pagination and sort parameters. If a term is provided, results are filtered by matching against organization names using full-text search. The result set is then sorted and paginated, and each matching organization is serialized into a lightweight document containing its id, name, summary, profile image, Twitter username, and slug. When no term is given, all organizations are returned in sorted, paginated form.

## Key Members

- `term` — optional search string matched against organization names
- `sort_by` — attribute to sort by; defaults to `name`
- `sort_direction` — direction of sort (`asc` or `desc`); defaults to `desc`
- `page` — zero-based page index; defaults to `0`
- `per_page` — number of results per page; defaults to 75, capped at 150
- `Search::OrganizationSerializer` attributes: `id`, `name`, `summary`, `profile_image`, `twitter_username`, `slug`

## Scenarios

### Search with a matching term

1. A caller invokes the search with a non-empty `term`.
2. The system filters organizations whose name matches the term via full-text search.
3. Because a search term is present and no explicit `sort_by` is provided, results are returned in the relevance order produced by the search scope (sort step is skipped).
4. Results are paginated and each organization is serialized; the list of attribute hashes is returned.

### Search with a term and explicit sort

1. A caller invokes the search with a non-empty `term` and an explicit `sort_by` value.
2. The system filters organizations by the term and then applies `reorder(sort_by => sort_direction)`.
3. The sorted, paginated results are serialized and returned.

### Browse all organizations (no term)

1. A caller invokes the search without a `term`.
2. The system returns all organizations, applying the default sort by `name` descending.
3. Results are paginated using the default page size of 75 (capped at 150) and serialized.

### Empty result set

1. A caller invokes the search with a term that matches no organization names.
2. The system returns an empty array.

## Failures / Exceptions

- `per_page` values exceeding 150 are silently clamped to `MAX_PER_PAGE` (150) to prevent excessively large queries.
- `page` is coerced to an integer and incremented by 1 before being passed to the pagination library, so non-integer or nil values are safely handled.
