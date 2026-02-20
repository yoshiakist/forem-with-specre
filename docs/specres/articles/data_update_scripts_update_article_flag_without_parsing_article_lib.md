---
id: "01KHY7PZCQ2TW336K0KHAY86BF"
name: "data_update_scripts_update_article_flag_without_parsing_article_lib"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/articles_controller.rb
- app/controllers/api/v0/articles_controller.rb
- app/controllers/api/v1/articles_controller.rb
- app/controllers/api/v1/recommended_articles_lists_controller.rb
- app/controllers/article_approvals_controller.rb
- app/controllers/articles_controller.rb
- spec/lib/data_update_scripts/update_article_flag_without_parsing_article_spec.rb

## Functional Overview

This specification defines the expected behavior of `DataUpdateScripts::UpdateArticleFlagWithoutParsingArticle` within the articles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: set main_image_from_frontmatter to true only for articles with cover_image in bo...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** set main_image_from_frontmatter to true only for articles with cover_image in body_markdown

