---
id: "01KHY7Q1K6A7ZPPM01M6W2PY8H"
name: "ab_experiment_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/ab_experiment.rb
- app/models/ab_experiment/goal_conversion_handler.rb
- spec/models/ab_experiment_spec.rb

## Functional Overview

This specification defines the expected behavior of `AbExperiment` within the ab_testing domain.

### Behavioral Areas

- **CURRENT_FEED_STRATEGY_EXPERIMENT**: Ensures correct behavior under the specified conditions
- **validate field test experiment configuration**: is a key in the FieldTest.config[
- **.register_conversions_for**: Ensures correct behavior under the specified conditions
- **.get_feed_variant_for**: Ensures correct behavior under the specified conditions
- **.get**: Ensures correct behavior under the specified conditions
- **with :feed_strategy_round_3 experiment**: only allow at most one active feed_strategy (e.g. an experiment without a winner)
- **with :feed_strategy experiment**: only allow at most one active feed_strategy (e.g. an experiment without a winner)

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/ab_experiment.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/ab_experiment/goal_conversion_handler.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- be a String

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: is a key in the FieldTest.config[

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is a key in the FieldTest.config[

### S-3: only allow at most one active feed_strategy (e.g. an experiment without a winner...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only allow at most one active feed_strategy (e.g. an experiment without a winner)

### S-4: forwards delegates to Converter.call

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** forwards delegates to Converter.call

### S-5: returns an inquirable string

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an inquirable string

### S-6: repurposes the :feed_strategy experiment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** repurposes the :feed_strategy experiment

### S-7: returns an inquirable string

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an inquirable string

### S-8: allows for an config override

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows for an config override

### S-9: returns the default value when the FeatureFlipper is off

- **Given** the system is in a standard operational state
- **When** the FeatureFlipper is off
- **Then** returns the default value

