---
id: "01KHY7Q0NA7DWYG29822CN2WWW"
name: "spam_domain_detector_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/spam/domain_detector.rb
- app/services/notifications/remove_by_spammer.rb
- app/services/slack/messengers/potential_spammer.rb
- app/services/spam/handler.rb
- app/services/spam/reaction_ring_detector.rb
- app/services/users/resolve_spam_reports.rb
- app/workers/articles/handle_spam_worker.rb
- app/workers/comments/handle_spam_worker.rb
- app/workers/notifications/remove_by_spammer_worker.rb
- app/workers/spam/block_domain_and_suspend_users_worker.rb
- app/workers/spam/reaction_ring_detection_worker.rb
- spec/services/spam/domain_detector_spec.rb

## Functional Overview

This specification defines the expected behavior of `Spam::DomainDetector` within the moderation domain.

### Behavioral Areas

- **check_and_block_domain!**: Ensures correct behavior under the specified conditions
- **when domain should be skipped**: returns false and does not block domain
- **when spam pattern is detected**: does not block the domain when legitimate users exist
- **when there are legitimate users with the same email**: enqueues background job to block domain and suspend users
- **when there are not enough spam users**: enqueues background job to block domain and suspend users
- **when spam users are older than 2 weeks**: enqueues background job to block domain and suspend users
- **should_skip_domain?**: Ensures correct behavior under the specified conditions
- **extract_domain**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/spam/domain_detector.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/notifications/remove_by_spammer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/slack/messengers/potential_spammer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/spam/handler.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/spam/reaction_ring_detector.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/users/resolve_spam_reports.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/articles/handle_spam_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/comments/handle_spam_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/notifications/remove_by_spammer_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/spam/block_domain_and_suspend_users_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/spam/reaction_ring_detection_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns false and does not block domain

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false and does not block domain

### S-2: enqueues background job to block domain and suspend users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues background job to block domain and suspend users

### S-3: enqueues job with correct domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues job with correct domain

### S-4: does not block the domain when legitimate users exist

- **Given** the system is in a standard operational state
- **When** legitimate users exist
- **Then** does not block the domain

### S-5: does not block the domain when there are only 2 spam users

- **Given** the system is in a standard operational state
- **When** there are only 2 spam users
- **Then** does not block the domain

### S-6: does not block the domain when spam users are too old

- **Given** the system is in a standard operational state
- **When** spam users are too old
- **Then** does not block the domain

### S-7: skips popular shared domains

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** skips popular shared domains

### S-8: does not skip custom domains

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not skip custom domains

### S-9: extracts domain from email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** extracts domain from email

### S-10: handles uppercase emails

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles uppercase emails

### S-11: returns nil for blank emails

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns nil for blank emails

