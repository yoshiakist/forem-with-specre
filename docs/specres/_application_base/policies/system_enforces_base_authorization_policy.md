---
id: "01KJVS451ZBWV9SF8NRH3B9HVZ"
name: "system_enforces_base_authorization_policy"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/policies/application_policy.rb`
- `spec/policies/application_policy_spec.rb` (Test)
- `spec/policies/shared_examples/authorization_shared_examples.rb` (Test)

## Functional Overview

`ApplicationPolicy` is the abstract base class for all Pundit-based authorization policies in the application. It establishes a secure default-deny posture: every standard action (`index?`, `show?`, `create?`, `new?`, `update?`, `edit?`, `destroy?`) returns false unless a subclass overrides it. Initialization stores the requesting user and target record, and immediately enforces that a user is present by calling `require_user!`. The class defines three application-specific error classes (`NotAuthorizedError`, `UserSuspendedError`, `UserRequiredError`) that form a hierarchy rooted at `Pundit::NotAuthorizedError`, allowing callers to rescue at the level of granularity they need. Class-level guard methods (`require_user!`, `require_user_in_good_standing!`) are exposed so that controllers, services, and other non-policy contexts can invoke the same authentication checks without instantiating a policy. A utility method (`dom_classes_for`) generates consistent CSS class strings for policy-aware HTML elements, optionally appending "hidden" when a policy subclass signals that an element should be concealed.

## Design Intent

All authorization logic is intended to flow through policies rather than being scattered across controllers and views with direct role checks such as `user.admin?`. The abstract base enforces this discipline by denying everything by default, requiring subclasses to explicitly grant access. Making `require_user!` and `require_user_in_good_standing!` class methods (rather than instance-only) allows shared usage before a full policy object is constructed, which supports gradual migration of ad-hoc auth checks to the policy layer.

## Key Members

- `@user` — the requesting user; may be nil only before `require_user!` raises
- `@record` — the resource being acted upon; a model class, instance, or PORO
- `Scope` inner class — wraps a relation and enforces user presence; `resolve` returns the full scope by default

## Scenarios

### Default denial of all actions

1. A policy subclass is instantiated with a valid user and a record.
2. None of the standard action predicates (`index?`, `create?`, `update?`, `destroy?`) are overridden.
3. Each predicate returns false, denying access.

### Enforcement of authenticated user on instantiation

1. A policy is instantiated with `nil` as the user.
2. The initializer calls `require_user!`, which raises `ApplicationPolicy::UserRequiredError`.
3. The caller receives the error and handles the unauthenticated case.

### Enforcement of a user in good standing

1. `require_user_in_good_standing!` is called with a suspended user.
2. The method first confirms a user is present, then checks suspension status.
3. Because the user is suspended, it raises `ApplicationPolicy::UserSuspendedError`.

### Generating DOM classes for policy-aware elements

1. A view calls `ApplicationPolicy.dom_classes_for(record: record, query: query)`.
2. The method builds a base CSS class string from the record type, optional record id, and query name.
3. If the corresponding policy class reports that the element should be hidden, `"hidden"` is appended to the class string.
4. The combined class string is returned and applied to the HTML element.

## Failures / Exceptions

- `ApplicationPolicy::UserRequiredError` (< `NotAuthorizedError` < `Pundit::NotAuthorizedError`) — raised when no user is present and an authenticated user is required.
- `ApplicationPolicy::UserSuspendedError` (< `NotAuthorizedError`) — raised when the user is suspended and a user in good standing is required.
- `Pundit::NotAuthorizedError` — raised by the `Scope` initializer directly when no user is provided to a scope resolution.
