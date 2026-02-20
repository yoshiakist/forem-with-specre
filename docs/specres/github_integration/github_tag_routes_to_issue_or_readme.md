---
id: "01KHY95XQ0ZTM1EVAMZWD5AW7K"
name: "github_tag_routes_to_issue_or_readme"
status: "draft"
---

## Related Files

- app/liquid_tags/github_tag.rb
- app/liquid_tags/github_tag/github_issue_tag.rb
- app/liquid_tags/github_tag/github_readme_tag.rb

## Functional Overview

`GithubTag` is a Liquid tag that serves as the entry point for embedding GitHub content in articles. It parses a GitHub URL, determines whether the URL refers to an issue/pull request or a repository, and delegates rendering to the appropriate sub-tag (`GithubIssueTag` or `GithubReadmeTag`). It is registered as the `{% github %}` Liquid tag and with the `UnifiedEmbed` registry for URL-based auto-embedding.

## Scenarios

### URL routing dispatches to issue or readme renderer

1. When the GitHub URL contains `issues` or `pull` in its path, the system delegates to `GithubTag::GithubIssueTag`.
2. When the URL does not contain `issues` or `pull`, the system delegates to `GithubTag::GithubReadmeTag`.
3. The content is pre-rendered during tag initialization and cached for the `render` call.

### URL sanitization strips tags and unescapes HTML entities

1. The input link is stripped of any HTML tags.
2. HTML entities in the link are unescaped (e.g., `&amp;` becomes `&`).

### Registration enables Liquid template and URL auto-embedding

1. The tag is registered with `Liquid::Template` under the name `"github"`, enabling `{% github URL %}` syntax.
2. The tag is registered with `UnifiedEmbed` using `REGISTRY_REGEXP`, enabling automatic embedding when a matching GitHub URL is pasted.
3. `REGISTRY_REGEXP` matches GitHub repository URLs, issue URLs, pull request URLs, and issue comment URLs.

### Rendering errors are re-raised as StandardError

1. If either sub-tag raises a `StandardError` during pre-rendering, `GithubTag` re-raises it.
