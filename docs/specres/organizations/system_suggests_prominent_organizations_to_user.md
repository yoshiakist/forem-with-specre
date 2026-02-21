---
id: "01KJ02W17VA8P0SYXCYAJ1MJR2"
name: "system_suggests_prominent_organizations_to_user"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/queries/organizations/suggest_prominent.rb`
- `spec/queries/organizations/suggest_prominent_spec.rb` (Test)

## Functional Overview

When the system needs to recommend organizations to a user, it queries for organizations that have published high-scoring articles tagged with topics the user already follows. Up to five organizations are returned in random order so that suggestions feel fresh on each request. If the user follows no tags, the system returns an empty list rather than surfacing arbitrary organizations.

## Design Intent

Relevance is established through two signals: the user's followed tags and article quality score. Using both filters together ensures that only organizations whose content genuinely aligns with the user's interests — and meets the platform's quality bar — are surfaced. Returning results in random order prevents the same organizations from always appearing at the top, which improves perceived variety for users who see the widget repeatedly. Returning an empty list when the user has no followed tags avoids recommending organizations that have no demonstrated relevance.

## Key Members

- `MAX` — hard cap of 5 on the number of organizations returned per call
- `user` — the authenticated user whose followed tags and preferences drive the suggestion
- `tags_to_consider` — the list of tag names the user follows, derived from cached data on the user decorator
- `fetch_and_pluck_org_ids` — resolves the lookback window and minimum score threshold from site-wide settings, then collects organization IDs from qualifying articles
- `Settings::UserExperience.feed_lookback_days` — configures how far back in time published articles are considered; defaults to two weeks when not set or zero
- `Settings::UserExperience.index_minimum_score` — the platform quality threshold; the effective minimum for suggestions is double this value

## Scenarios

### User follows at least one tag — organizations are suggested

1. The caller invokes `Organizations::SuggestProminent` with the current user.
2. The system retrieves the tag names the user follows from the user's cached decorator data.
3. Because at least one tag is found, the system queries published articles from the current subforem that are tagged with any of those tags and that are not associated with an organization-less author.
4. The query filters to articles published within the configured lookback window and with a score more than double the platform's minimum index score.
5. Organization IDs are collected from the top `MAX * 2` highest-scoring qualifying articles.
6. Duplicate organization IDs are removed, and the matching organizations are loaded in random order, limited to `MAX` (5).
7. The resulting collection of up to 5 organizations is returned to the caller.

### User follows no tags — empty list is returned

1. The caller invokes `Organizations::SuggestProminent` with a user who follows no tags.
2. The system retrieves the user's followed tag names and finds the list empty.
3. The system returns an empty array immediately without querying articles or organizations.

## Failures / Exceptions

- If no articles match the tag, recency, and score filters, `fetch_and_pluck_org_ids` returns an empty array and the resulting `Organization.where` call returns no records.
- If `Settings::UserExperience.feed_lookback_days` is zero or not set to a positive integer, the lookback window defaults to two weeks ago.
