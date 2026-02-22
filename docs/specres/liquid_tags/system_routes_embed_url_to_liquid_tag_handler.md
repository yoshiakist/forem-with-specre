---
id: "01KJ1F0NVRKVVJQK0DPZYCJKMX"
name: "system_routes_embed_url_to_liquid_tag_handler"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/unified_embed.rb`
- `app/liquid_tags/unified_embed/registry.rb`
- `app/liquid_tags/unified_embed/tag.rb`
- `app/liquid_tags/forem_tag.rb`
- `app/views/liquid_embeds/show.html.erb` (Template)
- `spec/liquid_tags/unified_embed/registry_spec.rb` (Test)
- `spec/liquid_tags/unified_embed/tag_spec.rb` (Test)
- `spec/liquid_tags/forem_tag_spec.rb` (Test)

## Functional Overview

When the Liquid template engine encounters an `{% embed <url> %}` tag, `UnifiedEmbed::Tag` is instantiated. It strips and parses the input to extract the URL and detect an optional `minimal` keyword. Before selecting a handler, it validates the URL by making an outbound HTTP HEAD request — following redirects, retrying on 405 responses, and blocking requests to private or loopback IP addresses to prevent SSRF attacks. The singleton `UnifiedEmbed::Registry` is then consulted: it first checks whether the link matches a Forem article on any known subforem domain (returning `LinkTag`), then walks its list of registered handlers looking for a regexp match. `ForemTag` is one such registered handler; when it matches a platform-internal URL it performs a second level of routing to determine whether the link points to a tag, a comment, a user, an organization, a podcast episode, or a generic article, and returns the appropriate tag class. If no registered handler matches, the registry falls back to `OpenGraphTag`. When `minimal` mode is active, only `LinkTag` is permitted; all other URLs are rendered via `OpenGraphTag`. If link validation raises a network or SSL error, `FallbackTag` renders a plain link card without metadata.

## Design Intent

The registry uses the Singleton pattern so that handler registrations, which happen at file-load time via `UnifiedEmbed.register(...)`, accumulate into a single shared list without requiring explicit initialization order management. `ForemTag` is registered as a single entry point for all platform-internal URLs, keeping external-platform handlers decoupled from Forem-specific routing logic. The `minimal` mode and its allowlist (`MINIMAL_ALLOWLIST`) allow embedding contexts that must restrict third-party iframes (e.g., email digests) to opt into a safer rendering path without changing the tag syntax. SSRF protection is layered: literal hostnames are checked first, then DNS-resolved addresses are each validated against private/loopback ranges.

## Key Members

- `UnifiedEmbed::Registry` — Singleton that stores registered `{ regexp:, klass:, skip_validation: }` entries and resolves a URL to a handler class.
- `UnifiedEmbed::Tag::MINIMAL_ALLOWLIST` — Array of tag classes permitted in minimal mode; currently contains only `LinkTag`.
- `UnifiedEmbed::Tag::MAX_REDIRECTION_COUNT` — Maximum number of HTTP redirects followed during link validation (default: 3).
- `ForemTag::REGISTRY_REGEXP` — Pattern used when registering `ForemTag` with the registry; matches any path under the platform's base URL.

## Scenarios

### URL matches a registered third-party handler

1. The author writes `{% embed https://www.youtube.com/watch?v=... %}` in an article.
2. `UnifiedEmbed::Tag` strips HTML from the input and extracts the URL.
3. The registry finds no subforem-domain match but finds a regexp match for `YoutubeTag` in its handler list.
4. The URL is validated via an HTTP HEAD request; the request succeeds.
5. `YoutubeTag` is instantiated with the validated URL and renders the embed.

### URL matches a Forem-internal path via ForemTag

1. The author embeds a URL pointing to a user profile on the same platform.
2. The registry matches the URL against `ForemTag::REGISTRY_REGEXP` and returns `ForemTag` as the handler.
3. `ForemTag.new` processes the input, then `determine_klass` checks path patterns in order: tag prefix, comment segment, then user/org/podcast lookup.
4. A `User` record is found for the path segment, so `UserTag` is returned and instantiated.

### URL points to a Forem article and returns LinkTag directly from registry

1. The embedded URL matches both a known subforem domain and an existing `Article` path.
2. `Registry#find_handler_for` detects this before consulting registered handlers and returns `{ klass: LinkTag, skip_validation: false }`.
3. The URL is validated and `LinkTag` renders a rich article card.

### Minimal mode restricts embed to LinkTag or OpenGraphTag

1. The author writes `{% embed https://www.youtube.com/watch?v=... minimal %}`.
2. `UnifiedEmbed::Tag` detects the `minimal` keyword and sets minimal mode.
3. The pre-validation handler lookup finds `YoutubeTag`, but it is not in `MINIMAL_ALLOWLIST`.
4. `OpenGraphTag` is used instead, rendering a plain open-graph card.
5. If the URL had resolved to a `LinkTag` (on `MINIMAL_ALLOWLIST`), `LinkTag` would have been used directly.

### Link validation fails with a network or SSL error

1. `UnifiedEmbed::Tag` attempts to validate the URL via `validate_link`.
2. A `SocketError`, `Timeout::Error`, `Errno::ECONNREFUSED`, `Errno::EHOSTUNREACH`, or `OpenSSL::SSL::SSLError` is raised.
3. The rescue block instantiates `FallbackTag` with the original unvalidated URL.
4. `FallbackTag#render` produces a minimal link card displaying the host and path without any fetched metadata.

## Failures / Exceptions

- If the URL resolves to a private or loopback IP address, `validate_link` raises `StandardError` with a user-facing message to prevent SSRF attacks.
- If the URL returns HTTP 404, `validate_link` raises `StandardError` indicating the resource was not found.
- If the URL redirects more than `MAX_REDIRECTION_COUNT` times, `validate_link` raises `StandardError` indicating too many redirects.
- If a 405 Method Not Allowed response is received and retries are exhausted, `validate_link` raises `StandardError`.
- If `ForemTag` is invoked for a platform URL that matches no known content type (e.g., `/terms-of-service`), it raises `StandardError` indicating no liquid tag exists for that URL.
- Network and SSL errors during validation are caught and result in `FallbackTag` being rendered rather than propagating the error to the author.
