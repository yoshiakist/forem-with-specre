---
id: "01KHYAE6BT4N3QJ2FR396TTRCQ"
name: "organization_decorator_enriches_color_presentation"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/organization_decorator.rb
- spec/decorators/organization_decorator_spec.rb (Test)

## Functional Overview

The OrganizationDecorator enriches Organization instances with presentation logic for color theme management, providing fallback colors when custom brand colors are absent, brightness-adjusted darker color variants for UI contrast, and a stub for the banishment check interface.

## Scenarios

### Decorator provides enriched colors with fallbacks

1. If the organization has a custom `bg_color_hex`, the system uses it as the background color.
2. If the organization has a custom `text_color_hex`, the system uses it; otherwise it falls back to the default white (#ffffff).
3. If `bg_color_hex` is blank, the system returns default colors: background #0a0a0a (near-black) and text #ffffff (white).

### Decorator computes darker color for contrast

1. The `darker_color` method applies a brightness adjustment (default 0.88) to the background and text colors using `Color::CompareHex`.
2. A lower adjustment factor produces a darker result; a factor above 1.0 produces a lighter result.
3. When no custom colors are set, the adjustment is applied to the default assigned colors.

### Decorator reports banishment status

1. `fully_banished?` always returns false, as organization banning is not currently implemented.

### Decorator supports serialization

1. Decorated organizations can be serialized with both model attributes and decorator methods via `as_json`.
2. Decorated collections also serialize correctly.
