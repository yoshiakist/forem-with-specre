---
id: "01KHZ26XHGBTBKDTDCRC8S5FCC"
name: "user_can_search_tags"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/search_controller.rb`
- `app/services/search/tag.rb`
- `app/serializers/search/tag_serializer.rb`
- `spec/services/search/tag_spec.rb` (Test)
- `spec/serializers/search/tag_serializer_spec.rb` (Test)

## Functional Overview

Users can search for tags on the platform either via the "Tags" filter on the search results page or through the dedicated tag search endpoint. The tag search matches against tag names and returns only supported tags, ordered by hotness score. Results include tag metadata such as name, summary, rules, badge information, and background color for visual display.

## Scenarios

### User searches tags by name

1. User enters a search query and selects the "Tags" content type filter, or the system queries `SearchController#tags`
2. Service queries supported tags via `.search_by_name(term)`, matching full and partial tag names
3. Results are ordered by `hotness_score` descending, surfacing the most popular matching tags first
4. Each result includes tag name, hotness score, short summary, rules HTML, background color, and optional badge image

### System excludes unsupported tags

1. A tag search query is executed
2. The service only returns tags where `supported` is true
3. Unsupported or deprecated tags are never included in search results

### Tag results respect pagination limits

1. User searches tags with pagination parameters
2. Default page size is 60 tags, with a maximum cap of 100
3. Results beyond the cap are not returned in a single page
