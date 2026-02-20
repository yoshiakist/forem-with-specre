---
id: "01KHYAG7500GXRZGY07Y91X18W"
name: "organization_search_returns_paginated_results"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/search/organization.rb
- app/serializers/search/organization_serializer.rb
- spec/services/search/organization_spec.rb (Test)
- spec/serializers/search/organization_serializer_spec.rb (Test)

## Functional Overview

The Search::Organization service provides paginated, searchable, and sortable organization listings for the internal search system. It delegates text matching to the `search_organizations` PgSearch scope, applies configurable sort ordering, paginates results, and serializes output via Search::OrganizationSerializer with attributes: id, name, summary, profile_image, twitter_username, slug, and class_name.

## Scenarios

### Search returns paginated organization results

1. The caller invokes `Search::Organization.search_documents` with optional term, sort_by, sort_direction, page, and per_page parameters.
2. The system applies the PgSearch `search_organizations` scope when a term is provided.
3. The system paginates results with a default of 75 per page and a maximum of 150 per page.
4. The system serializes results using `Search::OrganizationSerializer`, returning an array of attribute hashes.

### Search applies configurable sorting

1. By default, results are sorted by name in descending order.
2. If a term is provided but sort_by is blank, the system preserves the PgSearch relevance ordering.
3. If sort_direction is provided, the system reorders by the specified column and direction.

### Serializer formats organization for search results

1. The serializer outputs id, name, summary, profile_image, twitter_username, slug, and a fixed `class_name` of "Organization".
