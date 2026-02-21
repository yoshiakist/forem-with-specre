---
id: "01KHZ2A12P5D6JD7A07Y0K0G87"
name: "user_can_autocomplete_usernames"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/search_controller.rb`
- `app/services/search/username.rb`
- `spec/services/search/username_spec.rb` (Test)

## Functional Overview

Users can autocomplete usernames when mentioning other users (e.g., in comments or articles). The username search endpoint returns up to 6 matching users by name or username, with context-aware ranking that prioritizes users who have previously interacted with the current article or podcast. When an article or podcast context is provided, the author, co-authors, and previous commenters are ranked higher than unrelated users. Input is sanitized to reject potentially harmful characters.

## Scenarios

### User autocompletes a username by typing

1. User begins typing a username mention (e.g., `@jo`)
2. Frontend queries `SearchController#usernames` with the partial term
3. `Search::Username.search_documents` delegates to `.search_by_name_and_username(term)` on the User model
4. Up to 6 matching users are returned with id, name, profile image, and username

### System ranks contextually relevant users higher

1. Username autocomplete is triggered within the context of a specific article or podcast episode
2. The service receives `context_type` (Article or PodcastEpisode) and `context_id` parameters
3. Users who have commented on that specific article/podcast are ranked higher
4. The article/podcast author and co-authors are also prioritized
5. Each result includes a `has_commented` boolean indicating prior engagement

### System sanitizes username search input

1. A username search request is received with the query term
2. The service rejects input containing backslash characters
3. Special characters such as quotes are handled gracefully without causing errors
