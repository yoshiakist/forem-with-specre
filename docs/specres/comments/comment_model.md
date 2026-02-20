---
id: "01KHY7PZP7T3VPKK4XM2R0NV9N"
name: "comment_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/comments_controller.rb
- app/controllers/api/v0/comments_controller.rb
- app/controllers/api/v1/comments_controller.rb
- app/controllers/comments_controller.rb
- app/controllers/concerns/api/comments_controller.rb
- app/decorators/comment_decorator.rb
- app/helpers/comments_helper.rb
- app/liquid_tags/comment_tag.rb
- app/models/comment.rb
- app/models/concerns/algolia_searchable/searchable_comment.rb
- app/policies/comment_policy.rb
- app/sanitizers/comment_email_scrubber.rb
- app/serializers/search/comment_serializer.rb
- app/services/ai/comment_check.rb
- app/services/ai/comment_helpfulness_assessor.rb
- spec/models/comment_spec.rb

## Functional Overview

This specification defines the expected behavior of `Comment` within the comments domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **commentable**: is invalid if commentable is an unpublished article
- **body_has_content**: Ensures correct behavior under the specified conditions
- **user_mentions_in_markdown**: Ensures correct behavior under the specified conditions
- **search_id**: Ensures correct behavior under the specified conditions
- **processed_html**: converts body_markdown to proper processed_html
- **id_code_generated**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/comments_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/comments_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/comment_decorator.rb` -- presentation logic and view-model enrichment
- **View helper**: `app/helpers/comments_helper.rb` -- shared view utility methods
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/comment.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_comment.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/comment_policy.rb` -- authorization and access control rules
- `app/sanitizers/comment_email_scrubber.rb`


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user
- belong to commentable.optional
- have many reactions.dependent destroy
- have many mentions.dependent delete all
- have many notifications.dependent delete all
- have many notification subscriptions.dependent destroy
- validate presence of body markdown
- validate presence of positive reactions count
- validate presence of public reactions count
- validate presence of reactions count
- validate length of body markdown.is at least 1.is at most 25 000

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is invalid if commentable is an unpublished article

- **Given** commentable is an unpublished article
- **When** the action is triggered
- **Then** is invalid

### S-3: is invalid if commentable is an article and the discussion is locked

- **Given** commentable is an article and the discussion is locked
- **When** the action is triggered
- **Then** is invalid

### S-4: is valid without a commentable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid without a commentable

### S-5: checks for commentable_id presence only if commentable_type is present

- **Given** commentable_type is present
- **When** the action is triggered
- **Then** checks for commentable_id presence only

### S-6: is invalid when body_markdown contains only bold formatting (****)

- **Given** the system is in a standard operational state
- **When** body_markdown contains only bold formatting (****)
- **Then** is invalid

### S-7: is invalid when body_markdown contains only bold with spaces (** **)

- **Given** the system is in a standard operational state
- **When** body_markdown contains only bold with spaces (** **)
- **Then** is invalid

### S-8: is invalid when body_markdown contains only horizontal rule (---)

- **Given** the system is in a standard operational state
- **When** body_markdown contains only horizontal rule (---)
- **Then** is invalid

### S-9: is valid when body_markdown contains text with bold formatting

- **Given** the system is in a standard operational state
- **When** body_markdown contains text with bold formatting
- **Then** is valid

### S-10: is valid when body_markdown contains text with italic formatting

- **Given** the system is in a standard operational state
- **When** body_markdown contains text with italic formatting
- **Then** is valid

### S-11: is valid when body_markdown contains text with mixed formatting

- **Given** the system is in a standard operational state
- **When** body_markdown contains text with mixed formatting
- **Then** is valid

### S-12: is valid when body_markdown contains only plain text

- **Given** the system is in a standard operational state
- **When** body_markdown contains only plain text
- **Then** is valid

### S-13: is valid when body_markdown contains only an image

- **Given** the system is in a standard operational state
- **When** body_markdown contains only an image
- **Then** is valid

