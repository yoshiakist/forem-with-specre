---
id: "01KJ9R7CKPYWVRFA54JHZ2DRSE"
name: "system_syncs_user_to_mailchimp_newsletter"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/workers/users/subscribe_to_mailchimp_newsletter_worker.rb`
- `spec/workers/users/subscribe_to_mailchimp_newsletter_worker_spec.rb` (Test)

## Functional Overview

When triggered, this background worker looks up a user by ID and, if the user exists and has an email address, calls the Mailchimp integration to upsert the user's subscription. The job runs on the low-priority queue with up to 10 retries and uses an until-executed lock to prevent duplicate runs for the same user.

## Design Intent

The until-executed lock ensures that only one Mailchimp sync runs per user at a time, preventing race conditions or double-subscriptions when the job is enqueued multiple times in rapid succession. Skipping users without an email address avoids sending invalid data to Mailchimp's API.

## Scenarios

### User with email is synced to Mailchimp

1. A job is enqueued with a valid user ID.
2. The worker finds the user in the database.
3. Because the user has an email address, the worker calls `Mailchimp::Bot` to upsert the subscription.
4. Mailchimp receives the user's current information.

### User without email is skipped

1. A job is enqueued with a user ID whose account has no email address.
2. The worker finds the user in the database.
3. Because the user has no email, the worker takes no action and exits without calling Mailchimp.

## Failures / Exceptions

- If no user is found for the given ID (e.g., the user was deleted before the job ran), the worker exits silently without raising an error.
