---
id: "01KHY7PZK4T0QS7V59CZ1E2GQE"
name: "slack_messengers_article_published_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/slack/messengers/article_published.rb
- spec/services/slack/messengers/article_published_spec.rb

## Functional Overview

This specification defines the expected behavior of `Slack::Messengers::ArticlePublished` within the articles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/slack/messengers/article_published.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: does not message slack for a draft article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not message slack for a draft article

### S-2: does not message slack for an article that was published long ago

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not message slack for an article that was published long ago

### S-3: does not message slack if DISABLE_SLACK_NOTIFICATIONS is true

- **Given** DISABLE_SLACK_NOTIFICATIONS is true
- **When** the action is triggered
- **Then** does not message slack

### S-4: messages slack for an article that was published a few minutes ago

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** messages slack for an article that was published a few minutes ago

### S-5: contains the correct info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the correct info

### S-6: messages the proper channel with the proper username and emoji

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** messages the proper channel with the proper username and emoji

