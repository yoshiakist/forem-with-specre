---
id: "01KJ9K7RA1VNB0WQR28RQHV8Q9"
name: "moderator_can_banish_user"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/services/moderator/banish_user.rb`
- `app/workers/moderator/banish_user_worker.rb`
- `spec/services/moderator/banish_user_spec.rb` (Test)
- `spec/workers/moderator/banish_user_worker_spec.rb` (Test)

## Functional Overview

When an administrator banishes a spam or abusive user, the system performs a comprehensive account purge: it records the ban in the `BanishedUser` table (capturing who performed the ban), removes the user from mailing lists, clears all profile information, suspends the account with a spam label, destroys any sole-member organizations, deletes all user-generated content (articles, comments, podcasts, follows, reactions), and finally renames the user's identity to an anonymous `spam_*` handle while busting the old username's edge cache.

## Design Intent

The banish operation is intentionally destructive and irreversible, designed to erase a spam account's footprint from the platform completely. Running the full sequence inside a single `banish` method (inheriting from `ManageActivityAndRoles`) ensures that no partial state is left behind if a moderator acts on a confirmed spam account. The worker runs on the `high_priority` queue with 10 retries so that a transient failure does not leave a harmful account active.

## Key Members

- `admin` — the `User` record of the moderator initiating the banishment; recorded in `BanishedUser` as `banished_by`
- `user` — the target `User` record being banished
- `DEFAULT_PROFILE_IMAGE` — a fixed placeholder image URL applied to the user after their profile picture is removed

## Scenarios

### Moderator initiates banishment via the worker

1. A super-admin triggers `Moderator::BanishUserWorker` with their own user ID and the target user's ID.
2. The worker looks up both users and delegates to `Moderator::BanishUser.call`.
3. The system executes the full banish sequence and the target account is left in a suspended, anonymous state.

### User identity is anonymised

1. The system generates a random `spam_*` name and username for the user, retrying if either value collides with an existing account.
2. The old username and profile image are replaced; the previous username is stored in `old_username`.
3. The edge cache for the old username URL is busted so stale profile pages are invalidated.

### Profile information is cleared

1. The user's profile fields (summary, location, website URL, linked social accounts, and all custom profile data) are wiped.
2. The profile image is replaced with the default spam placeholder.
3. If the user has an email address, they are removed from Mailchimp newsletters.

### User-generated content is removed

1. All of the user's articles, comments, and podcasts (including podcast ownerships) are deleted.
2. All social follows created by the user are removed.
3. "Vomit" reactions targeting the user are deleted.
4. Any `feedback_message` abuse reports against the user are resolved.

### Sole-member organizations are destroyed

1. For each organization the user belongs to, the system checks whether the user is the only member.
2. If the user is the sole member, the organization record is permanently destroyed.
3. Organizations with multiple members are left intact.

## Failures / Exceptions

- If any `StandardError` is raised during the worker's `perform`, the error is counted in `ForemStatsClient` (tagged with `action:failed` and the user ID) and forwarded to Honeybadger for alerting. The job will retry up to 10 times before being moved to the dead-letter queue.
