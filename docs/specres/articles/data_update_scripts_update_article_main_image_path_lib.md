---
id: "01KHY7PZCT19FVNEE3TEF1Q33G"
name: "data_update_scripts_update_article_main_image_path_lib"
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
- spec/lib/data_update_scripts/update_article_main_image_path_spec.rb

## Functional Overview

This specification defines the expected behavior of `Update_Article_Main_Image_Path` within the articles domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/articles_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/recommended_articles_lists_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/article_approvals_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/articles_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: update main_image to a raw path

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** update main_image to a raw path

