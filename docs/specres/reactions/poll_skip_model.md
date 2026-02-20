---
id: "01KHY7Q0F1TT4XGQJ3GQAW7XPP"
name: "poll_skip_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/poll_skips_controller.rb
- app/models/poll_skip.rb
- app/models/poll_option.rb
- app/models/poll_text_response.rb
- app/models/poll_vote.rb
- app/models/privileged_reaction.rb
- app/models/rating_vote.rb
- app/models/reaction.rb
- app/models/reaction_category.rb
- spec/models/poll_skip_spec.rb

## Functional Overview

This specification defines the expected behavior of `PollSkip` within the reactions domain.

### Behavioral Areas

- **when user has not voted nor skipped the poll**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/poll_skips_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/poll_skip.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_option.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_text_response.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/poll_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/privileged_reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/rating_vote.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/reaction_category.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: is valid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is valid

