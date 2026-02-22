---
id: "01KJ1NAJZ24HMXNKC0E5H4G4FQ"
name: "author_can_embed_github_readme_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/github_tag.rb` (base dispatcher class that routes `{% github %}` tags to either GithubIssueTag or GithubReadmeTag)
- `app/liquid_tags/github_tag/github_readme_tag.rb`
- `app/views/liquids/_github_readme.html.erb` (Template)
- `spec/liquid_tags/github_tag/github_readme_tag_spec.rb` (Test)

## Functional Overview

The `GithubTag::GithubReadmeTag` renders a rich preview of a GitHub repository including its metadata and optionally its README content. It accepts either a full `github.com` repository URL or a bare `owner/repo` path. The tag fetches repository metadata and README HTML via `Github::OauthClient`, then rewrites relative paths in the README (images, links, anchors) to absolute GitHub URLs using Nokogiri. The `no-readme` option suppresses README rendering.

## Design Intent

README files frequently contain relative paths (`./image.png`, `#section`) that break when rendered outside GitHub. The `clean_relative_path!` method categorizes paths into three types — anchor (`#`), absolute from root (`/`), and relative — and prepends the appropriate base URL. Repositories without READMEs degrade gracefully by omitting the body section.

## Key Members

- `README_REGEXP` — matches `github.com/owner/repo` URLs (owner/repo each up to 39 chars)
- `NOREADME_OPTIONS` — `%w[no-readme noreadme]` suppress README fetching
- `parse_input` — strips the GitHub domain prefix, splits options, normalizes the path via `Addressable::URI`
- `clean_relative_path!` — Nokogiri-based rewriting of `img[src]` and `a[href]` to absolute URLs
- `fetch_readme` — calls `Github::OauthClient#readme` with HTML accept header

## Scenarios

### Embedding a repository with README

1. Author writes `{% github https://github.com/org/repo %}`
2. System fetches repository metadata via `Github::OauthClient#repository`
3. System fetches README HTML via `Github::OauthClient#readme`
4. Relative paths in the README are rewritten to absolute GitHub URLs
5. Rendered card shows repository info (stars, forks, description) and the README body

### Embedding a repository without README display

1. Author writes `{% github org/repo no-readme %}`
2. System fetches only repository metadata (skips README fetch)
3. Rendered card shows repository info without the README body

### Embedding a repository with missing README

1. Author provides a repository URL for a repo that has no README
2. `fetch_readme` catches `Github::Errors::NotFound` and returns `nil`
3. Rendered card shows repository info only (no body section)

## Failures / Exceptions

- Invalid repository URLs or non-existent repos raise `StandardError` via `raise_error`
- Invalid options (anything other than `no-readme` / `noreadme`) raise `StandardError` listing valid options
- `Github::Errors::NotFound` and `Github::Errors::InvalidRepository` are caught and converted to a user-facing error
