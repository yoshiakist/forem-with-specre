---
id: "01KHY91JCKT3BDMGCZRCGVCRME"
name: "github_issue_stores_github_content"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/github_issue.rb
- spec/models/github_issue_spec.rb (Test)

## Functional Overview

`GithubIssue` is an ActiveRecord model that caches GitHub issues, pull requests, and issue comments fetched from the GitHub API. It stores the raw API response as a serialized hash and a rendered HTML version of the body. The model provides a `find_or_fetch` class method that returns a cached record when available or fetches from the GitHub API on first access.

## Scenarios

### Validation constrains URL format and category

1. The system requires `url` to be present and at most 400 characters.
2. The system requires `url` to match the GitHub API URL pattern (`https://api.github.com/repos/...`).
3. The system enforces uniqueness on `url`.
4. The system requires `category` to be either `"issue"` or `"issue_comment"`.

### find_or_fetch returns cached record or fetches from API

1. When a `GithubIssue` with the given URL already exists in the database, it is returned without making an API call.
2. When no record exists, the system fetches the content from the GitHub API via `Github::OauthClient`.
3. The fetched data is saved as a new `GithubIssue` record and returned.

### Fetching distinguishes issues, pull requests, and comments

1. If the URL contains an issue-comments path segment, the system fetches via `issue_comment` and sets category to `"issue_comment"`.
2. If the URL contains an issues or pulls path segment, the system fetches via `issue` and sets category to `"issue"`.
3. The raw API response is serialized into `issue_serialized`.
4. If the response body is present, the system renders it to HTML via `Github::OauthClient#markdown` and stores it in `processed_html`.

### Not-found issues raise an error with a localized message

1. When the GitHub API returns a 404, the system raises `Github::Errors::NotFound`.
2. The error message is localized and includes the issue or comment ID extracted from the URL.

## Design Intent

`GithubIssue` acts as a read-through cache for GitHub content used by the `GithubIssueTag` liquid tag. By caching API responses, it avoids repeated GitHub API calls when the same issue is embedded in multiple articles. The `find_or_fetch` pattern provides a simple interface that hides the caching logic from consumers.
