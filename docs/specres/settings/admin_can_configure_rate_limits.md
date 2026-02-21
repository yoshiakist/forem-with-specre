---
id: "01KHZ40W0YD7MCM63T2PZ9354A"
name: "admin_can_configure_rate_limits"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/settings/rate_limits_controller.rb`
- `app/models/settings/rate_limit.rb`
- `app/lib/constants/settings/rate_limit.rb`
- `app/views/admin/settings/forms/_rate_limit.html.erb` (Template)
- `spec/models/settings/rate_limit_spec.rb` (Test)

## Functional Overview

A super-admin can configure rate limits and anti-spam measures to protect the platform from abuse. The `Settings::RateLimit` model defines 15+ integer rate limits for various user actions (article updates, comment creation, reaction creation, image uploads, mention creation, etc.), a configurable threshold for considering users "new," and a list of spam trigger terms. The model provides two helper methods: `user_considered_new?` which checks if a user was created within the configured number of days, and `trigger_spam_for?` which compiles the spam trigger terms into a regular expression and checks text against it. The controller inherits directly from the base settings controller with no custom logic.

## Key Members

- `user_considered_new_days` — integer (default: 3) controlling the threshold for new-user stricter limits
- `spam_trigger_terms` — array of strings compiled into a regexp for text matching

## Scenarios

### Admin sets rate limits for user actions

1. Admin adjusts integer rate limits for actions such as article updates (default: 30), comment creation (default: 9), reaction creation (default: 10), and image uploads (default: 9)
2. System persists the values; rate-limiting middleware enforces these limits per user per time window

### Admin configures new user threshold

1. Admin sets `user_considered_new_days` (default: 3)
2. `user_considered_new?` returns true for users created within that many days, and also for nil users
3. New users may be subject to stricter rate limits or additional moderation checks

### Admin manages spam trigger terms

1. Admin enters `spam_trigger_terms` as a comma-separated list
2. `trigger_spam_for?` compiles the terms into a regular expression
3. When user-submitted text matches any trigger term, the system flags it as potential spam

### Admin sets content moderation description

1. Admin enters `internal_content_description_spec` to define rules for AI/automated content moderation
2. System persists the description for use by internal moderation systems
