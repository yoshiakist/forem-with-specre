---
id: "01KJ1SFMV2GXC3T80QKKH4YY6D"
name: "system_generates_ai_recap_of_github_repo_activity"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/ai/github_repo_recap.rb`
- `spec/services/ai/github_repo_recap_spec.rb` (Test)

## Functional Overview

`Ai::GithubRepoRecap` fetches merged pull requests and recent commits from a GitHub repository over a configurable lookback window (default 7 days), builds a structured prompt from that activity data, and delegates to an AI client to produce a human-readable markdown recap. The recap is returned as a `RecapResult` struct containing a title and a markdown body. If no activity is found within the timeframe, or if any error occurs during the process, the service returns `nil`. PR and commit data is fetched page-by-page with manual pagination control (auto-pagination is temporarily disabled per call) and is capped at 500 PRs across 5 pages and 300 commits to prevent excessive API usage. Commit summaries are further capped at 50 entries in the prompt to stay within AI token limits.

## Design Intent

Manual pagination control exists because the underlying GitHub client has a global `auto_paginate` setting that would otherwise fetch all pages in a single call, risking hangs on large repositories. The service saves, disables, and restores `auto_paginate` around each API call so it can implement its own controlled loop with explicit page and item limits.

## Key Members

- `repo_name` — GitHub repository identifier in `"owner/name"` format
- `days_ago` — lookback window in days (default: 7)
- `since` — computed cutoff timestamp (`days_ago.days.ago`), used to filter PRs and commits
- `github_client` — injectable `Github::OauthClient` instance (defaults to a new unauthenticated client)
- `ai_client` — injectable `Ai::Base` instance used to call the language model
- `RecapResult` — keyword-init struct with `title` and `body` fields returned by `generate`

## Scenarios

### Activity found — recap generated successfully

1. Caller instantiates the service with a repository name and an optional `days_ago` value.
2. System fetches closed pull requests sorted by last update descending, page by page, collecting those whose `merged_at` timestamp falls within the lookback window. Fetching stops when a PR before the cutoff is encountered, the maximum page limit is reached, or the last page is received.
3. System fetches commits since the cutoff timestamp using the same controlled pagination, stopping at 300 commits.
4. System constructs a prompt that includes the repository name, timeframe, a formatted list of merged PRs with URLs and authors, and up to 50 commit short-SHAs with their first message lines (with an overflow count appended when more than 50 exist).
5. System sends the prompt to the AI client and receives a response containing a `TITLE:` line and a `BODY:` section.
6. System parses the response, strips any accidental code-fence wrapping from the body, and returns a `RecapResult` with the extracted title and body.

### No activity in the timeframe — nil returned

1. System fetches pull requests and commits as usual.
2. Both collections are empty (zero merged PRs and zero commits within the window).
3. System detects no activity and returns `nil` without calling the AI client.

### Only old pull requests exist — treated as no activity

1. GitHub returns closed PRs whose `merged_at` is older than the cutoff.
2. The within-timeframe filter excludes them all; the commit list is also empty.
3. System detects no activity and returns `nil`.

### Commits present but no merged PRs

1. No merged PRs fall within the window; commits do exist.
2. System builds the prompt with the PR section showing "No pull requests merged in this timeframe." and the commit section listing the available commits.
3. AI client generates a recap, and the service returns a populated `RecapResult`.

### AI response is malformed

1. The AI client returns a response that does not contain the expected `TITLE:` / `BODY:` markers.
2. System falls back to "Repository Activity Recap" as the default title and uses the full raw response as the body.
3. A `RecapResult` is returned rather than raising an error.

## Failures / Exceptions

- `Github::Errors::Error` raised during PR or commit fetching is rescued per-method; the affected collection is returned as an empty array and the error is logged via `Rails.logger.error`. The service continues and may still return a result if the other collection succeeded.
- Any `StandardError` raised during the overall `generate` flow (including AI client failures) is rescued at the top level, logged with class, message, and backtrace, and causes `generate` to return `nil`.
