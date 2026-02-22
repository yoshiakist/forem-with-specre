---
id: "01KJ1SF43DPAEFTTZJQ449412V"
name: "system_awards_contributor_badge_from_github"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/badges/award_contributor_from_github.rb`
- `spec/services/badges/award_contributor_from_github_spec.rb` (Test)

## Functional Overview

When triggered, the system scans a fixed set of Forem GitHub repositories and awards contributor badges to Forem users whose GitHub identities match recent commit authors or all-time contributors. It awards a basic "dev-contributor" badge to anyone who committed in the past day, and tiered commit-club badges (4x, 8x, 16x, 32x) to users whose total contribution counts meet the respective thresholds. The service only runs when GitHub is configured as an OAuth provider, and each badge is created at most once per user per badge type.

## Design Intent

Badges are resolved to database IDs once at initialization (`get_badge_slugs_with_id`) so that every subsequent per-user record creation avoids repeated `Badge.id_for_slug` lookups. The single-commit path uses a recent-commits query (since yesterday) to handle high-volume repositories efficiently, while the multi-commit path fetches the full contributor list to apply tiered thresholds. Idempotency for the base badge is achieved by using `first_or_create` rather than bare `create`, preventing duplicate awards on repeated runs.

## Key Members

- `BADGE_SLUGS` — maps badge slug symbols to their minimum commit-count thresholds (1, 4, 8, 16, 32)
- `REPOSITORIES` — fixed list of four Forem-owned GitHub repositories scanned on every run
- `badge_slugs_with_id` — hash populated at initialization mapping each slug to its database Badge ID; slugs without a matching badge record are excluded via `compact`
- `msg` — rewarding context message attached to `BadgeAchievement` records; defaults to the i18n key `services.badges.thank_you`

## Scenarios

### GitHub OAuth not configured

1. The system checks whether `:github` is included in the configured authentication providers.
2. Because GitHub is not configured, the service exits immediately without querying any repository or creating any badge achievements.

### Awarding the base contributor badge to a recent committer

1. GitHub OAuth is configured as a provider.
2. For each repository in `REPOSITORIES`, the system fetches commits made since the previous day via `Github::OauthClient`.
3. The GitHub author IDs from those commits are matched against `Identity.github` records in the local database.
4. For each matching identity, a `BadgeAchievement` for the "dev-contributor" badge is created if one does not already exist, attaching the configured reward message.

### Awarding tiered commit-club badges to multi-commit contributors

1. GitHub OAuth is configured as a provider.
2. For each repository in `REPOSITORIES`, the system fetches the full contributor list (all-time) via `Github::OauthClient`.
3. The contributor GitHub IDs are matched against local `Identity.github` records.
4. For each matched identity, the system retrieves that contributor's total contribution count from the GitHub response.
5. For each badge slug in `badge_slugs_with_id`, if the contributor's count meets or exceeds the slug's threshold, a `BadgeAchievement` record is created for that badge.

### Base badge is awarded only once per user

1. The service is called multiple times for the same repository and user.
2. On the first call, a "dev-contributor" `BadgeAchievement` is created via `first_or_create`.
3. On subsequent calls, the existing record is found and no duplicate is created, leaving the user's badge count unchanged.

## Failures / Exceptions

- If a badge slug does not exist in the database, `Badge.id_for_slug` returns `nil` and the slug is excluded from `badge_slugs_with_id` via `compact`; no badge achievement is attempted for that slug.
- If a contributor's identity is present in the GitHub contributor list but not found in the local `Identity.github` table, no badge is awarded for that contributor.
- If a contributor's GitHub user record cannot be matched within the contributor list (`user_contribution.nil?`), the identity is skipped without raising an error.
