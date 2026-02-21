---
id: "01KHZKCR70BAFQ159BEQFXBJQW"
name: "user_can_view_survey"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/surveys_controller.rb`
- `app/models/survey.rb`
- `app/views/surveys/show.html.erb` (Template)
- `spec/controllers/surveys_controller_spec.rb` (Test)
- `spec/requests/surveys_spec.rb` (Test)
- `spec/factories/surveys.rb` (Test)

## Functional Overview

When a visitor requests a survey page by slug, the system looks up the survey first by its current slug, then by its historical `old_slug` and `old_old_slug` fields to support past URLs. If the survey is found under a stale slug, the visitor is permanently redirected to the canonical current-slug URL. If the survey is found but marked inactive, or if no survey matches the slug at all, the system renders a 404 response. For a valid, active survey the controller loads the associated polls with their options in display order and renders the show template, which delegates presentation to a liquid partial and injects the `SurveyTag` JavaScript bundle.

## Design Intent

Slug history (`old_slug`, `old_old_slug`) is preserved so that previously published survey links remain functional after a title change. Redirecting stale slugs with HTTP 301 keeps external links valid while consolidating canonical traffic to the current URL. Slugs are generated automatically on creation from the title plus a short random hex suffix to guarantee uniqueness without requiring the author to choose one manually.

## Key Members

- `slug` — URL-friendly identifier derived from the survey title at creation time; must be unique
- `old_slug` / `old_old_slug` — previous slug values retained across up to two renames for redirect support
- `active` — boolean flag; only active surveys are publicly accessible via the show action
- `polls` — ordered collection of questions belonging to the survey, eager-loaded with their options on the show action

## Scenarios

### Viewing an active survey by its current slug

1. A visitor requests `/surveys/:slug` with the survey's current slug.
2. The system finds the survey by `slug` and confirms it is active.
3. The controller loads the survey's polls in position order, each with its options.
4. The show template renders, embedding the survey liquid partial and the `SurveyTag` script.

### Accessing a survey through an old slug (permanent redirect)

1. A visitor requests `/surveys/:slug` using a slug that was previously assigned to the survey but has since been changed.
2. The system fails to find an active survey by the current slug, then matches the survey by `old_slug` or `old_old_slug`.
3. Because the matched slug differs from the survey's current slug, the system responds with HTTP 301 and redirects to the canonical URL using the current slug.

### Requesting an inactive survey

1. A visitor requests `/surveys/:slug` for a survey whose `active` flag is `false`.
2. The system finds the survey record but raises `ActiveRecord::RecordNotFound` because it is not active.
3. The system renders `public/404.html` with HTTP 404 and no layout.

### Requesting an unknown slug

1. A visitor requests `/surveys/:slug` with a slug that does not match any survey (current or historical).
2. The system raises `ActiveRecord::RecordNotFound`.
3. The system renders `public/404.html` with HTTP 404 and no layout.

## Failures / Exceptions

- `ActiveRecord::RecordNotFound` is raised when no survey matches the slug or when the matched survey is inactive; the controller-level `rescue_from` handler renders `public/404.html` with status 404 and no application layout.
