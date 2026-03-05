---
id: "01KJXRY1N0DJQ23E3CMV1QHZNC"
name: "system_toggles_feature_flags_via_test_api"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/controllers/concerns/api/feature_flags_controller.rb`
- `app/controllers/api/v0/feature_flags_controller.rb`
- `app/controllers/api/v1/feature_flags_controller.rb`
- `app/services/feature_flag.rb`
- `spec/requests/api/v0/feature_flags_spec.rb` (Test)
- `spec/requests/api/v1/feature_flags_spec.rb` (Test)

## Functional Overview

The system exposes a test-only HTTP API for toggling Flipper-backed feature flags, enabling automated test suites (such as Cypress) to enable or disable named flags as part of their setup. Both API v0 and v1 share the same concern-based implementation: a `POST` to the feature flags endpoint enables the named flag, a `DELETE` disables it, and a `GET` returns the current enabled state as JSON. The endpoints are only available in non-production environments; routing raises an error in production. The underlying operations are delegated to the `FeatureFlag` service module, which wraps the Flipper gem.

## Design Intent

The controller uses `create` / `destroy` / `show` actions mapped to enable, disable, and query semantics respectively, rather than a single toggle action with a boolean parameter. This avoids conditional logic and type-casting in the controller. The concern module (`Api::FeatureFlagsController`) is included by both the v0 and v1 versioned controllers, keeping the implementation DRY across API versions.

## Scenarios

### Enabling a feature flag via the API

1. A test client sends a `POST` request to the feature flags endpoint with a `flag` parameter naming the target flag.
2. The system calls `FeatureFlag.enable` with the given flag name.
3. The system responds with HTTP 200 OK and no body.
4. Subsequent checks confirm the flag is now enabled.

### Disabling a feature flag via the API

1. A test client sends a `DELETE` request to the feature flags endpoint with a `flag` parameter naming the target flag.
2. The system calls `FeatureFlag.disable` with the given flag name.
3. The system responds with HTTP 200 OK and no body.
4. Subsequent checks confirm the flag is now disabled.

### Querying the current state of a feature flag

1. A test client sends a `GET` request to the feature flags endpoint with a `flag` parameter.
2. The system looks up the enabled state of the named flag via `FeatureFlag.enabled?`.
3. The system responds with a JSON object mapping the flag name to its boolean state (e.g., `{ "test_flag": true }`).

### Endpoint is unavailable in production

1. The Rails environment is set to production.
2. A test client attempts to send any request to the feature flags endpoint.
3. The routing layer raises `ActionController::RoutingError` — the endpoint does not exist in production routes.
