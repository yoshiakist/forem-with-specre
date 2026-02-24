---
id: "01KJ702TAET217EMSPHS27RTN1"
name: "system_assigns_experiment_variant"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/models/ab_experiment.rb`
- `spec/models/ab_experiment_spec.rb` (Test)
- `spec/factories/field_test_memberships.rb` (Test)

## Functional Overview

Experiments are defined declaratively in `config/field_test.yml` and activated by deploying the configuration via git push — there is no admin UI for creating or starting experiments. `AbExperiment` is a `SimpleDelegator` wrapping a controller object, providing an insulation layer between application logic and the `field_test` gem. The main public API is `AbExperiment.get`, which accepts an experiment name, a controller, a user, a default value, and an optional config override. It resolves the experiment to a handler method via `EXPERIMENT_TO_METHOD_NAME_MAP`, then delegates to that instance method. The `feed_strategy` handler checks the `:ab_experiment_feed_strategy` feature flag: if disabled it returns the default value immediately; otherwise it reads an optional ENV-backed config override or calls `field_test()` with the participant to obtain the assigned variant. All returned values are wrapped with `.inquiry` to support predicate-style checks (e.g., `result.original?`). A convenience method, `get_feed_variant_for`, hard-wires the current active feed-strategy experiment and its default variant. If the underlying `field_test` call raises `FieldTest::ExperimentNotFound`, the method logs a warning and falls back to the default value.

## Design Intent

`private_class_method :new` forces all callers through `AbExperiment.get`, enforcing the Law of Demeter and preventing bypassing the insulation layer. Wrapping the controller via `SimpleDelegator` is necessary because `field_test` requires controller context (request/cookies) when no user is present. Returning an inquirable string lets call sites use clean predicate checks without an explicit string comparison.

## Key Members

- `ORIGINAL_VARIANT` — the string `"original"`, used as the default feed-strategy variant
- `CURRENT_FEED_STRATEGY_EXPERIMENT` — the key of the first active (winner-less) `feed_strategy` experiment found in `FieldTest.config`
- `EXPERIMENT_TO_METHOD_NAME_MAP` — maps experiment keys to handler method names; currently maps `CURRENT_FEED_STRATEGY_EXPERIMENT` to `:feed_strategy`
- `config` parameter in `.get` — defaults to `ApplicationConfig`; accepts a hash with `"AB_EXPERIMENT_FEED_STRATEGY"` to override the variant without touching `field_test`

## Scenarios

### Variant assigned via field_test

1. A developer has defined an experiment in `config/field_test.yml` with variants, weights, goals, and a `started_at` date, and deployed the configuration.
2. Caller invokes `AbExperiment.get` with the experiment name, controller, user, and default value.
3. The system looks up the handler method for the experiment in `EXPERIMENT_TO_METHOD_NAME_MAP`.
4. The `:ab_experiment_feed_strategy` feature flag is checked and found to be enabled.
5. No config override is present, so `field_test` is called with the user as the participant.
6. The variant string returned by `field_test` is wrapped with `.inquiry` and returned to the caller.

### Variant overridden via environment config

1. Caller invokes `AbExperiment.get` and passes a `config` hash containing `"AB_EXPERIMENT_FEED_STRATEGY"`.
2. The feature flag check passes.
3. Because a config override is present, `field_test` is not called.
4. The override value is wrapped with `.inquiry` and returned.

### Feature flag disabled returns default value

1. Caller invokes `AbExperiment.get` with a default value.
2. The `:ab_experiment_feed_strategy` feature flag is disabled.
3. The system skips the `field_test` call and any config override.
4. The default value is wrapped with `.inquiry` and returned immediately.

### Convenience method for feed strategy

1. Caller invokes `AbExperiment.get_feed_variant_for` with a controller and user.
2. The method delegates to `.get` using `CURRENT_FEED_STRATEGY_EXPERIMENT` and `ORIGINAL_VARIANT` as the default.
3. The resolved variant is returned as an inquirable string.

## Failures / Exceptions

- If `field_test` raises `FieldTest::ExperimentNotFound` (e.g., the experiment is not registered in `config/field_test.yml`), a warning is logged that includes the experiment name and the default value, and the default value is returned wrapped with `.inquiry`.
