---
id: "01KHY7Q0JPHJVQTC8PTHP6BJZF"
name: "organizations_track_promotional_billboard_impressions_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/organizations/track_promotional_billboard_impressions_worker.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- app/helpers/admin/organizations_helper.rb
- app/queries/organizations/suggest_prominent.rb
- app/services/organizations/delete.rb
- app/workers/organizations/bust_cache_worker.rb
- app/workers/organizations/delete_worker.rb
- spec/workers/organizations/track_promotional_billboard_impressions_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organizations::TrackPromotionalBillboardImpressionsWorker` within the organizations domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **when organization has tracking enabled**: caches empty list of paused organization IDs
- **when impressions are within limit**: updates past 24 hours impressions and does not pause
- **when impressions exceed 2x ideal daily**: updates past 24 hours impressions and does not pause
- **when impressions exactly equal 2x ideal daily**: updates past 24 hours impressions and does not pause
- **when organization transitions from paused to unpaused**: caches empty list of paused organization IDs
- **with multiple billboards for the same organization**: caches empty list of paused organization IDs
- **when only counting impression events**: updates past 24 hours impressions and does not pause

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/organizations/track_promotional_billboard_impressions_worker.rb` -- asynchronous job processing
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/organizations_helper.rb` -- shared view utility methods
- **Query object**: `app/queries/organizations/suggest_prominent.rb` -- complex database query encapsulation
- **Service layer**: `app/services/organizations/delete.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/organizations/bust_cache_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/delete_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: updates past 24 hours impressions and does not pause

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates past 24 hours impressions and does not pause

### S-2: caches empty list of paused organization IDs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caches empty list of paused organization IDs

### S-3: updates past 24 hours impressions and pauses promotional billboards

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates past 24 hours impressions and pauses promotional billboards

### S-4: caches the paused organization ID

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caches the paused organization ID

### S-5: does not pause (must be greater than 2x)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not pause (must be greater than 2x)

### S-6: unpauses the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** unpauses the organization

### S-7: removes organization from cached paused list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes organization from cached paused list

### S-8: sums impressions across all billboards

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sums impressions across all billboards

### S-9: only counts impression events

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only counts impression events

### S-10: does not process the organization

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not process the organization

### S-11: processes only organizations with tracking enabled

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** processes only organizations with tracking enabled

### S-12: caches only paused organization IDs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** caches only paused organization IDs

