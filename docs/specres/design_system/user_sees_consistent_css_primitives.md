---
id: "01KJXZV2J4CC6YX6MZRPB6VSFN"
name: "user_sees_consistent_css_primitives"
status: "draft"
---

## Related Files

- `app/javascript/crayons/avatarsAndLogos/Avatar/__stories__/avatars.html.stories.jsx`
- `app/javascript/crayons/avatarsAndLogos/Logo/__stories__/logos.html.stories.jsx`
- `app/javascript/crayons/formElements/Checkbox/__stories__/checkbox.html.stories.jsx`
- `app/javascript/crayons/formElements/Select/__stories__/Select.stories.jsx`
- `app/javascript/crayons/formElements/Text/__stories__/text.html.stories.jsx`
- `app/javascript/crayons/formElements/Text/__stories__/multilineText.html.stories.jsx`
- `app/javascript/crayons/navigation/NavigationTabs/__stories__/navigationTab.html.stories.jsx`
- `app/javascript/crayons/Notice/__stories__/notice.html.stories.jsx`
- `app/javascript/crayons/typography/__stories__/typography.stories.jsx`
- `app/javascript/crayons/typography/__stories__/typographyAccented.stories.jsx`

## Functional Overview

The crayons design system exposes a set of CSS-only UI primitives — avatars, logos, form elements (checkbox, select, text, multiline text), navigation tabs, notices, and typography — that have no JSX implementation files of their own. Each primitive is applied purely through `crayons-*` CSS class names (e.g., `crayons-avatar`, `crayons-checkbox`, `crayons-tabs__item`, `fs-base`, `fw-bold`) added directly to HTML or JSX markup. These primitives are documented through Storybook HTML stories, which serve as both visual reference and living contract for consistent presentation across the application; any element that carries the correct class names will automatically inherit the design system's color, spacing, sizing, and typography tokens.

## Design Intent

The CSS-only approach is intentional: primitives carry no JavaScript runtime overhead and impose no component abstraction. Consumers apply styling by adding class names to native HTML elements, which keeps the primitives composable, framework-agnostic, and testable in isolation via Storybook without requiring a React or Preact component tree. Modifier classes follow a BEM-inspired convention (block, block--modifier, block__element) so visual variants (size, state, weight) are expressed through additive class composition rather than prop drilling or runtime logic.

## Scenarios

### User sees correctly sized avatars and logos

1. An image element is wrapped in a `<span>` with the `crayons-avatar` class and optionally a size modifier such as `crayons-avatar--l`, `crayons-avatar--xl`, `crayons-avatar--2xl`, or `crayons-avatar--3xl`.
2. The inner image carries the `crayons-avatar__image` class.
3. The avatar renders at the expected dimensions and shape defined by the design token for that size, with no additional JavaScript required.

### User sees consistent form element styling

1. A checkbox input carries the `crayons-checkbox` class; it renders with the design system's custom checkbox appearance in default, checked, and disabled states.
2. When wrapped in a `<div class="crayons-field crayons-field--checkbox">` alongside a `<label class="crayons-field__label">`, the label and optional description text align correctly with the control.
3. A select or text input carries the appropriate `crayons-select` or `crayons-textfield` class and inherits border, padding, focus ring, and disabled styling from the design system without any JS intervention.

### User sees tab navigation highlight the active item

1. A `<nav>` element carries the `crayons-tabs` class and contains a `<ul class="crayons-tabs__list">` with individual tab links or buttons.
2. The active tab link or button carries `crayons-tabs__item--current` in addition to `crayons-tabs__item`.
3. The active tab is visually distinguished (underline, color) purely through CSS applied to that modifier class; no JavaScript is needed to apply the style, only to toggle the class in response to user interaction.

### User sees typographically consistent text across the interface

1. Any element carrying a font-size utility class such as `fs-xs`, `fs-base`, `fs-2xl`, or `fs-5xl` renders at the corresponding size defined by the design token scale.
2. Weight utilities (`fw-medium`, `fw-bold`, `fw-heavy`) and line-height utilities (`lh-tight`, `lh-base`) compose additively on the same element without conflict.
3. Accented typography variants and monospace utilities follow the same additive class pattern, giving the full typographic system consistent visual rhythm.
