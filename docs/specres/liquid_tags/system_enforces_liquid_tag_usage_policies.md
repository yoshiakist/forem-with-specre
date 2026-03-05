---
id: "01KJ1EZV154EB8MH5FS06CB6XT"
name: "system_enforces_liquid_tag_usage_policies"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/liquid_tag_base.rb`
- `app/policies/liquid_tag_policy.rb`
- `app/services/users/approved_liquid_tags.rb`
- `app/errors/liquid_tags.rb`
- `app/policies/authorizer.rb`
- `app/models/liquid_tags/user_subscription_tag.rb`
- `spec/liquid_tags/liquid_tag_base_spec.rb` (Test)
- `spec/policies/liquid_tag_policy_spec.rb` (Test)
- `spec/services/users/approved_liquid_tags_spec.rb` (Test)

## Functional Overview

When a liquid tag is parsed, the system enforces two layers of policy. First, `LiquidTagBase#initialize` validates the parse context against any `VALID_CONTEXTS` the tag declares, raising `LiquidTags::Errors::InvalidParseContext` if the source object is absent or of an unexpected type. Second, it invokes Pundit with `LiquidTagPolicy` to authorize the user: unrestricted tags (those returning `nil` from `user_authorization_method_name`) are always allowed, while restricted tags require a logged-in user who passes the tag's designated authorization method. The `Users::ApprovedLiquidTags` service provides a complementary query that returns the list of restricted tags a given user is permitted to use, driven by the same `user_authorization_method_name` mechanism. `LiquidTags::UserSubscriptionTag` is the sole restricted tag in the system and uses Rolify for role-based access via `Authorizer::RoleBasedQueries#user_subscription_tag_available?`.

## Design Intent

`LiquidTagPolicy` deliberately does not inherit from `ApplicationPolicy` because liquid tags do not follow the standard model/controller lifecycle that Pundit assumes. The `user_authorization_method_name` indirection keeps authorization logic on the user (via the Authorizer) rather than hard-coded inside each tag, making it easier to add new restricted tags without touching the policy. A `policy:` backdoor is threaded through `parse_context` to allow bulk re-rendering operations to bypass per-user checks when an administrative process is driving the render.

## Key Members

- `LiquidTagBase.user_authorization_method_name` — class-level hook; returns `nil` for unrestricted tags or a symbol naming the user method that gates access (e.g., `:user_subscription_tag_available?`).
- `VALID_CONTEXTS` — optional constant on a tag subclass; an array of class-name strings listing the source types in which the tag may appear.
- `Users::ApprovedLiquidTags::RESTRICTED_LIQUID_TAGS` — the canonical list of tags that require explicit authorization (`[UserSubscriptionTag]`).

## Scenarios

### Unrestricted tag is always permitted

1. A liquid tag's class returns `nil` from `user_authorization_method_name`.
2. During parsing, `LiquidTagBase#initialize` calls `LiquidTagPolicy#initialize?`.
3. The policy sees no authorization method name and returns `true` immediately, regardless of whether a user is present.

### Restricted tag is blocked when no user is present

1. A liquid tag's class returns a non-nil method name from `user_authorization_method_name`.
2. The parse context carries no user (e.g., anonymous render).
3. `LiquidTagPolicy#initialize?` raises `Pundit::NotAuthorizedError` with the message "No user found".

### Restricted tag is blocked when the user lacks the required role

1. A liquid tag's class returns a non-nil method name from `user_authorization_method_name`.
2. The parse context carries a user who returns `false` for that method.
3. `LiquidTagPolicy#initialize?` raises `Pundit::NotAuthorizedError` with the message "User is not permitted to use this liquid tag".

### Restricted tag is allowed when the user has the required role

1. A liquid tag's class returns a non-nil method name from `user_authorization_method_name`.
2. The parse context carries a user who returns `true` for that method.
3. `LiquidTagPolicy#initialize?` returns `true` and parsing proceeds normally.

### Tag is rejected when used in an invalid source context

1. A liquid tag subclass declares `VALID_CONTEXTS` listing only certain source types.
2. During parsing, the source object in the parse context is absent or its class name is not in `VALID_CONTEXTS`.
3. `LiquidTagBase#validate_contexts` raises `LiquidTags::Errors::InvalidParseContext` before authorization is attempted.

### Administrative backdoor bypasses per-user policy

1. A bulk render process supplies a custom `policy:` class in the parse context that always returns `true` from `initialize?`.
2. `LiquidTagBase#initialize` passes that policy class to Pundit instead of `LiquidTagPolicy`.
3. Authorization succeeds regardless of the user's role, allowing the tag to render in an administrative context.

## Failures / Exceptions

- `LiquidTags::Errors::InvalidParseContext` — raised when `VALID_CONTEXTS` is defined and the source object is missing or its type is not in the allowed list.
- `Pundit::NotAuthorizedError` ("No user found") — raised by `LiquidTagPolicy` when a restricted tag is parsed without an authenticated user.
- `Pundit::NotAuthorizedError` ("User is not permitted to use this liquid tag") — raised by `LiquidTagPolicy` when the user exists but fails the tag's authorization predicate.
