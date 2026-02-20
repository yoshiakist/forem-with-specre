---
id: "01KHY7PZNSDXW3GJBZX08E5JR1"
name: "organizations_update_organization_articles_paths_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/organizations/update_organization_articles_paths_worker.rb
- app/workers/organizations/save_article_worker.rb
- spec/workers/organizations/update_organization_articles_paths_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organizations::UpdateOrganizationArticlesPathsWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **update article paths**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/organizations/update_organization_articles_paths_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/save_article_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: on organization slug change

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** on organization slug change

