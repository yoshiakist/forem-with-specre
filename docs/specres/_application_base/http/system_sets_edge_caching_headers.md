---
id: "01KJXS23EC325QAKXA39K1FE6R"
name: "system_sets_edge_caching_headers"
status: "draft"
---

## Related Files

- `app/controllers/concerns/caching_headers.rb`
- `app/controllers/concerns/edge_cache_safety_check.rb`

## Functional Overview

The `CachingHeaders` concern provides helper methods that controllers include to configure HTTP caching headers for edge caches such as Fastly and Nginx. When a controller action calls `set_cache_control_headers`, the system skips cookie session tracking and sets `Cache-Control`, `X-Accel-Expires`, and `Surrogate-Control` headers so that the response can be served from the edge cache. The `Surrogate-Control` value is constructed from a configurable max-age (defaulting to the `EDGE_CACHE_DURATION_IN_HOURS` environment variable, or 24 hours), plus optional stale-while-revalidate and stale-if-error directives. The companion `EdgeCacheSafetyCheck` concern monkey-patches `current_user` so that any attempt to access the current authenticated user inside an edge-cached code path is intercepted, preventing a cache leak where a user's session data could be served to other visitors.

## Design Intent

Edge caching is restricted to public Forems only. If the Forem is not configured as public, `set_cache_control_headers` returns immediately without setting any headers. This prevents private or member-only communities from accidentally caching authenticated content at the edge. The `RequestStore` flag `edge_caching_in_place` acts as a request-scoped signal that `EdgeCacheSafetyCheck` reads to enforce the `current_user` guard at runtime rather than relying solely on developer discipline.

## Key Members

- `max_age` — Duration in seconds the response may be cached at the edge; defaults to `EDGE_CACHE_DURATION_IN_HOURS` setting converted to seconds (fallback: 24 hours).
- `stale_if_error` — Number of seconds a stale cached response may be served when the origin returns an error; defaults to 26,400 seconds.
- `stale_while_revalidate` — Optional number of seconds during which a stale response may be served while the cache revalidates in the background.
- `RequestStore.store[:edge_caching_in_place]` — Request-scoped boolean flag set to `true` when edge caching headers are active; read by `EdgeCacheSafetyCheck` to intercept `current_user` calls.

## Scenarios

### System applies edge caching headers for a public Forem

1. The Forem is configured as public (`Settings::UserExperience.public` is truthy).
2. A controller action calls `set_cache_control_headers` with default or custom arguments.
3. The system disables cookie sessions for the request.
4. The system sets the `edge_caching_in_place` flag in the request store.
5. The system writes `Cache-Control: public, no-cache`, `X-Accel-Expires` (the max-age in seconds), and a `Surrogate-Control` header encoding max-age plus stale directives to the response.

### System skips caching headers for a non-public Forem

1. The Forem is not configured as public.
2. A controller action calls `set_cache_control_headers`.
3. The system returns immediately without modifying any response headers or session options.

### System removes edge caching headers

1. A controller action calls `unset_cache_control_headers` (e.g., when switching to a private or personalised response).
2. The system clears the `edge_caching_in_place` flag and removes `Cache-Control`, `X-Accel-Expires`, and `Surrogate-Control` headers from the response.

### System tags a response with surrogate keys for targeted cache purging

1. A controller action calls `set_surrogate_key_header` with one or more key strings.
2. The system disables cookie sessions and writes a `Surrogate-Key` header containing the space-joined keys, enabling the CDN to purge specific cached responses by key.

### System intercepts current_user access inside an edge-cached code path

1. A controller action activates edge caching (the `edge_caching_in_place` flag is `true`).
2. Application code calls `current_user` within that request.
3. If no session user ID is present, `EdgeCacheSafetyCheck` returns `nil`, preventing any user-specific data from leaking.
4. If a session user ID is present, the system logs a warning message and returns the `CANNOT_USE_CURRENT_USER` sentinel string instead of the actual user record, signalling a programming error.

## Failures / Exceptions

- If `current_user` is called while `edge_caching_in_place` is `true` and a session user ID exists, the system does not raise an exception but returns a sentinel string and logs a console warning. This is an intentional soft guard to catch accidental misuse without hard-crashing the response.
