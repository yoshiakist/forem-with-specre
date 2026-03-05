---
id: "01KJXTG35F6TPQJYNHA9TFPGAE"
name: "system_decorates_model_objects_for_view_presentation"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/decorators/application_decorator.rb`
- `app/models/application_record.rb`
- `app/errors/uninferrable_decorator_error.rb`
- `spec/decorators/application_decorator_spec.rb` (Test)

## Functional Overview

The system wraps model objects in decorator instances to provide view-presentation logic without polluting the model layer. `ApplicationRecord` instances can call `decorate` on themselves, which resolves the appropriate decorator class by inferring it from the model's name (e.g., `User` → `UserDecorator`) and returns a new `ApplicationDecorator` wrapping the original object. `ApplicationDecorator` delegates unknown messages to the underlying object, exposes the wrapped object via `#object`, and provides convenience methods such as `#decorated?`, `#decorate` (returns self to avoid re-wrapping), `#type_identifier`, and `#class_name` delegation. Collections can be decorated in bulk via `ApplicationDecorator.decorate_collection` or the class-level `ApplicationRecord.decorate` shortcut.

## Design Intent

Decorator inference is intentionally name-based so that no registration or configuration is required — a `FooDecorator` class is automatically picked up for any `Foo` model. The `#decorate` no-op on an already-decorated object prevents double-wrapping and avoids the cost of re-resolving the decorator class. `delegate_missing_to :@object` keeps the decorator transparent to callers, so views can call any model method without the decorator needing explicit forwarding code.

## Key Members

- `@object` — the raw model record being wrapped; exposed as `#object`
- `decorator_class` (class method on `ApplicationRecord`) — walks the inheritance chain to find a matching `*Decorator` constant; raises `UninferrableDecoratorError` if none is found

## Scenarios

### Decorating a single model instance

1. A view or controller calls `#decorate` on an `ApplicationRecord` instance.
2. The model resolves its decorator class by appending `"Decorator"` to its model name.
3. The resolved decorator class is instantiated with the model object as the argument.
4. The caller receives a decorator that transparently forwards any unrecognised messages to the original model.

### Checking whether an object is decorated

1. A caller asks `#decorated?` on any object in the system.
2. An undecorated `ApplicationRecord` returns `false`.
3. An `ApplicationDecorator` instance returns `true`.

### Re-decorating an already-decorated object (no-op)

1. A caller calls `#decorate` on an `ApplicationDecorator` instance.
2. The decorator returns itself immediately without creating a new wrapper.
3. Object identity is preserved — the returned object is the same instance.

### Decorating a collection

1. A caller invokes `ApplicationDecorator.decorate_collection` with an array or ActiveRecord relation.
2. The system maps each record through its own `#decorate` call.
3. The caller receives an array where every element is a decorator wrapping the corresponding original record.

### Identifying a decorated object by type

1. A caller asks for `#type_identifier` on a decorator.
2. The decorator returns the downcased class name of the underlying model (e.g., `"article"`, `"user"`).

## Failures / Exceptions

- `UninferrableDecoratorError` (subclass of `NameError`) — raised by `ApplicationRecord.decorator_class` when no matching `*Decorator` constant can be found anywhere in the model's inheritance chain.
