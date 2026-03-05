---
id: "01KHZ25T4PNZ33CT917WZ25JYT"
name: "user_can_search_users"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/search_controller.rb`
- `app/services/search/user.rb`
- `app/serializers/search/user_serializer.rb`
- `app/serializers/search/simple_user_serializer.rb`
- `spec/services/search/user_spec.rb` (Test)
- `spec/serializers/search/user_serializer_spec.rb` (Test)
- `spec/serializers/search/simple_user_serializer_spec.rb` (Test)
- `spec/system/search/display_users_search_spec.rb` (Test)
- `spec/system/search/user_searches_users_spec.rb` (Test)

## Functional Overview

Users can search for other users on the platform by selecting the "Users" filter on the search results page. The user search uses PostgreSQL full-text search against user names and usernames. Results are ranked by a custom hotness formula that combines article count, comment count, reaction count, badge achievements, and reputation modifier. Suspended and unregistered (invited-only) users are excluded from results. The search results display user profiles with contextual follow/edit buttons reflecting the current user's relationship with each result.

## Scenarios

### User searches users by name or username

1. User enters a search query and selects the "Users" content type filter
2. `SearchController#feed_content` delegates to `Search::User.search_documents` with the query term
3. Service queries registered users, applying full-text search via `.search_by_name_and_username(term)`
4. Results include user name, username, profile image, activity metrics, roles, and custom profile fields
5. Both full and partial matches against name and username are returned

### System ranks users by hotness

1. When no explicit sort is specified, results are ordered by a hotness formula
2. The formula considers `articles_count`, `comments_count`, `reactions_count`, `badge_achievements_count`, and a `reputation_modifier`
3. Users with higher combined activity and reputation appear first
4. When `sort_by: created_at` is specified, results are ordered by account creation date instead

### System excludes suspended and unregistered users

1. A user search query is executed
2. The service filters out users with a "suspended" role via `UserRole` lookup
3. As an optimization, the suspension filter is skipped entirely if no suspended users exist in the database
4. Users who are not yet registered (invitation-only accounts) are also excluded

### Search results display contextual follow buttons

1. User views search results for other users
2. For the current user's own profile, an "Edit Profile" button is shown
3. For users the current user follows, a "Following" button is shown
4. For users the current user does not follow, a "Follow" button is shown
5. For users who follow the current user but are not followed back, a "Follow Back" button is shown
