---
id: "01KJ6FP6NRZAWBSV32RZESNH58"
name: "system_awards_yearly_club_badges"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/badges/award_yearly_club.rb`
- `spec/services/badges/award_yearly_club_spec.rb` (Test)

## Functional Overview

The `Badges::AwardYearlyClub` service awards anniversary club badges to registered users whose account creation date falls within a two-day window of each whole-year anniversary. On each invocation it calculates the total number of years since the community's copyright start year, then iterates over each year from one up to that total. For each year it selects users whose accounts were created between two days before and exactly that many years ago, and calls `Badges::Award` with the corresponding named badge (e.g., "one-year-club", "two-year-club") and a localised congratulatory message that includes the community name and the number of years.

## Key Members

- `YEARS` — A frozen hash mapping integer year counts (1–13) to their English word equivalents used to construct badge slugs such as "one-year-club".
- `Settings::Community.copyright_start_year` — Determines the earliest year the community existed, which sets the upper bound of anniversary years to process.
- `Settings::Community.community_name` — Included in the badge award message via I18n.

## Scenarios

### Awarding a one-year anniversary badge

1. The service calculates the number of full years elapsed since the community's copyright start year.
2. For each elapsed year, it determines the precise registration window: from two days before that anniversary up to the anniversary date itself.
3. It selects all registered users whose accounts were created within that window.
4. It calls the award service for those users with the badge slug corresponding to the year count (e.g., "one-year-club") and a personalised message.
5. Each matched user receives one badge achievement for that anniversary.

### Only users within the two-day window receive a badge

1. A user registered exactly one year ago (e.g., 366 days ago) falls inside the two-day window and is awarded the one-year-club badge.
2. A user registered only six days ago is outside every anniversary window and receives no badge.
3. A user registered 390 days ago is outside the one-year window and receives no badge.

### Multiple anniversary years are processed in a single call

1. The service iterates over all years from one up to the total elapsed years.
2. Users who registered approximately two years ago receive the two-year-club badge.
3. Users who registered approximately three years ago receive the three-year-club badge.
4. Each anniversary year is handled independently; a user can receive at most one badge per call if they fall in exactly one window.

### Badge message is localised and community-aware

1. For each award, the service generates a message via `I18n.t` using the key `services.badges.award_yearly_club.message`.
2. The message includes the community name from `Settings::Community.community_name` and the numeric year count.
3. The localised message is passed directly to `Badges::Award` alongside the badge slug.

## Failures / Exceptions

- If `Settings::Community.copyright_start_year` returns a value equal to or greater than the current year, `total_years` will be zero or negative and the iteration range produces no awards without raising an error.
- Year counts beyond 13 have no entry in `YEARS`, so `generate_message` would still be called but the badge slug would become `"-year-club"` due to a `nil` lookup — badge creation for those years depends on whether a matching badge record exists in the database.
