---
id: "01KJ1NAH8W61VK3XGMD2PD713M"
name: "author_can_embed_gist_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/gist_tag.rb`
- `app/views/liquids/_gist.html.erb` (Template)
- `spec/liquid_tags/gist_tag_spec.rb` (Test)

## Functional Overview

The `{% gist %}` Liquid tag allows authors to embed GitHub Gists in articles. It accepts a full `gist.github.com` URL with an optional `file=` parameter to embed a specific file from a multi-file gist. The tag converts the URL to a `.js` embed URI and renders it via a `<script>` tag. Versioned gist URLs (with a commit SHA segment) are also supported. The tag is registered with `UnifiedEmbed` for automatic URL detection.

## Design Intent

GitHub Gists are embedded client-side via their `.js` endpoint. The tag constructs this endpoint URL from the provided gist URL, appending file selection as a query parameter when specified. Strict URL validation prevents XSS via crafted URLs.

## Key Members

- `VALID_LINK_REGEXP` — validates full gist URLs including owner, gist ID, and optional version segment
- `build_uri` — splits input into link and option, parses the link, appends `.js` suffix and file option
- `build_options` — validates `file=` option format and returns it as a query string
- `valid_option?` — ensures the `file=` value does not contain backslashes (XSS prevention)

## Scenarios

### Embedding a basic Gist

1. Author writes `{% gist https://gist.github.com/user/abc123def456 %}` in article body
2. System validates the URL and converts it to `https://gist.github.com/user/abc123def456.js`
3. Rendered output is a `<script>` tag that loads the Gist inline

### Embedding a specific file from a Gist

1. Author writes `{% gist https://gist.github.com/user/abc123 file=example.rb %}`
2. System appends `?file=example.rb` to the `.js` URI
3. Only the specified file from the Gist is rendered

### Embedding a specific version

1. Author provides a gist URL with a commit SHA: `https://gist.github.com/user/abc123/def456...`
2. System includes the version segment in the `.js` URL
3. The historical version of the Gist is rendered

## Failures / Exceptions

- Blank input raises `StandardError` with an invalid-gist-link message
- URLs not matching `VALID_LINK_REGEXP` (including XSS attempts like `@evil.com` suffixes) raise `StandardError`
- Invalid `file=` values containing backslashes raise `StandardError` with invalid-filename message
