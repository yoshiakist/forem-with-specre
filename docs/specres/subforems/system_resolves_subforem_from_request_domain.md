---
id: "01KHYYE333JHM6PGK7AZYCHD0X"
name: "system_resolves_subforem_from_request_domain"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/lib/middlewares/set_subforem.rb
- spec/lib/middlewares/set_subforem_spec.rb (Test)

## Functional Overview

The `Middlewares::SetSubforem` Rack middleware runs on every request and resolves the current subforem context from the request domain. It extracts the domain from either a `passed_domain` query parameter or the HTTP Host header, looks up the subforem ID via `Subforem.cached_id_by_domain`, and populates `RequestStore` with the subforem ID, domain, default subforem ID, and related context. It also handles cookie isolation for subdomains and sets Content-Security-Policy headers to allow iframe embedding across all subforem domains.

## Design Intent

Using Rack middleware for subforem resolution ensures that every request — including API calls, asset requests, and page loads — has consistent subforem context available before any controller code executes. The `RequestStore` approach provides thread-safe, per-request scoping without polluting global state.

## Scenarios

### System resolves subforem from Host header

1. A request arrives with a Host header containing a known subforem domain
2. Middleware looks up the subforem ID via `Subforem.cached_id_by_domain`
3. Middleware stores the resolved `subforem_id`, `subforem_domain`, and `default_subforem_id` in `RequestStore`
4. The request proceeds to the application with full subforem context available

### System resolves subforem from passed_domain parameter

1. A request includes a `passed_domain` query parameter
2. Middleware uses this parameter instead of the Host header for domain resolution
3. The resolved subforem context is stored in `RequestStore` as usual

### System handles unknown domain

1. A request arrives with a Host header that does not match any known subforem
2. Middleware sets `subforem_id` to nil in `RequestStore`
3. The default subforem ID is still populated for fallback behavior

### System isolates cookies across subdomains

1. For requests to subdomain-based subforems, the middleware deletes the session cookie to prevent cross-subforem session leakage
2. This ensures users have separate sessions per subforem domain
