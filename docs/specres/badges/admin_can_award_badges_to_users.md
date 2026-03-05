---
id: "01KJ6FBFV0DKQVMBPB49V7ZKCB"
name: "admin_can_award_badges_to_users"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/badge_achievements_controller.rb`
- `app/workers/badge_achievements/badge_award_worker.rb`
- `app/services/badges/award.rb`
- `app/views/admin/badge_achievements/award.html.erb` (Template)
- `spec/requests/admin/badge_achievements_spec.rb` (Test)
- `spec/services/badges/award_spec.rb` (Test)
- `spec/workers/badge_achievements/badge_award_worker_spec.rb` (Test)

## Functional Overview

An admin can award one or more badges to a list of users by submitting a form with a badge slug, a comma-separated list of usernames, an optional custom message, and an optional flag to include the badge's default description. The controller normalises the usernames to lowercase, falls back to a community-specific congratulatory message when no custom message is provided, and hands the work off to `BadgeAchievements::BadgeAwardWorker` as an asynchronous Sidekiq job on the high-priority queue. The worker resolves the user relation and delegates to `Badges::Award`, which creates a `BadgeAchievement` record for each eligible user, skipping any banished accounts. If the badge slug matches a predefined award class (e.g. `Badges::AwardYearlyClub`), that class's `call` method is invoked directly instead.

## Design Intent

Award processing runs asynchronously via a high-priority Sidekiq worker so that bulk awards to many users do not block the HTTP request cycle. The worker checks for a predefined award class first, enabling badge-specific logic (e.g. yearly club eligibility checks) to be encapsulated without changing the general award path.

## Key Members

- `usernames` — comma-separated string of target usernames; normalised to lowercase before passing to the worker
- `badge` — slug of the badge to award
- `message_markdown` — optional custom markdown message; defaults to a community congratulations string when blank
- `include_default_description` — boolean flag ("1" / "0") controlling whether the badge's default description is appended to the achievement

## Scenarios

### Admin awards a badge with a custom message

1. Admin navigates to the award form, which lists all available badges ordered by title.
2. Admin selects a badge, enters one or more usernames (comma-separated), and provides a custom message.
3. Admin submits the form.
4. The controller normalises usernames to lowercase, enqueues `BadgeAchievements::BadgeAwardWorker` with the usernames, badge slug, custom message, and the include-default-description flag.
5. A success flash message confirms that awarding is in progress, and the admin is redirected to the badge achievements index.

### Admin awards a badge without a custom message (default message used)

1. Admin submits the award form leaving the message field blank.
2. The controller detects no custom message and substitutes the community-specific congratulatory message.
3. The worker is enqueued with the default message; subsequent steps are the same as the custom-message scenario.

### Worker delegates to `Badges::Award` for a standard badge

1. The worker receives a list of usernames, a badge slug, a message, and the include-default-description flag.
2. The slug does not match any predefined award class.
3. The worker resolves the user relation via `User.where(username: usernames)` and calls `Badges::Award.call` with that relation, slug, message, and flag.
4. `Badges::Award` iterates the relation and creates a `BadgeAchievement` for each non-banished user, storing the message and description flag on each record.

### Worker dispatches to a predefined award class

1. The worker receives a badge slug that maps to a predefined class (e.g. `award_yearly_club` → `Badges::AwardYearlyClub`).
2. The worker calls `Badges::AwardYearlyClub.call` directly and does not invoke `Badges::Award`.

### Banished users are skipped during award

1. `Badges::Award` iterates the user relation.
2. For any user flagged as banished, the service skips badge creation entirely.
3. Non-banished users in the same relation receive their badge achievements as normal.

## Failures / Exceptions

- If no badge slug is provided in the form submission, the controller raises `ArgumentError` with a localised message, sets a danger flash, and redirects back to the badge achievements index without enqueuing the worker.
- If destroying a `BadgeAchievement` fails, the controller returns a 422 JSON response with an error message.
