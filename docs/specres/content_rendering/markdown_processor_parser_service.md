---
id: "01KHY7Q1CZHE4D7NYJBMYSQ5QX"
name: "markdown_processor_parser_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/markdown_processor/parser.rb
- app/services/markdown_processor.rb
- app/services/markdown_processor/fixer/base.rb
- app/services/markdown_processor/fixer/fix_all.rb
- app/services/markdown_processor/fixer/fix_for_comment.rb
- app/services/markdown_processor/fixer/fix_for_preview.rb
- app/services/markdown_processor/traverser.rb
- spec/services/markdown_processor/parser_spec.rb

## Functional Overview

This specification defines the expected behavior of `MarkdownProcessor::Parser` within the content_rendering domain.

### Behavioral Areas

- **when rendering links markdown**: renders complex markdown content without Liquid syntax errors
- **image URL processing**: replaces the image URL in the HTML but not in the Markdown
- **mentions**: Ensures correct behavior under the specified conditions
- **when checking XSS attempt in markdown content**: renders complex markdown content without Liquid syntax errors
- **when provided with an @username**: renders complex markdown content without Liquid syntax errors
- **when html has injected styles**: does not render the escaped dashes when using a `raw` Liquid tag in codeblocks with syntax highlighting
- **when provided with nested links**: renders complex markdown content without Liquid syntax errors
- **when provided with liquid tags**: renders complex markdown content without Liquid syntax errors

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/markdown_processor/parser.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/base.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/fix_all.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/fix_for_comment.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/fixer/fix_for_preview.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/markdown_processor/traverser.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: renders complex markdown content without Liquid syntax errors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders complex markdown content without Liquid syntax errors

### S-2: renders plain text as-is

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders plain text as-is

### S-3: escapes liquid tags in codeblock

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** escapes liquid tags in codeblock

### S-4: escapes the `raw` Liquid tag in codeblocks

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** escapes the `raw` Liquid tag in codeblocks

### S-5: does not allow button tag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not allow button tag

### S-6: does not render the escaped dashes when using a `raw` Liquid tag in codeblocks w...

- **Given** the system is in a standard operational state
- **When** using a `raw` Liquid tag in codeblocks with syntax highlighting
- **Then** does not render the escaped dashes

### S-7: escapes some triple backticks within a codeblock when using tildes

- **Given** the system is in a standard operational state
- **When** using tildes
- **Then** escapes some triple backticks within a codeblock

### S-8: allows more than 1 codeblock written separately

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows more than 1 codeblock written separately

### S-9: does not throw an error if code in codeblock does not match language

- **Given** code in codeblock does not match language
- **When** the action is triggered
- **Then** does not throw an error

### S-10: does not remove the non-

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not remove the non-

### S-11: escapes the `raw` Liquid tag in codespans

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** escapes the `raw` Liquid tag in codespans

### S-12: escapes the `raw` Liquid tag in inline code

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** escapes the `raw` Liquid tag in inline code

