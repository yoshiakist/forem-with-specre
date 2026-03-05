---
id: "01KJXNAJ03071FX53KZT4JECAT"
name: "system_enforces_unique_slugs_across_models"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/validators/cross_model_slug_validator.rb`
- `app/models/cross_model_slug.rb`
- `app/models/concerns/unique_across_models.rb`
- `spec/validators/cross_model_slug_validator_spec.rb` (Test)

## Functional Overview

The system enforces that slug-like identifiers (usernames, slugs) are globally unique across all "slug-like" models — `User`, `Page`, `Podcast`, and `Organization` — because each slug maps to a top-level route (`/slug`). `CrossModelSlug` maintains the registry of those models and their identifier attributes, and exposes an `exists?` check that queries each model in turn. `CrossModelSlugValidator` is an `ActiveModel::EachValidator` that applies four rules in sequence: correct character format (with model-specific regex variants for `Organization` and `Page`), an allowed subdirectory depth limit for `Page` slugs, absence from a reserved-word list, and uniqueness across all registered models. The `UniqueAcrossModels` concern provides a concise class-level DSL (`unique_across_models :attribute`) that models use to wire in presence validation and this validator, running the cross-model check only when the attribute has changed.

## Design Intent

Because every slug resolves to the same URL namespace, a collision between a User username and an Organization slug would produce an ambiguous route. Centralizing the cross-model check in `CrossModelSlug::exists?` keeps query logic in one place and makes it easy to add new slug-bearing models to the registry. The `attribute_changed?` guard in both the concern and the validator avoids the expensive multi-model query on every save when the attribute is unchanged.

## Key Members

- `CrossModelSlug::MODELS` — frozen hash mapping model class names to their identifier attribute; currently covers `User` (`:username`), `Page` (`:slug`), `Podcast` (`:slug`), and `Organization` (`:slug`)
- `CrossModelSlugValidator::FORMAT_REGEX` — default allowlist regex for slugs (`[0-9a-z\-_]+`)
- `CrossModelSlugValidator::ORGANIZATION_FORMAT_REGEX` — variant that additionally rejects all-digit slugs
- `CrossModelSlugValidator::PAGE_FORMAT_REGEX` — variant that permits `/` and `+` for page path slugs
- `CrossModelSlugValidator::PAGE_DIRECTORY_LIMIT` — maximum number of `/`-separated segments allowed in a page slug (6)

## Scenarios

### Slug passes all validations

1. A model attribute that has just changed is submitted for validation.
2. The validator confirms the value matches the character-format regex for the model type.
3. If the model is a `Page`, the validator confirms the path has at most six slash-delimited segments.
4. The validator confirms the value does not appear in the reserved-word list (unless the model is a `Page`).
5. The validator queries `CrossModelSlug` and finds no matching record across any registered model.
6. No errors are added; the record is valid.

### Slug fails format check

1. A model attribute value contains a disallowed character (e.g., `+` for a non-Page model, or only digits for an Organization).
2. The validator detects the mismatch against the model-specific format regex.
3. An `is_invalid` error is added to the attribute and further checks are still run.

### Slug collides with a reserved word

1. A non-Page model submits a slug that appears in `ReservedWords.all`.
2. The validator adds an `is_reserved` error to the attribute.

### Slug already taken by another model's record

1. A model attribute value matches an existing record in one of the registered slug-bearing models (e.g., a `User` with that username).
2. `CrossModelSlug.exists?` returns truthy after querying each model in turn.
3. The validator adds an `is_taken` error to the attribute.

### Validation is skipped when attribute is unchanged

1. A record is saved but its slug attribute has not changed since last persistence.
2. The `attribute_changed?` guard in `UniqueAcrossModels` (and secondarily inside the validator) short-circuits before the cross-model query is executed.
3. No cross-model database queries are issued and no errors are added.

## Failures / Exceptions

- A slug containing `sitemap-` is treated as already existing by `CrossModelSlug.exists?`, so the validator will add an `is_taken` error regardless of actual database state.
- A `Page` slug is exempt from the reserved-word check, allowing page slugs to reuse otherwise reserved paths.
- A `Page` slug with more than six slash-separated segments receives a `too_many_subdirectories` error.
