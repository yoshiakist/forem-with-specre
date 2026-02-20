---
id: "01KHY7Q1JV128A8APM9QZ7M2J7"
name: "survey_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/surveys_controller.rb
- app/controllers/surveys_controller.rb
- app/liquid_tags/survey_tag.rb
- app/mailers/survey_mailer.rb
- app/models/survey.rb
- app/models/survey_completion.rb
- app/services/survey_completion_service.rb
- app/workers/emails/survey_daily_email_worker.rb
- spec/models/survey_spec.rb

## Functional Overview

This specification defines the expected behavior of `Survey` within the surveys domain.

### Behavioral Areas

- **slug**: rotates old slugs on update
- **to_param**: Ensures correct behavior under the specified conditions
- **completed_by_user?**: Ensures correct behavior under the specified conditions
- **when user has not responded to any polls**: returns true even when user has completed the survey
- **when user has responded to some polls but not all**: returns true even when user has completed the survey
- **when user has responded to all polls**: returns true even when user has completed the survey
- **when user has responded to all polls but in different sessions**: returns true even when user has completed the survey
- **when survey has no polls**: returns true even when user has completed the survey

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/surveys_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/surveys_controller.rb` -- HTTP request routing and response handling
- **Liquid tag**: `app/liquid_tags/survey_tag.rb` -- custom Markdown/Liquid embed rendering
- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery
- **Model layer**: `app/models/survey.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/survey_completion.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/survey_completion_service.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/emails/survey_daily_email_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: is generated from title on create

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is generated from title on create

### S-2: is not regenerated on update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is not regenerated on update

### S-3: can be updated manually

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can be updated manually

### S-4: rotates old slugs on update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rotates old slugs on update

### S-5: validates uniqueness

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates uniqueness

### S-6: allows nil slug

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows nil slug

### S-7: returns id

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns id

### S-8: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-9: returns false

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false

### S-10: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

### S-11: returns false (only counts responses in the same session)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false (only counts responses in the same session)

### S-12: returns true

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true

