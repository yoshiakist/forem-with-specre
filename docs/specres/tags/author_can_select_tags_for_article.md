---
id: "01KJ41F3K1B3SRQ2HBYFY2N2M4"
name: "author_can_select_tags_for_article"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/javascript/hooks/useTagsField.js`
- `app/javascript/article-form/components/TagsField.jsx`
- `app/javascript/article-form/components/Help/TagInput.jsx`
- `app/javascript/crayons/MultiSelectAutocomplete/TagAutocompleteOption.jsx`
- `app/javascript/crayons/MultiSelectAutocomplete/TagAutocompleteSelection.jsx`
- `app/models/concerns/taggable.rb`
- `app/lib/acts_as_taggable_on/tag_parser.rb`
- `spec/models/shared_examples/taggable_spec.rb` (Test)
- `spec/lib/acts_as_taggable_on/tag_parser_spec.rb` (Test)

## Functional Overview

When composing an article, an author can search for and select up to four tags using a multi-select autocomplete field. As the author types, the field queries either Algolia or an internal search endpoint (chosen based on site configuration) and displays matching tag suggestions with their name, optional background color, short summary, and badge image. Previously selected tags are pre-populated on load by fetching enriched tag data for each saved tag name. Each selected tag is displayed as a removable chip that can also be edited inline. On the server side, raw tag input is cleaned by lowercasing, stripping spaces and non-alphanumeric characters, and resolving any tag aliases to their canonical name before the tag list is stored. The `Taggable` concern on taggable models provides scopes for querying records by their cached tag list.

## Design Intent

The hook `useTagsField` decouples search-backend selection (Algolia vs. internal `fetchSearch`) from the UI component, determined at runtime from `document.body.dataset.algoliaId`. This lets the same tag-selection UI work in both Algolia-enabled and Algolia-free deployments without any branching in the component layer. Tag aliases are resolved server-side so that canonical tag names are always stored, regardless of which alias the author typed.

## Key Members

- `maxSelections: 4` — the field enforces a hard cap of four tags per article
- `allowUserDefinedSelections: true` — authors may type a tag name that does not yet exist in the search results
- `defaultValue: string` — comma-separated tag names passed in as the initial state; enriched with full tag data on first mount
- `syncSelections` — converts the array of selected tag objects back to a comma-separated string and calls `onInput` to propagate changes to the article form state
- `TagParser#clean` — lowercases, removes spaces, and strips all non-alphanumeric characters from each tag string before storage

## Scenarios

### Selecting tags from autocomplete suggestions

1. The author focuses the tags field in the article form.
2. The field fetches a list of top tags from `/tags/suggest` and displays them as static suggestions.
3. The author types a search term; the field queries Algolia (or the internal search API) and displays matching tags, each showing the tag name, optional badge image, and short summary.
4. The author clicks or keyboards to a suggestion; it is added as a selected chip with its background color applied.
5. Once four tags are selected, the input no longer accepts additional selections.

### Pre-populating tags when editing an existing article

1. The article form mounts with a `defaultValue` string containing the existing comma-separated tag names.
2. On first mount, `useTagsField` splits the string and issues a search request for each tag name.
3. For each tag, if the search result's name matches exactly, the full tag object (including color and badge) is used; otherwise a minimal object with only the name is used.
4. The resolved tag objects are set as the initial selections, displaying enriched chips immediately.

### Removing or editing a selected tag

1. Each selected tag chip renders an edit button and a remove button.
2. Clicking the remove button calls `onDeselect`, which removes the tag from the selections array.
3. Clicking the edit button calls `onEdit`, allowing the author to modify the tag name inline.
4. After any change, `syncSelections` converts the remaining selections to a comma-separated string and fires `onInput` to keep the article form state current.

### Parsing and cleaning tags on the server

1. When the article is saved, the raw tag list string is passed to `ActsAsTaggableOn::TagParser#parse`.
2. The parser lowercases the entire string, splits on commas, strips surrounding whitespace, removes internal spaces, and strips all non-alphanumeric characters from each token.
3. Each cleaned tag is then checked for a known alias; if found, the alias chain is followed until the canonical tag name is reached.
4. The resulting canonical tag list is stored on the article.

### Validating tag names on the model

1. Before saving, `Taggable#validate_tag_name` is called with the tag list.
2. For each tag, a `Tag` instance is constructed and its name validation is run.
3. Any validation error on the tag name is propagated to the article model's errors under the `:tag` key with the offending tag name quoted.

## Failures / Exceptions

- If an author's tag input string is blank, `TagParser#clean` returns an empty array and no tags are stored.
- If a tag name matches no search result exactly, `useTagsField` falls back to a minimal tag object containing only the name, preventing a broken chip from blocking pre-population.
- `Taggable#cached_tagged_with` raises `TypeError` if passed an argument that is not a `String`, `Symbol`, `Array`, or `Tag` object.
- `Taggable#cached_tagged_with_any` raises `TypeError` under the same unsupported-type conditions.
