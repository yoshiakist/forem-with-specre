---
id: "01KHY7Q0N73NYPMH2P865D6TDP"
name: "slack_messengers_potential_spammer_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/slack/messengers/potential_spammer.rb
- spec/services/slack/messengers/potential_spammer_spec.rb

## Functional Overview

This specification defines the expected behavior of `Slack::Messengers::PotentialSpammer` within the moderation domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/slack/messengers/potential_spammer.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: contains the correct info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the correct info

### S-2: messages the proper channel with the proper username and emoji

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** messages the proper channel with the proper username and emoji

