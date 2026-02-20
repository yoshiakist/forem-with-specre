---
id: "01KHY7Q0BDGT5FZ22QMNVNFZ72"
name: "badge_achievements_badge_award_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/badge_achievements/badge_award_worker.rb
- app/controllers/admin/badge_achievements_controller.rb
- app/controllers/api/v0/badge_achievements_controller.rb
- app/controllers/api/v1/badge_achievements_controller.rb
- app/controllers/concerns/api/badge_achievements_controller.rb
- app/workers/badge_achievements/send_email_notification_worker.rb
- spec/workers/badge_achievements/badge_award_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `BadgeAchievements::BadgeAwardWorker` within the badges domain.

### Behavioral Areas

- **perform_now**: Ensures correct behavior under the specified conditions
- **with badge achievement**: sends badge email
- **with predefined badge_slug**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/badge_achievements/badge_award_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/badge_achievements_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/badge_achievements/send_email_notification_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: sends badge email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends badge email

### S-2: sends badge email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends badge email

