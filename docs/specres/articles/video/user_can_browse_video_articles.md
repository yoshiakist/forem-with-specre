---
id: "01KJBWV962FQYVV8TD7XMHWN5Q"
name: "user_can_browse_video_articles"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/videos_controller.rb`
- `app/controllers/api/v0/videos_controller.rb`
- `app/controllers/api/v1/videos_controller.rb`
- `app/controllers/concerns/api/videos_controller.rb`
- `app/javascript/articles/components/Video.jsx`
- `app/javascript/utilities/videoPlayback.js`
- `app/javascript/utilities/gifVideo.js`
- `app/views/videos/index.html.erb` (Template)
- `app/views/articles/_video_player.html.erb` (Template)
- `spec/requests/videos_spec.rb` (Test)
- `spec/requests/api/v0/videos_spec.rb` (Test)
- `spec/requests/api/v1/videos_spec.rb` (Test)
- `spec/requests/api/v1/docs/videos_spec.rb` (Test)
- `spec/requests/articles/video_player_show_spec.rb` (Test)
- `spec/system/videos/user_visits_videos_spec.rb` (Test)

## Functional Overview

Users can browse a paginated listing of published video articles sorted by descending hotness score, accessible via the web UI at `/videos` and via the REST API at `/api/videos` (both v0 and v1). The listing can be filtered by tag. Each article in the listing exposes a thumbnail with a duration overlay for native videos, or an embedded iframe for YouTube, Mux, and Twitch sources. Individual video articles are also viewable on their own show page, which renders a JWPlayer-based player partial with VideoObject structured data for SEO. The API response includes fields such as `path`, `video`, `video_duration_in_minutes`, `video_source_url`, `cloudinary_video_url`, and the author's user information.

## Design Intent

The web and API controllers share the same query logic through the `Api::VideosController` concern, ensuring consistent filtering and ordering. Edge caching is applied via surrogate key headers (`videos`, `articles`, and per-record keys) so that CDN invalidation can target this endpoint precisely. The `Video` component validates embed URLs by parsing them and checking the host and path pattern rather than relying on simple string matching, limiting accepted iframe sources to known trusted providers (YouTube, Mux, Twitch).

## Key Members

- `INDEX_ATTRIBUTES_FOR_SERIALIZATION` — the fixed set of article columns selected by the API to minimize query payload: `id`, `video`, `path`, `title`, `video_thumbnail_url`, `user_id`, `video_duration_in_seconds`, `video_source_url`
- `per_page` / `API_PER_PAGE_MAX` — the requested page size is capped by the `API_PER_PAGE_MAX` environment variable (default 1000); default page size is 24
- `hotness_score` — primary sort key for ordering video articles in the listing

## Scenarios

### Browsing the video listing page

1. A visitor navigates to `/videos`.
2. The system fetches published articles that have a video, ordered by descending hotness score, limited to 24 per page.
3. The page renders the list of video articles; only articles with a video field are shown.

### Filtering video articles by tag

1. A visitor navigates to `/t/:tag/videos`.
2. The system applies a tag filter on top of the standard video query.
3. Only video articles tagged with the specified tag appear; others are excluded.

### Retrieving video articles via the API

1. A client sends `GET /api/videos` (with an optional `page` and `per_page` parameter).
2. The system returns a JSON array of published video articles ordered by descending hotness score.
3. Each item includes `type_of`, `id`, `path`, `cloudinary_video_url`, `title`, `user_id`, `video`, `video_duration_in_minutes`, `video_source_url`, and a nested `user` object.
4. The response includes surrogate key headers for CDN cache management.

### Pagination and per-page limiting via the API

1. A client requests a specific page with `page` and `per_page` query parameters.
2. The system returns only the requested slice of results.
3. If `per_page` exceeds the server's `API_PER_PAGE_MAX` limit, the server caps the result count to that maximum.

### Viewing an individual video article

1. A visitor navigates to the article's URL path.
2. The system renders the article show page including the video player partial.
3. The page includes the article title, description, author username, publication date, and the video source URL embedded in the player.

## Failures / Exceptions

- Articles with a hotness score below the threshold (e.g., score of -4) are excluded from the API listing.
- Non-iframe video sources render as a thumbnail link with duration overlay instead of an embedded player.
- Unrecognized or invalid embed URLs (those that do not match YouTube, Mux, or Twitch patterns) fall back to the thumbnail-link rendering path.
