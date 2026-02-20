---
id: "01KHY7Q0BNTVGC5VGAN3G2DJNS"
name: "tags_suggested_for_onboarding_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/tags/suggested_for_onboarding.rb
- app/controllers/admin/tags/moderators_controller.rb
- app/controllers/admin/tags_controller.rb
- app/controllers/api/v0/tags_controller.rb
- app/controllers/api/v1/tags_controller.rb
- app/controllers/concerns/api/tags_controller.rb
- app/controllers/liquid_tags_controller.rb
- app/controllers/tags_controller.rb
- app/workers/tags/alias_retag_worker.rb
- app/workers/tags/bust_cache_worker.rb
- app/workers/tags/resave_supported_tags_worker.rb
- spec/queries/tags/suggested_for_onboarding_spec.rb

## Functional Overview

This specification defines the expected behavior of `Tags::SuggestedForOnboarding` within the tags domain.

### Behavioral Areas

- **when suggested tags aren**: starts with Settings::General::SuggestedTags

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/tags/suggested_for_onboarding.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/tags/moderators_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/tags_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/tags/alias_retag_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/tags/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/tags/resave_supported_tags_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: starts with Settings::General::SuggestedTags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** starts with Settings::General::SuggestedTags

### S-2: adds supported tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds supported tags

