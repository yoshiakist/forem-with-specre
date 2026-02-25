---
id: "01KJBH80DYJTW6BEDGTH8XC06C"
name: "visitor_can_view_user_profile_page"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/users_controller.rb`
- `app/controllers/stories_controller.rb`
- `app/models/user.rb`
- `app/decorators/user_decorator.rb`
- `app/helpers/users_helper.rb`
- `app/policies/user_policy.rb`
- `app/views/users/show.html.erb` (Template)
- `app/views/users/_sidebar.html.erb` (Template)
- `app/views/users/_metadata.html.erb` (Template)
- `app/views/users/_meta.html.erb` (Template)
- `app/views/users/_badges_area.html.erb` (Template)
- `app/views/users/_main_feed.html.erb` (Template)
- `app/views/users/_comments_section.html.erb` (Template)
- `app/views/users/_comments_locked_cta.html.erb` (Template)
- `spec/requests/user/user_show_spec.rb` (Test)
- `spec/decorators/user_decorator_spec.rb` (Test)
- `spec/views/users/main_feed_spec.rb` (Test)
- `spec/system/user/view_user_comments_spec.rb` (Test)
- `spec/system/user/view_user_index_spec.rb` (Test)

## Functional Overview

When a visitor (authenticated or anonymous) navigates to a user's profile URL (e.g., `/:username`), the system looks up the user by username, enforces visibility rules (returning 404 for unregistered or fully-banished users, and for suspended users with no published content when the visitor is not signed in), then renders a public-facing profile page. The page displays the user's avatar, display name, tagline, location, join date, optional email and website links, social account links, and earned badges. Below the header, a two-column layout presents a sidebar with activity stats (post count, comment count, followed tag count), organization memberships, featured GitHub repositories, and custom profile field values, alongside a main content area showing pinned articles, published articles, and a recent-comments section. For anonymous visitors outside of internal navigation, the page also injects a JSON-LD `Person` schema block for SEO. The `UserDecorator` supplies formatted display values, and profile data is cached with surrogate keys to support efficient CDN invalidation.

## Design Intent

The profile page uses the decorator pattern (`UserDecorator`, `ProfileDecorator`) to separate display-formatting logic from the model, keeping computed values such as `profile_email` and `profile_summary` out of the `User` model itself. Aggressive fragment caching (keyed by profile cache timestamps and badge counts) keeps rendering fast for high-traffic profiles while ensuring that updates to the profile, badges, or GitHub repositories invalidate only the relevant cache fragments. JSON-LD is emitted only for unauthenticated, non-internal-navigation requests because signed-in visitors and Turbo frame navigations do not need the structured-data block for SEO purposes.

## Scenarios

### Anonymous visitor views a public profile

1. Visitor navigates to `/:username` without being signed in.
2. System finds the user by username; returns 404 if the user is not registered, is fully banished (spam prefix + banned), or is suspended with no published content.
3. The page renders the profile header with avatar, name, tagline, location, join date, and any social/website links.
4. Earned badges appear in the header if the user has 7 or more badge achievements; otherwise badges appear in the sidebar (up to 6).
5. The main feed shows pinned articles followed by published articles; the comments section shows a locked call-to-action prompting the visitor to sign in to view comments.
6. A JSON-LD `Person` schema block is embedded in the page for search engine indexing.

### Authenticated visitor views another user's profile

1. Signed-in visitor navigates to `/:username`.
2. System renders the same profile header and article feed as for an anonymous visitor.
3. The comments section shows the profile user's recent comments (good-quality, non-deleted) rather than the locked call-to-action.
4. The page header action area shows "Follow" and a dropdown menu offering block, flag/unflag, and spam/unspam options.
5. JSON-LD is not rendered for signed-in requests.

### Visitor views a profile with no articles

1. Visitor navigates to the profile of a user who has no published articles and no comments.
2. If the current subforem is not the default subforem, the system redirects permanently to the user's profile on the default subforem.
3. If the subforem matches, the main content area is empty (neither article cards nor comment rows are shown).

### Visitor views the comments tab

1. Visitor navigates to `/:username/comments`.
2. If the visitor is signed in, the comments section is rendered directly showing all of the profile user's recent comments with links and timestamps.
3. If the visitor is not signed in, the locked call-to-action ("Want to connect with [name]?") is rendered instead of the comment list.

### System generates JSON-LD structured data for SEO

1. An anonymous visitor (not using internal navigation) loads a profile page.
2. The system builds a `schema.org/Person` object containing the user's name, profile URL, profile image, public email (if display-on-profile is enabled), tagline as description, and `sameAs` links for connected social accounts.
3. The JSON-LD block is embedded as an inline `<script type="application/ld+json">` in the page head area.
4. Blank or null fields are omitted from the output so that invalid empty properties are never emitted.

## Failures / Exceptions

- Unregistered user (`user.registered` is false): returns 404.
- Fully banished spam user (username prefixed with `spam_` and banned): returns 404.
- Suspended user with no published content, anonymous request: returns 404.
- Suspended user who still has published content: profile is rendered but search engines receive `noindex`/`nofollow` meta tags; same applies to users with a negative score.
- User not found by username: system attempts to redirect to the profile at the changed username; if no forwarding record exists, returns 404.
