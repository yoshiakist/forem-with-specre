---
id: "01KHYAH6H7WPMS2EW9Y1XK6QYJ"
name: "organizations_suggest_prominent_recommends_by_tags"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/organizations/suggest_prominent.rb
- spec/queries/organizations/suggest_prominent_spec.rb (Test)

## Functional Overview

The Organizations::SuggestProminent query generates a curated list of up to 5 recommended organizations based on the user's followed tags. It finds recent high-scoring articles tagged with the user's interests, extracts their organization IDs, and returns a randomized set of matching organizations.

## Scenarios

### System suggests prominent organizations for a user

1. The system retrieves the user's followed tag names.
2. If the user follows no tags, the system returns an empty list.
3. The system queries published articles from the current subforem that are tagged with any of the user's followed tags, have an organization, were published within the lookback period, and score above twice the index minimum score setting.
4. The system orders matching articles by score descending and takes up to 10 organization IDs.
5. The system deduplicates the organization IDs, fetches matching Organization records, randomizes the order, and limits to 5 results.

## Key Members

- `MAX`: Maximum number of suggested organizations (5).
- `feed_lookback_days`: Setting that controls the article recency window; defaults to 2 weeks if not configured.
- `index_minimum_score`: Setting threshold; articles must score above twice this value.
