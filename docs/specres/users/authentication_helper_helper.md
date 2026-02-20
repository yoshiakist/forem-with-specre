---
id: "01KHY7PZSJNVTWCDET99GEADKM"
name: "authentication_helper_helper"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/helpers/authentication_helper.rb
- app/helpers/admin/users_helper.rb
- app/helpers/users_helper.rb
- spec/helpers/authentication_helper_spec.rb

## Functional Overview

This specification defines the expected behavior of `AuthenticationHelper` within the users domain.

### Behavioral Areas

- **authentication_enabled_providers_for_user**: Ensures correct behavior under the specified conditions
- **signed_up_with**: Ensures correct behavior under the specified conditions
- **available_providers_array**: Ensures correct behavior under the specified conditions
- **authentication_provider_enabled?**: Ensures correct behavior under the specified conditions
- **tooltip classes, attributes and content**: Ensures correct behavior under the specified conditions
- **when invite-only-mode enabled and no enabled registration options**: returns an enabled provider
- **display_social_login?**: Ensures correct behavior under the specified conditions
- **when the request is from a non-ForemWebView User Agent**: returns an authentication reminder when a user auths with a provider

### Implementation Architecture

The behavior is implemented across the following layers:

- **View helper**: `app/helpers/authentication_helper.rb` -- shared view utility methods
- **View helper**: `app/helpers/admin/users_helper.rb` -- shared view utility methods
- **View helper**: `app/helpers/users_helper.rb` -- shared view utility methods


## Scenarios

### S-1: returns an enabled provider

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an enabled provider

### S-2: does not return a disabled provider

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return a disabled provider

### S-3: returns an authentication reminder when a user auths with a provider

- **Given** the system is in a standard operational state
- **When** a user auths with a provider
- **Then** returns an authentication reminder

### S-4: returns an authentication reminder when a user signs up with email

- **Given** the system is in a standard operational state
- **When** a user signs up with email
- **Then** returns an authentication reminder

### S-5: returns array of available providers in lowercase

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns array of available providers in lowercase

### S-6: returns true when a provider has been enabled

- **Given** the system is in a standard operational state
- **When** a provider has been enabled
- **Then** returns true

### S-7: returns false when a provider has not yet been enabled

- **Given** the system is in a standard operational state
- **When** a provider has not yet been enabled
- **Then** returns false

### S-8: returns 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 

### S-9: returns 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns 

### S-10: returns appropriate text for 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns appropriate text for 

### S-11: responds with true regardless if the Apple Auth is enabled

- **Given** the Apple Auth is enabled
- **When** the action is triggered
- **Then** responds with true regardless

### S-12: responds with true when Apple Auth is enabled

- **Given** the system is in a standard operational state
- **When** Apple Auth is enabled
- **Then** responds with true

