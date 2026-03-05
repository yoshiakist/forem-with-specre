---
id: "01KJ6FAFV9D47QGGRY76KPKNC4"
name: "user_can_view_badges"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/badges_controller.rb`
- `app/models/badge.rb`
- `app/views/badges/index.html.erb` (Template)
- `app/views/badges/_badge_detail.html.erb` (Template)
- `spec/requests/badges_spec.rb` (Test)
- `spec/models/badge_spec.rb` (Test)

## Functional Overview

The badges feature allows any visitor — authenticated or not — to browse the full list of awarded badges. The `BadgesController` is entirely public; it loads all badges ordered by creation date and, for signed-in users, also fetches their earned badge IDs so the view can highlight which badges the current user holds. Each badge can also be viewed individually via a slug-based URL, with HTTP surrogate key headers set for CDN caching. The `Badge` model stores a title, description, image, and an auto-generated URL-safe slug derived from the title.

## Key Members

- `Badge#slug` — URL-safe identifier auto-generated from the title via `generate_slug`; used as the route parameter for the show action
- `Badge#allow_multiple_awards` — boolean flag indicating whether the same badge can be awarded more than once to a user
- `Badge#bonus_weight` — non-negative integer used for ranking or ordering purposes

## Scenarios

### Visitor browses all badges (unauthenticated)

1. A visitor navigates to the badges index page without being signed in.
2. The system loads all badges ordered by their creation date.
3. The page renders with all badge images and titles visible.
4. No earned-badge highlights are shown because no user session exists.

### Authenticated user browses all badges

1. A signed-in user navigates to the badges index page.
2. The system loads all badges ordered by creation date.
3. The system also fetches the IDs of badges the current user has earned.
4. The page renders all badges and visually distinguishes the ones the user has already earned.

### User views a single badge by slug

1. A visitor requests the show page for a badge using its slug in the URL.
2. The system looks up the badge by slug.
3. If found, the badge detail page is rendered with CDN surrogate key headers set.
4. If no badge matches the slug, the system responds with a not-found page.

## Failures / Exceptions

- If the slug provided to the show action does not match any badge, the controller calls `not_found`, which renders a 404 response.
