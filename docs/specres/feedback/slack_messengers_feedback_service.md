---
id: "01KHY7Q1GFZ2ZFPEDZBR94XNYA"
name: "slack_messengers_feedback_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/feedback_messages_controller.rb
- app/controllers/api/v1/feedback_messages_controller.rb
- app/controllers/feedback_messages_controller.rb
- app/helpers/feedback_messages_helper.rb
- app/models/feedback_message.rb
- app/services/slack/messengers/feedback.rb
- spec/services/slack/messengers/feedback_spec.rb

## Functional Overview

This specification defines the expected behavior of `Slack::Messengers::Feedback` within the feedback domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/feedback_messages_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/feedback_messages_helper.rb` -- shared view utility methods
- **Model layer**: `app/models/feedback_message.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/slack/messengers/feedback.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: supports an anonymous report

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports an anonymous report

### S-2: contains user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains user

### S-3: contains report information

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains report information

### S-4: messages the proper channel with the proper username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** messages the proper channel with the proper username

### S-5: uses the cry emoji for abuse reports

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the cry emoji for abuse reports

### S-6: uses the robot face emoji for other reports

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the robot face emoji for other reports

