---
id: "01KJ9JHJXSYEDB3WWBQGZKPQCF"
name: "system_includes_users_in_sitemap"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/sitemaps_controller.rb` (Shared)
- `app/views/sitemaps/users.xml.erb` (Template)
- `spec/requests/sitemaps_spec.rb` (Shared, Test)

## Functional Overview

When a request is made to a users sitemap URL, the system renders a paginated XML sitemap of user profile pages. Users are ordered by comment count descending to surface the most active profiles first, and any user with a score of -1 or lower is excluded as a spam mitigation measure. Each page holds up to `RESULTS_LIMIT` users (10,000 in production, 5 in other environments). The page offset is derived from a numeric segment in the URL path; if that segment is absent or non-numeric it evaluates to zero, rendering the first page. The resulting XML lists each user's profile URL and the date their profile was last updated.

## Design Intent

Ordering by `comments_count DESC` prioritises high-engagement users near the top of the sitemap so search crawlers index the most valuable profiles first. The `score > -1` filter is a lightweight server-side spam gate that keeps spammer profiles out of the sitemap without requiring a separate blocklist. Deriving the offset from the URL slug (e.g., `/sitemap-users-1.xml`) keeps sitemap pagination stateless and crawlable without query parameters.

## Key Members

- `RESULTS_LIMIT` — Maximum users per sitemap page (10,000 in production, 5 in other environments).
- `@users` — Array of `[username, profile_updated_at]` tuples passed to the template; populated by ordering on `comments_count DESC` with the spam score filter and the computed offset applied.
- `offset` — Page offset calculated from the numeric segment of the sitemap URL slug; defaults to zero when the segment is absent or non-numeric.

## Scenarios

### First page of users sitemap

1. A crawler requests `/sitemap-users.xml`.
2. The system identifies `users` as a valid resource sitemap target.
3. Users with a score greater than -1 are fetched, ordered by comment count descending, limited to one page of results starting at offset zero.
4. The response is an XML document listing each user's profile URL and last-modified date, with the highest-comment-count user appearing first.

### Subsequent page of users sitemap

1. A crawler requests `/sitemap-users-1.xml` (where `1` is the page index).
2. The system parses the numeric segment `1` from the URL and multiplies it by `RESULTS_LIMIT` to compute the row offset.
3. Users are fetched with the same ordering and filter but starting from that offset.
4. The response lists the users on that page; users from the first page do not appear.

### Non-numeric or absent offset segment treated as first page

1. A crawler requests a URL whose slug suffix is non-numeric (e.g., `/sitemap-users-randomn0tnumber.xml`).
2. The system attempts to parse the suffix as an integer; because it is not a valid number the result is zero.
3. The response is identical to the first page, including the highest-comment-count user.

### Empty page beyond available users

1. A crawler requests a page index whose offset exceeds the total number of matching users (e.g., `/sitemap-users-2.xml` when fewer than `2 * RESULTS_LIMIT` users exist).
2. The query returns no rows.
3. The response is a valid XML document with an empty `<urlset>` — no user URLs are listed.

## Failures / Exceptions

- Users with `score <= -1` are silently excluded from all sitemap pages as a spam mitigation measure; no error is raised and no indication of exclusion appears in the response.
