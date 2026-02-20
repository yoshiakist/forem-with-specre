---
id: "01KHY7PZNP6CPCJTY55FJA8A03"
name: "organizations_save_article_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/organizations/save_article_worker.rb
- app/workers/organizations/update_organization_articles_paths_worker.rb
- spec/workers/organizations/save_article_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organizations::SaveArticleWorker` within the articles domain.

### Behavioral Areas

- **perform**: Ensures correct behavior under the specified conditions
- **save articles with worker**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/organizations/save_article_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/organizations/update_organization_articles_paths_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: on organization slug change

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** on organization slug change

