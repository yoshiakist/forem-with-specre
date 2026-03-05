---
id: "01KJXZEFFF536J5E1TJD9VPMJ7"
name: "user_can_select_date_range"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/formElements/DateRangePicker/DateRangePicker.jsx`
- `app/javascript/crayons/formElements/DateRangePicker/dateRangeUtils.js`
- `app/javascript/crayons/formElements/DateRangePicker/index.js`
- `app/javascript/crayons/formElements/DateRangePicker/__tests__/DateRangePicker.test.jsx` (Test)
- `app/javascript/crayons/formElements/DateRangePicker/__tests__/dateRangeUtils.test.js` (Test)

## Functional Overview

`DateRangePicker` is a Preact component that wraps the `react-dates` library to provide an accessible date range selection UI. The user can pick a start date and an end date either by typing into text inputs, by clicking calendar days, or by clicking a preset quick-select button (e.g. "This month", "Last quarter"). The calendar orientation switches automatically from horizontal to vertical on narrow viewports. Month and year dropdowns allow rapid navigation within the permitted date window. Each text input is validated on blur and displays an accessible error message when the typed value is malformed or falls outside the permitted `minStartDate`–`maxEndDate` bounds. The component respects the browser locale: `en-US` users see `MM/DD/YYYY` formatting while all other locales receive `DD/MM/YYYY`. A hidden `date_format` input is rendered alongside the picker so that server-side form handlers can parse submitted dates correctly.

## Design Intent

The component is a thin, opinionated wrapper rather than a from-scratch calendar, deliberately delegating complex calendar rendering and keyboard interaction to `react-dates`. Custom overrides (custom nav icons, `MonthYearPicker`, `PresetDateRangeOptions`, `useDateRangeValidation`) are layered on top to meet Forem's accessibility and UX requirements without duplicating calendar logic. Preset ranges are defined as pure utility functions in `dateRangeUtils.js` so they can be tested in isolation without a DOM.

## Key Members

- `DateRangePicker` — main exported component; accepts `startDateId`, `endDateId`, `defaultStartDate`, `defaultEndDate`, `minStartDate`, `maxEndDate`, `onDatesChanged`, `presetRanges`, `startDateAriaLabel`, `endDateAriaLabel`, `todaysDate`
- `onDatesChanged` — callback called with `{ startDate: Date, endDate: Date }` every time the internal selection changes
- `presetRanges` — array of preset range name constants (`MONTH_UNTIL_TODAY`, `LAST_FULL_MONTH`, `QUARTER_UNTIL_TODAY`, `LAST_FULL_QUARTER`, `YEAR_UNTIL_TODAY`, `LAST_FULL_YEAR`)
- `getDateRangeStartAndEndDates({ today, dateRangeName })` — pure utility that returns `{ start: Moment, end: Moment }` for a named preset relative to a given reference date
- `useDateRangeValidation` — internal hook that attaches blur listeners to the two text inputs and exposes `startDateError` / `endDateError` strings
- `MonthYearPicker` — internal sub-component rendering month and year `<select>` elements for rapid calendar navigation
- `PresetDateRangeOptions` — internal sub-component rendering quick-select `<Button>` elements for permitted preset ranges

## Scenarios

### User selects dates by typing into the inputs

1. User focuses the start date text input (placeholder shows the locale-appropriate format, e.g. `MM/DD/YYYY`).
2. User types a valid date string; the calendar updates in real time to reflect the typed value.
3. User types a valid end date into the end date input.
4. `onDatesChanged` is called with `{ startDate, endDate }` as native `Date` objects on each keystroke that produces a parseable date.

### User selects dates by clicking calendar days

1. User clicks the calendar icon or the start date input to open the calendar.
2. User clicks a day in the calendar grid to set the start date; focus automatically moves to the end date.
3. User clicks a day for the end date; the calendar closes and `onDatesChanged` is called with the selected range.

### User selects a preset range with a quick-select button

1. Preset range buttons (e.g. "This month", "Last quarter") are rendered below the calendar only for presets that fall entirely within `minStartDate`–`maxEndDate`.
2. User clicks a preset button; the start and end inputs are populated with the corresponding dates and the calendar closes.
3. `onDatesChanged` is called with the resolved `{ startDate, endDate }`.

### User navigates to a different month or year via dropdowns

1. The calendar header renders a month `<select>` and a year `<select>` in place of the default react-dates header.
2. User changes the month or year; the calendar grid immediately scrolls to show that period.
3. Available months in the dropdown are constrained to those within the `minStartDate`–`maxEndDate` window for the selected year.

### Text input shows an accessible error message for invalid or out-of-range input

1. User types an unrecognisable string (e.g. "something") into the start or end date input and tabs away.
2. The component validates the value on `blur`; if it does not match the expected format, an error message is rendered and associated with the input via `aria-describedby`.
3. If the value is a valid date but before `minStartDate`, the error reads "Start date must be on or after `<minStartDate>`".
4. If the value is a valid date but after `maxEndDate`, the error reads "Start date must be on or before `<maxEndDate>`".
5. The error region uses `aria-live="assertive"` so screen readers announce it immediately.

## Failures / Exceptions

- A preset range button is silently omitted when any part of its computed range falls outside the `minStartDate`–`maxEndDate` window; no error is shown to the user.
- If `todaysDate` is not provided, `new Date()` (the real system clock) is used; this parameter exists primarily to make tests deterministic.
- Dates in the calendar grid that are outside the permitted window are marked as outside-range by `react-dates` and cannot be clicked.
