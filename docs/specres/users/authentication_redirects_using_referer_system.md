---
id: "01KHY7Q00KKP2X4V7T1KV9MZFQ"
name: "authentication_redirects_using_referer_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/settings/authentications_controller.rb
- app/errors/authentication/errors.rb
- app/helpers/authentication_helper.rb
- app/lib/constants/settings/authentication.rb
- app/models/settings/authentication.rb
- app/services/authentication/authenticator.rb
- app/services/authentication/paths.rb
- app/services/authentication/providers.rb
- app/services/authentication/providers/apple.rb
- app/services/authentication/providers/facebook.rb
- spec/system/authentication/redirects_using_referer_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Redirects` within the users domain.

### Behavioral Areas

- **Redirects authentication using Referer**: redirects back to the main feed (root path)
- **when a valid referer is available**: Ensures correct behavior under the specified conditions
- **when no referer is available**: Ensures correct behavior under the specified conditions
- **when the referer is from an external host**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/settings/authentications_controller.rb` -- HTTP request routing and response handling
- `app/errors/authentication/errors.rb`
- **View helper**: `app/helpers/authentication_helper.rb` -- shared view utility methods
- `app/lib/constants/settings/authentication.rb`
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/authentication/authenticator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/paths.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/apple.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/facebook.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: redirects back to the main feed (root path)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects back to the main feed (root path)

### S-2: redirects back to an article page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects back to an article page

### S-3: /#{article.slug}

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /#{article.slug}

### S-4: redirects back to the main feed as default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects back to the main feed as default

### S-5: redirects back to the main feed as default

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects back to the main feed as default

