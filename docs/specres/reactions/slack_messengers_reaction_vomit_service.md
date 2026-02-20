---
id: "01KHY7Q0GHRYWXQF2G62P3SMSG"
name: "slack_messengers_reaction_vomit_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/slack/messengers/reaction_vomit.rb
- spec/services/slack/messengers/reaction_vomit_spec.rb

## Functional Overview

This specification defines the expected behavior of `Slack::Messengers::ReactionVomit` within the reactions domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/slack/messengers/reaction_vomit.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: does not message slack for a like reaction

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not message slack for a like reaction

### S-2: contains the correct info

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the correct info

### S-3: messages the proper channel with the proper username and emoji

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** messages the proper channel with the proper username and emoji

