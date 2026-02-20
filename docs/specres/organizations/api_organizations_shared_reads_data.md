---
id: "01KHYAR0M26F2KE6CFGA3390RE"
name: "api_organizations_shared_reads_data"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- spec/requests/api/v0/organizations_spec.rb (Test)

## Functional Overview

The Api::OrganizationsController concern provides shared read-only API endpoints for organization data, included by both API v0 and v1 controllers. It supports showing organization profile details, listing active members, retrieving published listings (with optional category filter), and fetching published articles — all with pagination and configurable per-page limits.

## Scenarios

### API returns organization profile by username

1. The caller requests an organization by username (id_or_slug parameter).
2. The system returns selected profile attributes: id, username, name, summary, social links, URL, location, created_at, profile_image, tech_stack, tag_line, story.

### API returns paginated organization members

1. The caller requests members with optional page and per_page parameters.
2. The system returns active users joined with profiles, with selected attributes.
3. The per_page is capped at the API_PER_PAGE_MAX configuration value.

### API returns paginated organization listings

1. The caller requests listings with optional category filter and pagination.
2. The system returns published listings ordered by bumped_at descending, including user, taggings, and listing_category.

### API returns paginated organization articles

1. The caller requests articles with optional pagination.
2. The system returns published articles from the current subforem, ordered by published_at descending, decorated for presentation.

### Concern resolves organization by ID or username

1. The `find_organization` before_action looks up the organization by id first, then by username.
2. If neither matches, the system raises `ActiveRecord::RecordNotFound`.
