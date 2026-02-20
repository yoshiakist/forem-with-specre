---
id: "01KHY7Q1D5AJBXJ0MFX57XXZ4F"
name: "data_update_scripts_insert_apple_connect_broadcast_message_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/broadcasts_controller.rb
- app/helpers/broadcasts_helper.rb
- app/models/broadcast.rb
- app/services/broadcasts/welcome_notification/generator.rb
- app/workers/broadcasts/send_welcome_notifications_worker.rb
- spec/lib/data_update_scripts/insert_apple_connect_broadcast_message_spec.rb

## Functional Overview

This specification defines the expected behavior of `Insert_Apple_Connect_Broadcast_Message` within the broadcasts domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/broadcasts_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/broadcasts_helper.rb` -- shared view utility methods
- **Model layer**: `app/models/broadcast.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/broadcasts/welcome_notification/generator.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/broadcasts/send_welcome_notifications_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: works without a broadcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works without a broadcast

### S-2: works when a Broadcast already exists

- **Given** the system is in a standard operational state
- **When** a Broadcast already exists
- **Then** works

