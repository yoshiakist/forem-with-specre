---
id: "01KJ1NAJFG6ZBXN7HJTB9VVXBE"
name: "author_can_embed_github_issue_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/github_tag/github_issue_tag.rb`
- `app/liquid_tags/github_tag.rb` (source file — the base dispatcher class that routes `{% github %}` tags to either GithubIssueTag or GithubReadmeTag)
- `app/models/github_issue.rb` (source file — the model that caches GitHub issue/PR/comment data, used by `GithubIssue.find_or_fetch`)
- `app/views/liquids/_github_issue.html.erb` (Template)
- `spec/liquid_tags/github_tag/github_issue_tag_spec.rb` (Test)
- `spec/models/github_issue_spec.rb` (Test)

## Functional Overview

The `GithubTag::GithubIssueTag` renders rich preview cards for GitHub issues, pull requests, and comments. It converts a public `github.com` URL into the corresponding GitHub API endpoint, fetches the content via `GithubIssue.find_or_fetch` (which caches results), and renders a card showing the title, author avatar, creation date, and processed HTML body. The tag handles three URL types: issues (`/issues/{id}`), pull requests (`/pull/{id}`), and issue comments (`/issues/{id}#issuecomment-{id}`).

## Design Intent

GitHub's public URLs differ from their API URLs in multiple ways: `/pull/` becomes `/pulls/`, and `#issuecomment-{id}` fragments must be converted to `/issues/comments/{id}` paths. The `generate_api_link` method performs these conversions using `Addressable::URI` parsing. The `GithubIssue` model provides caching to avoid redundant API calls.

## Key Members

- `ISSUE_REGEXP` — matches GitHub issue, PR, and comment URLs with optional fragment
- `generate_api_link` — converts public GitHub URL to API endpoint (handles `/pull/` → `/pulls/`, comment fragment → `/issues/comments/`)
- `GithubIssue.find_or_fetch` — retrieves or caches the API response
- `@is_issue` — distinguishes issues/PRs (have title) from comments (no title)

## Scenarios

### Embedding a GitHub issue

1. Author writes `{% github https://github.com/org/repo/issues/123 %}`
2. System converts URL to `https://api.github.com/repos/org/repo/issues/123`
3. `GithubIssue.find_or_fetch` retrieves the issue data
4. Rendered card shows issue title, author, date, and body HTML

### Embedding a pull request

1. Author provides `https://github.com/org/repo/pull/456`
2. System converts `/pull/` to `/pulls/` in the API URL
3. Rendered card shows the PR details with the same layout as issues

### Embedding an issue comment

1. Author provides `https://github.com/org/repo/issues/123#issuecomment-789`
2. System rewrites the URL to `https://api.github.com/repos/org/repo/issues/comments/789`
3. Rendered card shows "Comment for" as the title and the comment body

## Failures / Exceptions

- URLs not matching `ISSUE_REGEXP` raise `StandardError` with an invalid-github-issue-pull message
- Non-existent issues (API 404) propagate the error from `GithubIssue.find_or_fetch`
