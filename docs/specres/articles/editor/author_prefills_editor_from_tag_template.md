---
id: "01KJV0FGPPG85X74PBP40BXG5N"
name: "author_prefills_editor_from_tag_template"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/services/articles/builder.rb`
- `app/controllers/articles_controller.rb`
- `app/models/article.rb`
- `spec/services/articles/builder_spec.rb` (Test)

## Functional Overview

When a user navigates to `/new?template=<tag_name>` or `/new?prefill=<markdown>`, `Articles::Builder` detects the `tag` or `prefill` parameter. For a tag with a submission template and a logged-in v2 user, `Builder#tag_user_editor_v2` creates an `Article` pre-populated with the tag's `submission_template_customized` output (splitting on `---` to extract `title:`, body, and sets `cached_tag_list` to the tag name), and returns `needs_authorization?: true`. For a plain prefill string with a v2 user, `Builder#prefill_user_editor_v2` parses `title:` and `tags:` headers from the markdown. The controller then calls `authorize(Article)` via Pundit before rendering the editor. Third-party sites can deep-link authors into the editor with pre-populated content using these query parameters.

## Design Intent

The tag template feature lets communities (e.g., hackathons, challenge series) guide authors to produce consistently formatted posts, analogous to what StackOverflow and CodePen offer. Pundit authorization is required in this path because the template may be restricted to specific users.

## Key Members

- `Articles::Builder#tag_user_editor_v2` — populates `body_markdown`, `cached_tag_list`, `title` from `tag.submission_template_customized(user.name)`
- `Articles::Builder#prefill_user_editor_v2` — populates `body_markdown`, `cached_tag_list`, `title` by parsing `prefill` markdown headers
- `Articles::Builder#normalized_text(source, split_pattern)` — extracts a single-line value after a `key:` marker in front-matter

## Scenarios

### Author opens /new?template=<tag_name> (v2 editor)

1. Logged-in v2 user navigates to `/new?template=some_tag`.
2. `Builder` finds the tag and calls `tag_user_editor_v2`.
3. `submission_template_customized` fills in the tag's template with the user's name.
4. `Builder` returns `[article, true]`; controller calls `authorize(Article)`.
5. Editor renders with `body_markdown`, `title`, and `cached_tag_list` pre-filled from the template.

### Author opens /new?prefill=<markdown> (v2 editor)

1. Logged-in v2 user follows an external deep-link with a `?prefill=` query param.
2. `Builder` calls `prefill_user_editor_v2`, parsing `title:` and `tags:` from the markdown.
3. Editor renders with `title`, `tagList`, and `bodyMarkdown` pre-filled.

## Failures / Exceptions

- If the tag does not exist or has no `submission_template`, `Builder` falls through to the standard `user_editor_v2` path (no prefill).
- Pundit authorization failure (e.g., the user lacks permission) returns HTTP 403.
