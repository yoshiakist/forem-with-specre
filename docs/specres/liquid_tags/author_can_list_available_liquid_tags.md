---
id: "01KJ1F0MZV6TAFYBWNQG6V0K2W"
name: "author_can_list_available_liquid_tags"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/liquid_tags_controller.rb`
- `spec/requests/liquid_tags_request_spec.rb` (Test)

## Functional Overview

When an authenticated user sends a GET request to `/liquid_tags`, the system collects all registered Liquid template tags, filters out internal tags whose names begin with `NullTag` or `Liquid::`, sorts the remaining names alphabetically, and returns them as a JSON array under the key `liquid_tags`. Unauthenticated requests are rejected before reaching this logic.

## Design Intent

Filtering out tags matching `NullTag` or `Liquid::` ensures that only custom, application-defined tags are exposed to authors. Internal Liquid framework tags and null-placeholder tags are not meaningful to content authors and are therefore excluded from the listing.

## Scenarios

### Authenticated user retrieves the tag list

1. An authenticated user sends `GET /liquid_tags`.
2. The system reads all registered tags from `Liquid::Template.tags`.
3. Tags whose names match the pattern `NullTag` or start with `Liquid::` are removed from the set.
4. The remaining tag names are sorted alphabetically.
5. The system responds with HTTP 200 and a JSON body of the form `{ "liquid_tags": [...] }` containing the filtered, sorted tag names.

### Unauthenticated request is rejected

1. A visitor who is not signed in sends `GET /liquid_tags`.
2. The `authenticate_user!` before-action fires before any tag data is accessed.
3. The system responds with HTTP 401 Unauthorized and no tag data is returned.

## Failures / Exceptions

- Any request without a valid authenticated session is blocked by `authenticate_user!` and receives a 401 response before the index action executes.
