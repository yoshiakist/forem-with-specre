---
id: "01KJXS2J6JX5ZKHWS3Z43QVMHP"
name: "system_validates_request_origin_and_redirect_protocol"
status: "draft"
---

## Related Files

- `app/controllers/concerns/valid_request.rb`

## Functional Overview

The `ValidRequest` concern provides two monkey-patched methods to handle known Rails request-origin and redirect-protocol inconsistencies. `valid_request_origin?` overrides Rails' built-in CSRF origin check to manually compare only the host and port of the referer header (ignoring http vs https), and to reject requests bearing a `null` origin by raising an `InvalidAuthenticityToken` error. `_compute_redirect_to_location` overrides Rails' redirect helper so that application-relative redirect paths are prefixed with the application's configured protocol (via `URL.protocol`) rather than the protocol inferred from the incoming request, ensuring redirects consistently use the correct scheme.

## Design Intent

Both methods exist as explicit workarounds for historical mismatches between the HTTP `Origin` header and Rails' `request.base_url` (e.g., `https://dev.to` vs `http://dev.to`). The origin check normalizes https/http differences so that protocol discrepancies introduced by load-balancers or proxies do not break CSRF validation. The redirect override ensures that outgoing redirects carry the canonical application protocol rather than reflecting whatever protocol the upstream proxy presented to Rails.

## Scenarios

### Referer-based origin check passes when host and port match

1. A request arrives with a `Referer` header set to a URL on the same host and port as the application.
2. The system parses the referer URI and extracts its host and port.
3. The system compares the referer host and port against the request host and port, ignoring the scheme (http vs https).
4. Because host and port match, the method returns a truthy value and the request is allowed to proceed.

### Origin header check passes when origin matches base URL (ignoring scheme)

1. A request arrives without a `Referer` header but with an `Origin` header containing a valid URL.
2. The system normalizes both the origin and `request.base_url` by replacing `https` with `http`.
3. The normalized strings match, so the method returns a truthy value and the request is allowed.

### Request with null origin is rejected

1. A request arrives with no `Referer` header and an `Origin` header value of the string `"null"`.
2. The system detects the literal `"null"` origin.
3. The system raises `ActionController::InvalidAuthenticityToken` with the application's `NULL_ORIGIN_MESSAGE` constant.

### Request with no origin and no referer is allowed

1. A request arrives with neither a `Referer` header nor an `Origin` header.
2. The system observes that `origin` is `nil`.
3. The method returns `true` (nil is treated as a permitted case), allowing the request to proceed.

### Redirect to a relative path uses the application protocol

1. A controller action calls `redirect_to` with a relative path string (not a full URL).
2. The system constructs the full redirect URL by prepending `URL.protocol` (the application's canonical protocol) and `request.host_with_port` to the path.
3. The redirect response is sent to the client using the canonical protocol regardless of the incoming request protocol.

## Failures / Exceptions

- When the `Origin` header is the literal string `"null"`, `valid_request_origin?` raises `ActionController::InvalidAuthenticityToken` to prevent potential null-origin attacks.
- In the test environment, `valid_request_origin?` returns immediately without performing any checks, bypassing CSRF origin validation entirely.
