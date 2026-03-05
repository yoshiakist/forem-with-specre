---
id: "01KJ6DW7GBQ5XAQKBV7MCPS2FA"
name: "user_can_view_broadcast_notification"
status: "draft"
---

## Related Files

- `app/views/notifications/_broadcast.html.erb`
- `app/helpers/broadcasts_helper.rb`

## Functional Overview

When a broadcast is delivered to a user as a notification, the broadcast notification partial renders a card in the notifications UI showing the sender's avatar with a link to their profile, the broadcast's processed HTML content, and — for Welcome-type broadcasts — an additional paragraph linking to the user's notification settings. Fragment caching is applied per broadcast title to avoid redundant rendering. The content container is given a DOM ID derived from the broadcast title by lowercasing it, removing colons, and replacing spaces with underscores.

## Design Intent

Fragment caching on the broadcast title allows the expensive HTML rendering to be shared across all users who receive the same broadcast, since the content is identical for every recipient. The sanitized DOM ID enables JavaScript or CSS to target individual broadcast content blocks by a stable, predictable identifier.

## Key Members

- `notification.json_data` — Hash containing two sub-keys: `"broadcast"` (with `title`, `processed_html`, `type_of`) and `"user"` (with `id`, `path`, `username`), used to drive all rendering decisions
- `sanitized_broadcast_id(broadcast_title)` — Converts a broadcast title to a lowercase, colon-free, underscore-spaced string suitable for use as an HTML element ID

## Scenarios

### Viewing a standard broadcast notification

1. The user navigates to their notifications feed
2. A broadcast notification card is displayed with the promoted styling
3. The sender's avatar image is shown and linked to the sender's profile page
4. The broadcast's pre-processed HTML body is rendered inside a content container whose DOM ID is derived from the broadcast title

### Viewing a Welcome-type broadcast notification

1. The notification's broadcast payload carries `type_of` equal to `"Welcome"`
2. In addition to the avatar and broadcast content, an extra paragraph appears below the body
3. The paragraph contains an inline link directing the user to their notification settings page

### Fragment cache hit for a repeated broadcast

1. The broadcast notification is rendered for a user
2. Because the fragment cache already holds an entry keyed to that broadcast title, the inner HTML — avatar, content, and any type-specific additions — is served from cache without re-rendering
