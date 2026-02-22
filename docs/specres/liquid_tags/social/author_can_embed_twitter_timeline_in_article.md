---
id: "01KJ1FP0T67WTKGPRZS3CQY3QR"
name: "author_can_embed_twitter_timeline_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/twitter_timeline_tag.rb`
- `app/views/liquids/_twitter_timeline.html.erb`
- `spec/liquid_tags/twitter_timeline_tag_spec.rb` (Test)

## Functional Overview

When an author includes a `{% twitter_timeline <url> %}` Liquid tag in an article body, the system validates the provided URL against a strict pattern requiring the Twitter timelines URL format (`https://twitter.com/<username>/timelines/<numeric_id>`), then renders an embedded Twitter timeline widget. The rendered output is an anchor element styled as a Twitter timeline alongside a direct link button. The Twitter widgets JavaScript is registered separately via `self.script` so the host page can include it once rather than once per tag. The tag is also registered with `UnifiedEmbed` so it participates in the unified embed resolution flow.

## Design Intent

The tag delegates HTML rendering to a Rails partial rather than building strings in Ruby, keeping presentation separate from validation logic. URL validation is intentionally strict — only the exact timelines URL shape is accepted — to prevent inadvertent embedding of arbitrary Twitter URLs (e.g., individual tweet status URLs). HTML is stripped from the incoming link before validation to guard against injection through tag attributes.

## Key Members

- `URL_REGEXP` — strict regex that matches only `https://twitter.com/<alphanumeric>/timelines/<digits>`, used for validation
- `REGISTRY_REGEXP` — looser regex (no anchors) used when registering with `UnifiedEmbed` for auto-detection in article text
- `SCRIPT` — the `<script>` tag for `platform.twitter.com/widgets.js`; exposed via `self.script` so callers can inject it once per page
- `@href` — the validated timeline URL stored at initialization and passed to the partial at render time
- `PARTIAL` — path to the ERB partial (`liquids/twitter_timeline`) that produces the embed markup

## Scenarios

### Author embeds a valid Twitter timeline

1. Author writes `{% twitter_timeline https://twitter.com/ExampleUser/timelines/1234567890 %}` in an article.
2. The tag strips any HTML from the argument and trims whitespace.
3. The cleaned URL is matched against `URL_REGEXP`; it passes.
4. At render time the system renders the `_twitter_timeline` partial with the validated URL as `href`.
5. The output contains an `<a class="twitter-timeline">` anchor and a "View" link button, both pointing to the timeline URL.

### Author provides a URL with trailing whitespace

1. Author writes `{% twitter_timeline https://twitter.com/ExampleUser/timelines/1234567890   %}` (trailing spaces).
2. The tag strips HTML and trims whitespace, normalizing the URL.
3. Validation succeeds and the embed renders correctly.

### Page includes the Twitter widgets script

1. The host page calls `TwitterTimelineTag.script`.
2. The system returns the `<script async src="https://platform.twitter.com/widgets.js">` tag as a string.
3. The page injects this script once to activate all timeline widgets on the page.

### UnifiedEmbed auto-detects a Twitter timeline URL

1. A Twitter timelines URL appears in article content and is processed by `UnifiedEmbed`.
2. `UnifiedEmbed` matches the URL against `REGISTRY_REGEXP`.
3. `TwitterTimelineTag` is selected as the handler and the embed is rendered.

## Failures / Exceptions

- If the URL matches a Twitter status URL (e.g., `https://twitter.com/user/status/123`) rather than a timelines URL, `valid_link?` returns false and `raise_error` raises a `StandardError` with the localized message from `liquid_tags.twitter_timeline_tag.invalid_url`.
- If the URL is from a domain other than `twitter.com`, or follows a non-timelines path structure, the same error is raised.
- Any HTML embedded in the tag argument (e.g., from a rich-text editor) is stripped before validation, preventing injection.
