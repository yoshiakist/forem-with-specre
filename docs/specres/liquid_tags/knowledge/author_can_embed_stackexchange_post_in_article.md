---
id: "01KJ1NWDWHPM44X5SD64WS49KM"
name: "author_can_embed_stackexchange_post_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/stackexchange_tag.rb`
- `app/views/liquids/_stackexchange.html.erb` (Template)
- `spec/liquid_tags/stackexchange_tag_spec.rb` (Test)

## Functional Overview

The `{% stackoverflow %}` and `{% stackexchange %}` Liquid tags allow authors to embed Stack Exchange questions and answers in articles. The tag performs a two-phase API lookup: first it calls the StackExchange `/posts/{id}` endpoint to determine the post type (question or answer), then fetches the full post details from the type-specific endpoint (`/questions/{id}` or `/answers/{id}`) with body HTML included. The tag supports both Stack Overflow (default site) and any Stack Exchange network site via a subdomain parameter. It is registered with `UnifiedEmbed` for automatic URL detection.

## Design Intent

Stack Exchange's API requires knowing the post type before fetching detailed data (questions and answers have different response shapes and filter codes). The two-phase approach first queries the generic `/posts` endpoint to learn the type, then fetches the type-specific data with the appropriate filter. The `FILTERS` hash maps post types to Stack Exchange API filter codes that control which fields are returned.

## Key Members

- `REGISTRY_REGEXP` — matches `stackoverflow.com` and `*.stackexchange.com` question/answer URLs
- `parse_site` — determines the target site: defaults to `"stackoverflow"` for the `{% stackoverflow %}` tag or SO URLs; extracts subdomain for `{% stackexchange %}` tag
- `get_data` — two-phase API call: first `/posts/{id}` to get post type, then type-specific endpoint for full data
- `FILTERS` — hash mapping `"post"`, `"answer"`, `"question"`, and `"site"` to SE API filter codes
- `handle_response_error` — raises on API failure or empty results (deleted/not-found posts)

## Scenarios

### Embedding a Stack Overflow question

1. Author writes `{% stackoverflow 57496168 %}` in article body
2. System defaults site to `"stackoverflow"` (based on tag name)
3. API call to `/posts/57496168` returns `post_type: "question"`
4. Second API call to `/questions/57496168` fetches title, body, score, answer count
5. Rendered card shows the question title, body excerpt, score, and link

### Embedding a Stack Exchange answer

1. Author writes `{% stackexchange 1163633 askubuntu %}`
2. System extracts site `"askubuntu"` from the subdomain parameter
3. API calls fetch the answer data from the Ask Ubuntu site
4. Rendered card shows the answer body, score, and link to the original answer

### Automatic detection via URL

1. Author pastes `https://stackoverflow.com/questions/57496168/my-question`
2. `UnifiedEmbed` matches `REGISTRY_REGEXP` and routes to `StackexchangeTag`
3. System extracts the post ID and site from the URL

## Failures / Exceptions

- Invalid or non-numeric IDs raise `StandardError` with an i18n invalid-id message
- Missing site subdomain for `{% stackexchange %}` raises `StandardError` with an i18n invalid-site message
- Deleted or non-existent posts (empty API response) raise `StandardError` with "find a post with that ID"
- API HTTP errors raise `StandardError` with the API error message
