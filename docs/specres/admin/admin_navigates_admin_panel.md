---
id: "01KJ9GWMJV27RNX4KT7WT0MQXS"
name: "admin_navigates_admin_panel"
status: "stable"
last_verified: "2026-02-25"
---

## Related Files

- `app/models/admin_menu.rb`
- `app/helpers/admin_helper.rb`
- `app/helpers/admin/sidebar_helper.rb`
- `app/javascript/admin/controllers/sidebar_controller.js`
- `app/views/layouts/admin.html.erb` (Template)
- `app/views/admin/shared/_nested_sidebar.html.erb` (Template)
- `app/views/admin/shared/_navbar.html.erb` (Template)
- `app/views/admin/shared/_tabbed_navbar.html.erb` (Template)
- `spec/models/admin_menu_spec.rb` (Test)
- `spec/requests/admin/nested_sidebar_spec.rb` (Test)

## Functional Overview

The admin panel provides a hierarchical sidebar navigation organized into named scopes (Member Manager, Content Manager, Customization, Admin Team, Moderation, Advanced, and Apps). Each scope groups related items under a top-level link with an icon. Scopes with multiple children render an expandable sub-list, while scopes with a single child navigate directly to that child. When a nested route is active, the layout also renders a tabbed secondary navbar at the top of the main content area, derived from the current request path. The active sidebar item and active tab are visually distinguished using aria-current and CSS modifier classes. Feature-flagged items (such as Data Update Scripts) are conditionally included based on runtime flag evaluation.

## Design Intent

The menu structure is defined declaratively in code via `AdminMenu::ITEMS` (a PORO, not a database-backed model), using `Menu.define` with `scope` and `item` DSL calls. This ensures the navigation is deterministic, version-controlled, and renderable without any database queries. Nested grandchild items (tabs) are resolved at render time from the request path, keeping URL conventions as the single source of truth for active state.

## Key Members

- `AdminMenu::ITEMS` — a frozen hash of `Menu::Scope` objects keyed by scope name symbol, defined at class load time
- `Menu::Scope` — represents a top-level sidebar group with an icon (svg), a children list, and `has_multiple_children?` / `has_children?` predicates
- `Menu::Item` — represents one navigation entry with `name`, `controller`, `parent`, `visible`, and optional `children`
- `AdminHelper#deduced_scope(request)` — extracts the third path segment (e.g. `content_manager`) to identify the active scope
- `AdminHelper#deduced_controller(request)` — extracts the fourth path segment to identify the active controller
- `Admin::SidebarHelper#sidebar_item_active?(item)` — returns true when the item's controller matches the currently active controller, resolving through `AdminMenu.nested_menu_items` for grandchild routes
- `SidebarController` (Stimulus) — on page load, disables the currently-active nav button in expanded dropdowns; on dropdown expand, closes all other open submenus

## Scenarios

### Admin views sidebar with grouped navigation sections

1. An authenticated admin loads any admin page.
2. The layout renders the left sidebar using `AdminMenu.navigation_items`, which returns all defined scopes.
3. Each scope appears as a top-level link with its icon and display name (e.g. "Member Manager", "Content Manager").
4. Scopes with multiple children display a collapsed sub-list beneath the top-level link.

### Admin clicks a scope to expand nested sub-items

1. The admin is on a page whose URL scope matches a group that has multiple children (e.g. Member Manager at `/admin/member_manager/users`).
2. The sidebar detects the current scope via `deduced_scope` and renders the sub-list as visible (`block`) for the matching group.
3. Each child item is shown as a link; the item whose controller matches `deduced_controller` is marked `aria-current="page"`.
4. The Stimulus `SidebarController` disables the currently-active nav button on page load to prevent redundant clicks.

### Admin navigates to a tabbed sub-section

1. The admin navigates to a nested route such as `/admin/content_manager/badge_achievements`.
2. The layout detects that the path has a depth of three segments under `/admin` and calls `AdminMenu.nested_menu_items_from_request` to find the matching parent item.
3. If the resolved item has children (e.g. the "badges" item with "Library" and "Achievements" tabs), the tabbed navbar is rendered above the main content.
4. Each visible child is shown as a tab link; the tab whose controller matches `deduced_controller` receives the `crayons-tabs__item--current` class.

### Active item is visually highlighted

1. On every admin page load, `AdminHelper#current?` compares the current scope slug to each group's first child's parent (or the group name itself) to decide which top-level link is active.
2. The active top-level link receives the `c-link--current` CSS class and `aria-current="page"` (when the scope has only one child).
3. Within an expanded sub-list, `Admin::SidebarHelper#sidebar_item_active?` compares the resolved controller name to each item's controller, marking the matching item with `aria-current="page"`.

### Feature-flagged item is conditionally displayed

1. An item defined with a `visible` lambda (e.g. "Data Update Scripts" gated on `:data_update_scripts`) is evaluated at render time.
2. When the feature flag is disabled, the item is excluded from the tabbed navbar and is not present in the response body.
3. When the feature flag is enabled, the item appears as a tab in the navbar.

## Failures / Exceptions

- If the request path has fewer than four segments (e.g. `/admin`), `deduced_controller` returns nil and no sidebar item is marked active beyond the top-level overview link.
- If `nested_menu_items_from_request` finds no matching item for the path (e.g. `/admin/moderation/feedback_messages` which has no sub-items), the tabbed navbar is not rendered.
- Items whose `visible` lambda evaluates to false are hidden from the sidebar and tabbed navbar without raising errors.
