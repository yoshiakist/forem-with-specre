---
id: "01KJ1FNZWK2F8ZEV0MZ52DK4T6"
name: "author_can_embed_reddit_post_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/reddit_tag.rb`
- `app/views/liquids/_reddit.html.erb` (Template)
- `spec/liquid_tags/reddit_tag_spec.rb` (Test)

## Functional Overview

An article author can embed a Reddit post into their article body by using the `{% reddit %}` Liquid tag with a valid Reddit post URL as the argument. The tag fetches post metadata from Reddit's JSON API, then renders it through a partial template that displays the post title, author, creation date, and either a thumbnail image (for image posts) or sanitized markdown body text (for text posts), along with a link back to the original post.

## Design Intent

Reddit's public JSON API returns data as an array where the first element contains the post and the second contains comments. The tag reads only the post element, extracting the fields needed for the embed. Reddit blocks requests without a proper `User-Agent`, so the tag identifies itself using the community name and site URL from application settings. Markdown body text is rendered via Redcarpet and truncated to 60 words to keep the embed concise. Input sanitization via `strip_tags` and `Addressable::URI` prevents script injection from malicious tag arguments. The tag is also registered with `UnifiedEmbed` so that bare Reddit URLs pasted into articles are handled automatically.

## Key Members

- `REGISTRY_REGEXP` — matches any URL beginning with `https://reddit.com` or `https://www.reddit.com`; used for URL validation and `UnifiedEmbed` registration
- `@url` — the sanitized Reddit post URL supplied by the author
- `@reddit_content` — hash of post data fetched from the Reddit API, including `:author`, `:title`, `:post_url`, `:created_at`, `:post_hint`, `:image_url`, `:thumbnail`, `:selftext`, and `:selftext_html`

## Scenarios

### Embed an image post

1. Author writes `{% reddit https://www.reddit.com/r/aww/comments/... %}` in the article body.
2. On initialization, the tag strips HTML tags from the URL and validates it against `REGISTRY_REGEXP` to confirm it is a Reddit URL with a recognized scheme.
3. The tag calls the Reddit JSON API endpoint (`<url>.json`) with a `User-Agent` header containing the community name and site URL, and reads the first post element from the response array.
4. `post_hint` is `"image"`, so the thumbnail URL and image URL are stored alongside the title, author, and formatted creation date.
5. The `_reddit` partial renders a card showing the Reddit logo, post title as a link, creation date, author name, and the thumbnail image.
6. A "See on Reddit" button links back to the original post in a new tab.

### Embed a text (self) post

1. Author writes `{% reddit https://www.reddit.com/r/IAmA/comments/... %}` in the article body.
2. Initialization, URL validation, and API fetch proceed identically to the image post scenario.
3. `post_hint` is `"self"`, so the tag renders the `selftext` field: the markdown body is converted to HTML via Redcarpet, truncated to 60 words, and sanitized.
4. The `_reddit` partial renders the card header as above, but the body shows the truncated text content instead of an image.

### Invalid URL is rejected

1. Author provides a string that is not a valid Reddit URL (e.g., a URL from another domain, or malformed input).
2. `validate_url` checks both `valid_url?` (scheme must be `http` or `https`) and that the URL matches `REGISTRY_REGEXP` from position zero.
3. If either check fails, a `StandardError` is raised with a localized message identifying the invalid URL, and the article fails to parse.

## Failures / Exceptions

- Any URL that does not match `REGISTRY_REGEXP` or lacks an `http`/`https` scheme raises `StandardError` at initialization time, before any HTTP call is made.
- Reddit's API requires a custom `User-Agent` header; omitting it would result in 429 (Too Many Requests) errors. The tag always supplies this header using community settings.
- If the API response structure is unexpected (e.g., missing keys), a `NoMethodError` or `KeyError` will propagate uncaught, causing the article render to fail.
- Markdown body text is truncated to 60 words and sanitized by `HTML_Truncator` and `sanitize` to prevent excessively long or unsafe HTML from appearing in the embed.
