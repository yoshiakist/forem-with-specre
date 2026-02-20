---
id: "01KHYCHBSG5WKRXGVJ81HAFC7F"
name: "user_browses_and_edits_tags"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/tags_controller.rb
- app/views/tags/index.html.erb (Template)
- app/views/tags/edit.html.erb (Template)
- app/views/tags/_liquid.html.erb (Template)
- spec/requests/tags_spec.rb (Test)
- spec/system/tags/user_updates_a_tag_spec.rb (Test)

## Functional Overview

`TagsController` serves the public-facing tag browsing and editing interface. Any visitor can browse and search tags via the index page. Tag moderators and admins can edit tag metadata (colors, summaries, markdown content) through a Pundit-authorized edit form. The controller also provides JSON endpoints for bulk tag lookups and tag suggestions.

## Scenarios

### Visitor browses the tag index

1. The tag index page lists direct (non-aliased) tags from the current subforem, ordered by hotness score descending, limited to 100.
2. Aliased tags are excluded from the listing.
3. When a search query parameter `q` is present, tags are filtered by name using prefix-based text search, and the heading reflects the search term.
4. When no results match the query, an empty-state message is displayed.

### Client fetches tags in bulk

1. A GET request to the bulk endpoint accepts `tag_ids` and/or `tag_names` as array parameters.
2. When `tag_ids` are provided, only tags matching those IDs are returned.
3. When `tag_names` are provided, only tags matching those names are returned.
4. Results are paginated (default 10, max 1000 per page), ordered by taggings count descending.
5. The response is JSON with serialized tag attributes including badge image.

### Client fetches tag suggestions

1. A GET request to the suggest endpoint returns up to 100 tags from the current subforem, ordered by hotness score descending.
2. The response is JSON including name, rules HTML, short summary, background color, and badge image.

### Tag moderator edits a tag

1. Only authenticated users with the `tag_moderator` role scoped to the specific tag, or super admins, can access the edit page.
2. Unauthenticated users are redirected to the login page.
3. Users without the tag moderator role receive a 404 response.
4. A tag moderator for one tag cannot edit a different tag.
5. The editable fields are: wiki body markdown, rules markdown, short summary, pretty name, background color hex, and text color hex.
6. Empty color strings are converted to nil before saving.
7. On successful update, the user is redirected back to the edit page with a success message.
8. On validation failure, the edit form is re-rendered with error messages.
