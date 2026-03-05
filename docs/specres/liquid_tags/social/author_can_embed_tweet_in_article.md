---
id: "01KJ1FNWVTW45KZ4WKNQ6ATE2V"
name: "author_can_embed_tweet_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/tweet_tag.rb`
- `app/views/liquids/_tweet.html.erb` (Template)
- `spec/liquid_tags/tweet_tag_spec.rb` (Test)

## Functional Overview

An article author can embed a tweet by writing a `{% tweet <id_or_url> %}` (or `{% twitter ... %}`) Liquid tag anywhere in the article body. The tag accepts either a bare numeric tweet ID or a full Twitter/X URL. It renders an iframe pointing to the Twitter embed platform, with inline JavaScript that detects the user's dark-theme preference and adjusts the iframe's dimensions in response to resize messages from the embedded widget.

## Design Intent

Using an iframe-based embed from `platform.twitter.com` avoids loading the full Twitter widget.js library on every page. Accepting both a raw numeric ID and a full URL (covering both `twitter.com` and `x.com` hostnames) maximises compatibility as the platform migrated its domain. The iframe approach also makes dark-theme support straightforward: a small inline script rewrites the `src` attribute before the iframe loads when a dark theme is detected on the host page.

## Key Members

- `REGISTRY_REGEXP` — matches full `twitter.com` or `x.com` status URLs and captures the numeric tweet ID
- `VALID_ID_REGEXP` — matches a bare 10–20 digit numeric ID
- `REGEXP_OPTIONS` — ordered list of patterns tried during parsing; URL match is attempted first
- `SCRIPT` — frozen JavaScript string injected into pages; handles iframe resize messages from `platform.twitter.com` and legacy video-preview click behaviour
- `@id` — the resolved numeric tweet ID stored on the tag instance after parsing

## Scenarios

### Embedding a tweet by numeric ID

1. Author writes `{% tweet 1671839966572290048 %}` in an article body.
2. The tag is parsed; the ID is matched by `VALID_ID_REGEXP` and stored.
3. The `_tweet.html.erb` partial renders an `<iframe>` whose `src` points to `https://platform.twitter.com/embed/Tweet.html?id=<numeric_id>`.
4. Inline JavaScript checks whether the page body carries the `dark-theme` class and, if so, rewrites the iframe `src` to append `&theme=dark`.
5. The rendered HTML is returned and appears inline in the article.

### Embedding a tweet by full Twitter/X URL

1. Author writes `{% tweet https://twitter.com/username/status/1671839966572290048 %}` (or an `x.com` equivalent URL).
2. The tag is parsed; the URL is matched by `REGISTRY_REGEXP` and the numeric ID is extracted.
3. Rendering proceeds identically to the numeric-ID scenario above.

### UnifiedEmbed auto-detection

1. An author pastes a bare `twitter.com` or `x.com` status URL on its own line without an explicit Liquid tag.
2. The `UnifiedEmbed` registry matches the URL against `TweetTag::REGISTRY_REGEXP`.
3. `TweetTag` is instantiated automatically and renders the tweet embed as above.

### Dark-theme rendering

1. The article page is loaded with the dark theme active (the `<body>` element has the class `dark-theme`).
2. After the iframe element is created, the inline script detects the class and updates the iframe `src` to include `&theme=dark`.
3. The embedded tweet is displayed in dark mode.

## Failures / Exceptions

- If the input is neither a valid numeric ID nor a recognised Twitter/X status URL, `parse_id_or_url` raises a `StandardError` with the localised message `liquid_tags.tweet_tag.invalid_twitter_id`.
- HTML entities in the raw Liquid tag input (e.g., `&amp;`) are unescaped before parsing so that rich-text editors that encode the URL do not cause a false rejection.
