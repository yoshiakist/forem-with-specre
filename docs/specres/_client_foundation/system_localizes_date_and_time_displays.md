---
id: "01KJXXZA1WFJVBDE2YJ67GMEGP"
name: "system_localizes_date_and_time_displays"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/packs/initializers/initializeDateTimeHelpers.js`
- `app/javascript/packs/initializers/initializeTimeFixer.js`
- `app/javascript/packs/initializers/__tests__/initializeTimeFixer.test.js` (Test)

## Functional Overview

When a page loads, the system scans the DOM for elements that carry UTC timestamps and rewrites their visible content using the browser's locale and the user's local timezone. Two initializers handle this: `initializeDateHelpers` targets semantic `<time>` elements with class-based format hints (`date-no-year`, `date`, `date-short-year`) and delegates to the shared `localizeTimeElements` utility, while `initializeTimeFixer` targets elements with classes `utc-time`, `utc-date`, and `utc`, reads their raw UTC millisecond values, converts them with `Intl.DateTimeFormat('en-US', ...)`, and writes the formatted string back into each element's `innerHTML`.

## Key Members

- `initializeDateHelpers()` — entry point that localizes `<time>` elements for three date format variants
- `initializeTimeFixer()` — entry point that localizes `.utc-time`, `.utc-date`, and `.utc` elements
- `formatDateTime(options, value)` — thin wrapper around `Intl.DateTimeFormat('en-US', options).format(value)`
- `convertUtcTime(utcTime)` — converts a UTC millisecond value to a time string: hour + minute + short timezone name (e.g. "3:04 AM UTC")
- `convertUtcDate(utcDate)` — converts a UTC millisecond value to a short date string: abbreviated month + day (e.g. "Feb 2")
- `convertCalEvent(utc)` — converts a UTC millisecond value to a calendar-event string: long weekday, long month, day, hour, minute (e.g. "Tuesday, January 20 at 11:23 AM")
- `updateLocalDateTime(elements, convertCallback, getUtcDateTime)` — iterates an element collection, invokes `convertCallback` with the UTC value returned by `getUtcDateTime`, and writes the result into each element's `innerHTML`

## Scenarios

### Semantic date elements are localized on page load

1. The page contains `<time>` elements marked with one of the CSS classes `date-no-year`, `date`, or `date-short-year`.
2. `initializeDateHelpers` is called during page initialization.
3. For `date-no-year` elements, the system renders the date as abbreviated month and day (e.g. "Jul 12").
4. For `date` elements, the system renders the date as abbreviated month, day, and four-digit year (e.g. "Jul 12, 2020").
5. For `date-short-year` elements, the system renders the date as abbreviated month, day, and two-digit year (e.g. "Jul 12 '20").

### UTC time elements are converted to local time

1. The page contains elements with the CSS class `utc-time` whose `data-datetime` attribute holds a UTC timestamp in milliseconds.
2. `initializeTimeFixer` is called during page initialization.
3. The system converts each element's timestamp to a local time string showing hour, minute, and the abbreviated timezone name (e.g. "3:04 AM UTC").
4. Each element's visible text is replaced with the formatted local time string.

### UTC date elements are converted to short local date

1. The page contains elements with the CSS class `utc-date` whose `data-datetime` attribute holds a UTC timestamp in milliseconds.
2. `initializeTimeFixer` is called during page initialization.
3. The system converts each element's timestamp to a short date string showing abbreviated month and day (e.g. "Feb 2").
4. Each element's visible text is replaced with the formatted date string.

### Calendar event elements are converted to a full datetime string

1. The page contains elements with the CSS class `utc` whose `innerHTML` holds a UTC timestamp in milliseconds.
2. `initializeTimeFixer` is called during page initialization.
3. The system converts each element's timestamp to a full calendar-event string showing long weekday, long month name, day, and time (e.g. "Tuesday, February 2 at 3:04 AM").
4. Each element's visible text is replaced with the formatted calendar-event string.

### No conversion occurs when no UTC elements are present

1. The page contains no elements with the CSS class `utc`, `utc-time`, or `utc-date`.
2. `initializeTimeFixer` is called during page initialization.
3. The system finds empty collections for all three class lookups and makes no DOM changes.
