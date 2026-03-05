---
id: "01KJ9JGGNEP4QG1M8993MB2A5K"
name: "system_checks_subscription_status_with_cache"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/controllers/user_subscriptions_controller.rb` (subscribed action)
- `app/services/user_subscriptions/is_subscribed_cache_checker.rb`
- `spec/services/user_subscriptions/is_subscribed_cache_checker_spec.rb` (Test)

## Functional Overview

`UserSubscriptions::IsSubscribedCacheChecker` is a service object that determines whether a given user is subscribed to a particular source (identified by type and ID). The result is cached in Rails cache for 24 hours using a cache key that encodes the user's identity, last-updated timestamp, and current subscription count, ensuring the cached value is automatically invalidated whenever any of those properties change. If no cached result exists, the service queries `UserSubscription` records directly and stores the boolean outcome.

## Design Intent

The cache key includes `user.updated_at` and `user.subscribed_to_user_subscriptions_count` so that any change to the user record or their subscription list naturally busts the cache without requiring an explicit invalidation step. This avoids stale reads after a user subscribes or unsubscribes, while still preventing repeated database queries for the common read path.

## Key Members

- `user` — the subscriber whose subscription status is being checked
- `source_type` — the polymorphic type string of the subscription source (e.g., an article class name)
- `source_id` — the ID of the subscription source record

## Scenarios

### User is subscribed to the source

1. Caller invokes the service with a user and a source identified by type and ID.
2. System constructs a cache key that incorporates the user's ID, last-updated timestamp, and subscription count.
3. System looks up the key in the cache; if a cached value exists, it is returned immediately.
4. If the cache is empty, the system queries the `UserSubscription` table for a matching record.
5. System stores the result in the cache with a 24-hour expiry and returns `true`.

### User is not subscribed to the source

1. Caller invokes the service with a user and a source for which no subscription exists.
2. System constructs the same cache key and finds no cached value.
3. System queries `UserSubscription` and finds no matching record.
4. System caches the result with a 24-hour expiry and returns `false`.

### Cached result is reused on subsequent calls

1. A previous call has already stored a result in the cache under the user's current key.
2. Caller invokes the service again with the same user and source.
3. System finds the cached boolean and returns it without querying the database.

### Cache is invalidated after user record changes

1. The user's `updated_at` timestamp or `subscribed_to_user_subscriptions_count` changes (e.g., after a new subscription is created).
2. On the next call, the system computes a different cache key because one of the key components has changed.
3. System finds no cached value under the new key and falls back to a fresh database query.
