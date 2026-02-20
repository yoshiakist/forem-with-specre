---
id: "01KHY7Q042ZV189YKCW57BJC54"
name: "segmented_user_refresh_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/segmented_user_refresh_worker.rb
- app/workers/emails/send_user_digest_worker.rb
- app/workers/moderator/banish_user_worker.rb
- app/workers/spam/block_domain_and_suspend_users_worker.rb
- app/workers/users/bust_cache_worker.rb
- app/workers/users/bust_profile_details_cache_worker.rb
- app/workers/users/bust_profile_identity_cache_worker.rb
- app/workers/users/bust_profile_image_cache_worker.rb
- app/workers/users/confirm_flag_reactions_worker.rb
- app/workers/users/delete_worker.rb
- app/workers/users/follow_worker.rb
- spec/workers/segmented_user_refresh_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `SegmentedUserRefreshWorker` within the users domain.

### Behavioral Areas

- **when scenario is pre-built**: can confirm the scenario baseline by refreshing

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/segmented_user_refresh_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/emails/send_user_digest_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/moderator/banish_user_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/spam/block_domain_and_suspend_users_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/bust_profile_details_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/bust_profile_identity_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/bust_profile_image_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/confirm_flag_reactions_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/delete_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/users/follow_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: can confirm the scenario baseline by refreshing

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can confirm the scenario baseline by refreshing

### S-2: refreshes a user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** refreshes a user

