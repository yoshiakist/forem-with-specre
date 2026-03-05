---
id: "01KJV76MT6VG17M3KM7NJQ6T52"
name: "author_selects_series_for_article_in_editor"
status: "draft"
---

## Related Files

- `app/javascript/article-form/components/SeriesSelector.jsx`
- `app/javascript/article-form/components/SeriesSelectorModal.jsx`
- `app/javascript/article-form/components/Options.jsx`
- `app/javascript/article-form/articleForm.jsx`
- `app/javascript/article-form/components/__tests__/Options.test.jsx` (Test)

## Functional Overview

When authoring an article, the author can assign it to a series from the Advanced Post Options panel. The `SeriesSelector` component renders a card-style grid of available series filtered by the currently selected organization: personal series are always shown, and organization series are shown only when the matching organization is active. The author may select an existing series from the grid, or open an inline creation form to name and submit a new series. The component monitors changes to `currentSeries` and `allSeries` to detect when a newly created series has been persisted, and automatically dismisses the creation form at that point. A "Remove series" action clears the selection. The `Options` panel controls the show/hide state of the creation form so that the modal remains open during the create flow. The `SeriesSelectorModal` variant provides the same capabilities inside a standalone modal overlay that closes upon selection or creation.

## Design Intent

The component supports both controlled and uncontrolled modes for the "show create form" toggle. When hosted inside `Options`, the controlled mode is used so that `Options` can reset the create-form state when its own modal closes, preventing stale UI across modal open/close cycles. The async-confirmation pattern (storing a `pendingSeriesName` and watching for it to appear in state) avoids the need for the child component to know about the API call lifecycle — it simply reacts to prop changes from the parent.

## Key Members

- `allSeries`: Array of series objects (or legacy strings). Each object carries `slug`, `organization_id`, `organization_name`, and `is_personal`.
- `currentSeries`: Slug of the currently assigned series, or empty string for none.
- `organizationId`: Filters which series are visible in the grid.
- `showCreateForm` / `onShowCreateFormChange`: Controlled props for the create-form toggle (optional; falls back to internal state).
- `pendingSeriesName`: Internally tracks the slug submitted via the create form, used to detect when creation has completed.

## Scenarios

### Author selects an existing series

1. The author opens the Advanced Post Options panel by clicking the cog icon in the editor toolbar.
2. The Options modal displays the Series section with a card grid of available series filtered by the current organization.
3. The author clicks a series card; the card highlights to indicate selection.
4. The `onSelectSeries` callback fires with the chosen series slug. If the series belongs to a different organization than the current context, a second event fires to update `organizationId`.
5. The article state updates to reflect the selected series, and the grid shows the card as selected.

### Author creates a new series inline

1. With no series currently selected, the author clicks "Create new series" in the Series section.
2. The component transitions to a creation form showing a text input for the series name.
3. The author types a name and submits the form.
4. The `onCreateSeries` callback fires with the new name. The button changes to "Creating..." and is disabled while the request is in flight.
5. Once `allSeries` or `currentSeries` updates to include the new slug, the create form automatically closes and the new series appears selected.

### Author removes the current series

1. The author opens the Options modal while the article already has a series assigned.
2. The series card grid shows the current series highlighted, along with a "Currently selected" indicator and a "Remove series" button.
3. The author clicks "Remove series".
4. The `onSelectSeries` callback fires with an empty value, clearing `series` from the article state.

### Series list is filtered by organization

1. The author switches the article to a specific organization via the organization selector in the editor header.
2. When the author opens the Series section, the grid shows both personal series and series belonging to that organization. Series from other organizations are hidden.
3. When no organization is selected, only personal series are shown.

### Author selects a series via the modal variant

1. The `SeriesSelectorModal` opens (e.g. triggered by another UI entry point) with `isOpen=true`.
2. The author selects an existing series card; the modal closes immediately after the selection callback fires.
3. If the author instead submits the create form, the creation callback fires and the modal closes.
4. Clicking the backdrop or the modal close button closes the modal and resets the create-form state.

## Failures / Exceptions

- Submitting the create form with an empty or whitespace-only name is prevented: the submit handler returns early without firing the callback.
- While a creation request is in progress (`isCreating=true`), the "Create series" button is disabled and the "Cancel" button is also disabled to prevent conflicting state changes.
- Legacy `allSeries` entries that are plain strings (rather than objects) are normalized to objects with `is_personal: true` and no `organization_id`, preserving backward compatibility.
