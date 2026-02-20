---
id: "01KHY7Q0HP546BV629DAYVKDGC"
name: "organizations_suggest_prominent_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/organizations/suggest_prominent.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- app/helpers/admin/organizations_helper.rb
- app/services/organizations/delete.rb
- app/workers/organizations/bust_cache_worker.rb
- app/workers/organizations/delete_worker.rb
- app/workers/organizations/save_article_worker.rb
- spec/queries/organizations/suggest_prominent_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organizations::SuggestProminent` within the organizations domain.

### Behavioral Areas

- **when user is following any tags**: returns organizations with posts with at least an average score under followed tags
- **when user is not following any tags**: returns organizations with posts with at least an average score under followed tags

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/organizations/suggest_prominent.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/organizations_helper.rb` -- shared view utility methods
- **Service layer**: `app/services/organizations/delete.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/organizations/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/delete_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/save_article_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns organizations with posts with at least an average score under followed t...

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns organizations with posts with at least an average score under followed tags

### S-2: does not return organizations if no tags

- **Given** no tags
- **When** the action is triggered
- **Then** does not return organizations

