---
id: "01KHY7Q1CM2SSZSKJKZ0QP1VQY"
name: "content_renderer_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/content_renderer.rb
- app/services/markdown_processor.rb
- app/services/markdown_processor/fixer/base.rb
- app/services/markdown_processor/fixer/fix_all.rb
- app/services/markdown_processor/fixer/fix_for_comment.rb
- app/services/markdown_processor/fixer/fix_for_preview.rb
- app/services/markdown_processor/parser.rb
- app/services/markdown_processor/traverser.rb
- spec/services/content_renderer_spec.rb

## Functional Overview

This specification defines the expected behavior of `ContentRenderer` within the content_rendering domain.

### Behavioral Areas

- **process**: calculates reading time if processing an article
- **with double parser**: calls finalize with link_attributes
- **when processing links**: calculates reading time if processing an article
- **process_article**: Ensures correct behavior under the specified conditions
- **when markdown is valid**: processes markdown
- **when markdown contains an invalid liquid tag**: processes markdown
- **when markdown has liquid tags that aren**: processes markdown
- **when markdown has invalid frontmatter**: processes markdown

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/content_renderer.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/base.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/fix_all.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/fix_for_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/fix_for_preview.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/parser.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/traverser.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: calls fixer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls fixer

### S-2: calls finalize with link_attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls finalize with link_attributes

### S-3: adds target=

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** adds target=

### S-4: does not add target=

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not add target=

### S-5: does not add target=

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not add target=

### S-6: calculates reading time if processing an article

- **Given** processing an article
- **When** the action is triggered
- **Then** calculates reading time

### S-7: sets front_matter if it exists

- **Given** it exists
- **When** the action is triggered
- **Then** sets front_matter

### S-8: processes markdown

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** processes markdown

### S-9: raises ContentParsingError for comment

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises ContentParsingError for comment

### S-10: raises ContentParsingError for comment

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises ContentParsingError for comment

### S-11: raises ContentParsingError for billboard

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises ContentParsingError for billboard

### S-12: raises ContentParsingError

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises ContentParsingError

