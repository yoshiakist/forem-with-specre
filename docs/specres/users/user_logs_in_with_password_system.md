---
id: "01KHY7Q0390J4Q7B8GM663GMS7"
name: "user_logs_in_with_password_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/gdpr_delete_requests_controller.rb
- app/controllers/admin/settings/authentications_controller.rb
- app/controllers/admin/settings/user_experiences_controller.rb
- app/controllers/admin/user_queries_controller.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- spec/system/user_logs_in_with_password_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Authenticating` within the users domain.

### Behavioral Areas

- **Authenticating with a password**: displays an error when the password is wrong
- **when logging in with incorrect credentials**: displays an error when the email address is wrong
- **when the user**: displays an error when the email address is wrong
- **when logging in with the correct credentials**: displays an error when the email address is wrong

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/gdpr_delete_requests_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/settings/user_experiences_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/user_queries_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: displays an error when the email address is wrong

- **Given** the system is in a standard operational state
- **When** the email address is wrong
- **Then** displays an error

### S-2: displays an error when the password is wrong

- **Given** the system is in a standard operational state
- **When** the password is wrong
- **Then** displays an error

### S-3: sends an email with the unlock link if the user gets locked out

- **Given** the user gets locked out
- **When** the action is triggered
- **Then** sends an email with the unlock link

### S-4: allows the user to unlock their account via social logins

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the user to unlock their account via social logins

### S-5: allows the user to sign in with the correct password

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the user to sign in with the correct password

