---
id: "01KJ7HR805TS43BDP921B57G4T"
name: "system_normalizes_navigation_link_urls"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/navigation_link.rb`
- `spec/models/navigation_link_spec.rb` (Test)

## Functional Overview

When a `NavigationLink` is saved, the system normalizes its URL so that local links pointing to the current forem host are stored as relative paths (e.g., `/contact`), while external URLs are stored unchanged. Before validation, if the URL is already a relative path starting with `/`, the system temporarily expands it to an absolute URL so that standard URL validators can evaluate it. Before the record is persisted, the system strips the local hostname from any absolute URL that matches the current forem base URL, reducing it back to a relative path. This normalization logic is also applied when looking up or seeding records via `create_or_update_by_identity`, ensuring that identity matching is consistent regardless of whether the caller supplies a relative or absolute local URL.

## Design Intent

Storing local navigation links as relative paths makes it possible to switch the forem between domains (e.g., from a `.forem.cloud` subdomain to a custom domain) without needing to update every stored navigation link URL.

## Scenarios

### Local absolute URL is normalized to a relative path on save

1. A navigation link is given a URL that begins with the current forem base URL (e.g., `https://testforem.com/about`).
2. Before validation, the system expands it to an absolute URL if it was already relative — no change is needed here because it is already absolute.
3. Before the record is saved, the system detects that the URL matches the local hostname and strips the host portion, storing only the path (`/about`).

### Relative URL is preserved unchanged on save

1. A navigation link is given a URL that is already a relative path starting with `/` (e.g., `/contact`).
2. Before validation, the system temporarily prepends the base URL so the URL validator accepts it.
3. Before the record is saved, the system detects the resulting absolute URL matches the local hostname and strips it back to a relative path, yielding the original value (`/contact`).

### External URL is preserved unchanged on save

1. A navigation link is given a fully-qualified external URL (e.g., `https://example.com/news`).
2. No hostname stripping occurs because the URL does not match the local forem host.
3. The URL is stored exactly as provided.

### Identity-based upsert normalizes the URL before lookup

1. A caller invokes `create_or_update_by_identity` with a URL and a name.
2. The system normalizes the supplied URL (stripping the local hostname if applicable) before querying for an existing record.
3. If a record with the normalized URL and name exists, it is updated with the supplied attributes; otherwise a new record is created.
