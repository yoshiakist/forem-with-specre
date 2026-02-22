---
id: "01KJ1F647GSC84NJAD0YRSHSFB"
name: "author_can_embed_user_profile_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/user_tag.rb`
- `app/views/users/_liquid.html.erb` (Template)
- `spec/liquid_tags/user_tag_spec.rb` (Test)

## Functional Overview

Authors can embed a user profile card inline within an article by writing a `{% user username %}` Liquid tag. When the article is rendered, the tag is replaced with a styled profile card showing the user's avatar, display name, tagline, and a follow button. If the username resolves to a registered user, the card links to that user's profile page. If the username does not match any registered user, the tag renders a placeholder "deleted user" card instead of raising an error.

## Design Intent

By delegating rendering to a Rails partial (`users/liquid`), the tag keeps logic and markup cleanly separated. The `UserTag` strips any leading site URL from the input so that authors may paste a full profile URL rather than just a bare username. Falling back to `Users::DeletedUser` when no match is found makes the behavior safe for articles that reference accounts deleted after publication.

## Key Members

- `PARTIAL` — the Rails partial path (`"users/liquid"`) used to render the profile card HTML
- `@user` — the resolved `User` record (or the `Users::DeletedUser` sentinel when not found)
- `@user_colors` — computed color values derived from the user's profile, passed to the partial for branded border/shadow styling
- `user_path` — the user's profile URL; when blank (deleted user), the card omits anchor links

## Scenarios

### Embedding a valid user by username

1. Author writes `{% user alice %}` inside an article body.
2. The tag strips any leading site URL from the input and looks up a registered user with username `alice`.
3. A profile card is rendered containing Alice's avatar image, display name, tagline, and a follow button.
4. The avatar and name are wrapped in links pointing to Alice's profile page.

### Embedding a valid user by full profile URL

1. Author writes `{% user https://example.com/alice %}` inside an article body.
2. The tag strips the site URL prefix, reducing the input to `alice`, then resolves the user as above.
3. The rendered output is identical to embedding by bare username.

### Embedding a non-existent or deleted username

1. Author writes `{% user nonexistent_person %}` inside an article body.
2. The tag finds no registered user matching that username.
3. A placeholder card is rendered using the `Users::DeletedUser` sentinel, displaying `[deleted user]` as the username and `[Deleted User]` as the display name.
4. No error is raised; the article renders normally.

## Failures / Exceptions

- If the username contains spaces, those spaces are removed before lookup, so `{% user john doe %}` becomes a lookup for `johndoe`.
- The fallback to `Users::DeletedUser` is the only error path; no exception is surfaced to the author or reader when a user is not found.
