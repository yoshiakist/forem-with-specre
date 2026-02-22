---
id: "01KJ1F3QAFT0HFRPDHZ3JKZG6Z"
name: "author_can_embed_comment_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/comment_tag.rb`
- `app/views/comments/_liquid.html.erb` (Template)
- `spec/liquid_tags/comment_tag_spec.rb` (Test)

## Functional Overview

An article author can embed a specific comment inline within article body content using a `{% comment <id_or_url> %}` Liquid tag. When the tag is processed, the system looks up the comment by its alphanumeric ID code (or by extracting the ID from a full DEV comment URL) and renders a styled card showing the commenter's profile image, display name, publication date, and comment body. If the comment is not found, a "Comment Not Found" placeholder is rendered instead of raising an error. The legacy `{% devcomment %}` tag alias is also supported for backward compatibility with existing embedded comments on DEV.

## Design Intent

Accepting both a bare ID code and a full URL as input reduces friction for authors: they can paste either form directly into article Markdown. HTML-encoded input is unescaped before parsing so that the tag survives round-trips through editors that encode special characters. Rendering is delegated to a Rails partial rather than inline string construction, keeping presentation logic in the view layer and making the output testable through standard Rails rendering.

## Key Members

- `VALID_LINK_REGEXP` — matches a full DEV comment URL and captures the `comment_id` segment from the path
- `VALID_ID_REGEXP` — matches a bare alphanumeric ID code
- `@comment` — the `Comment` record resolved at initialization time; may be `nil` if no matching record is found
- `PARTIAL` — path to the view partial used for rendering (`comments/liquid`)

## Scenarios

### Embedding a comment by bare ID code

1. Author writes `{% comment <id_code> %}` in article Markdown, where `<id_code>` is the alphanumeric ID of an existing comment.
2. At parse time the tag unescapes HTML entities in the input and extracts the ID code via `VALID_ID_REGEXP`.
3. The system queries `Comment` by `id_code` and stores the result.
4. When the article is rendered, the `comments/liquid` partial is invoked with the resolved comment record.
5. The rendered output contains the commenter's name, profile image link, publication date, and comment body.

### Embedding a comment by full URL

1. Author writes `{% comment https://<host>/<username>/comment/<id_code> %}` in article Markdown.
2. At parse time the tag matches the URL against `VALID_LINK_REGEXP` and extracts the `comment_id` capture group.
3. Processing then continues identically to the bare ID code path.

### Comment not found

1. The tag is parsed with a valid-format ID code that does not match any `Comment` record.
2. `Comment.find_by` returns `nil`; `@comment` is set to `nil`.
3. The `comments/liquid` partial renders the "Comment Not Found" fallback message instead of comment content.

### Legacy devcomment tag

1. An article body contains `{% devcomment <id_code> %}`, a tag originally used on DEV before the rename.
2. The Liquid template engine resolves `devcomment` to the same `CommentTag` class.
3. Rendering proceeds identically to the standard `{% comment %}` path.

## Failures / Exceptions

- If the input does not match either accepted pattern (`VALID_LINK_REGEXP` or `VALID_ID_REGEXP`), `parse_id_code` raises a `StandardError` with the I18n message `liquid_tags.comment_tag.invalid_comment` (displayed as "Invalid Comment ID or URL"). This occurs at Liquid parse time, before the article is rendered.
