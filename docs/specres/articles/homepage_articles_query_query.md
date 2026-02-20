---
id: "01KHY7PZEDRAHQTGMQ79H1BVTX"
name: "homepage_articles_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/homepage/articles_query.rb
- app/serializers/homepage/article_serializer.rb
- app/services/homepage/fetch_articles.rb
- spec/queries/homepage/articles_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Homepage::ArticlesQuery` within the articles domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **approved**: returns both approved and unapproved articles by default
- **published_at**: sorts by published_at
- **user_id**: Ensures correct behavior under the specified conditions
- **organization_id**: Ensures correct behavior under the specified conditions
- **tags**: returns no articles if none of the tags match
- **hidden_tags**: removes articles matching any hidden_tags
- **pagination**: supports pagination params

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/homepage/articles_query.rb` -- complex database query encapsulation
- **Serializer**: `app/serializers/homepage/article_serializer.rb` -- API response formatting and data transformation
- **Service layer**: `app/services/homepage/fetch_articles.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns a relation object

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a relation object

### S-2: returns only published articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only published articles

### S-3: does not return scheduled articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return scheduled articles

### S-4: does not return draft articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return draft articles

### S-5: returns both approved and unapproved articles by default

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns both approved and unapproved articles by default

### S-6: returns approved articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns approved articles

### S-7: returns unapproved articles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unapproved articles

### S-8: filters by publication date

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters by publication date

### S-9: returns no articles if the user id does not exist

- **Given** the user id does not exist
- **When** the action is triggered
- **Then** returns no articles

### S-10: filters articles belonging to the given user id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters articles belonging to the given user id

### S-11: returns no articles if the organization id does not exist

- **Given** the organization id does not exist
- **When** the action is triggered
- **Then** returns no articles

### S-12: filters articles belonging to the given organization id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters articles belonging to the given organization id

