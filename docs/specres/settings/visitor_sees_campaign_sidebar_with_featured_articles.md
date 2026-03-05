---
id: "01KJVM4JRDR1HWVGG2JNXWBT7N"
name: "visitor_sees_campaign_sidebar_with_featured_articles"
status: "draft"
---

## Related Files

- `app/models/campaign.rb`
- `app/decorators/campaign_decorator.rb`
- `app/controllers/sidebars_controller.rb`
- `app/views/articles/_sidebar_campaign.html.erb` (Template)
- `spec/requests/sidebars_spec.rb` (Test)

## Functional Overview

When a campaign is active and configured with a sidebar image, the home sidebar renders a campaign section showing a linked campaign image, a header with the campaign display name and total article count, and a list of up to five recently published, highly scored articles tagged with the campaign's featured tags. Two call-to-action links let the visitor submit a new article or browse all campaign-tagged articles. The `Campaign` singleton reads all configuration from `Settings::Campaign`, while `CampaignDecorator` handles image optimization and header text rendering. The `SidebarsController` fetches the article count and the latest article attributes (path, title, comment count, creation date) before rendering the sidebar partial.

## Design Intent

`Campaign` is a non-database singleton that delegates every configuration attribute to `Settings::Campaign`, keeping domain logic separate from persistence. Using a Singleton avoids repeated instantiation and allows `CampaignDecorator` to wrap the same shared object with view helpers without coupling the model to the view layer.

## Key Members

- `Campaign#show_in_sidebar?` — returns true only when both `sidebar_enabled?` is set and `sidebar_image` is present; guards rendering of the sidebar section.
- `Campaign#plucked_article_attributes(limit:, attributes:)` — returns lightweight tuples (path, title, comments_count, created_at) for up to five articles, avoiding full AR object instantiation.
- `Campaign#articles_scope` — filters articles by featured tags, recency (`articles_expiry_time` weeks), positive score, and optionally approval status.
- `CampaignDecorator#sidebar_image` — optimizes the image URL to 500 px wide and wraps it in an anchor if a campaign URL is configured.
- `CampaignDecorator#header_text(count)` — returns `"<display_name> (<count>)"` when a display name is set, otherwise falls back to the i18n `views.campaign.subtitle` key.

## Scenarios

### Campaign sidebar shown when enabled and image present

1. A visitor loads the home page sidebar.
2. `SidebarsController#get_latest_campaign_articles` calls `Campaign.current.count` and `Campaign.current.plucked_article_attributes` to populate `@campaign_articles_count` and `@latest_campaign_articles`.
3. The `_sidebar_campaign` partial checks `Campaign#show_in_sidebar?`; because `sidebar_enabled?` is true and `sidebar_image` is present, it renders the section.
4. The sidebar displays the optimized campaign image wrapped in a link to the campaign URL, a header showing the display name and article count linked to the main featured tag, and a list of up to five article widget items.
5. Two buttons are rendered: one to create a new article under the main tag, one to browse all articles under that tag.

### Campaign sidebar hidden when no image is configured

1. A visitor loads the home page sidebar.
2. `Campaign#show_in_sidebar?` returns false because `sidebar_image` is blank (even if `sidebar_enabled?` is true).
3. The `_sidebar_campaign` partial does not render the campaign section.

### Header text falls back to i18n key when display name is absent

1. The campaign has no `display_name` configured.
2. `CampaignDecorator#header_text` returns the translated string from `views.campaign.subtitle` with the article count interpolated.

### Campaign image rendered without link when no URL configured

1. The campaign has no `url` configured.
2. `CampaignDecorator#sidebar_image` returns a plain `<img>` tag (not wrapped in an anchor).

### Articles requiring approval filtered correctly

1. The campaign setting `articles_require_approval?` is true.
2. `Campaign#articles_scope` applies the `.approved` scope in addition to the tag, recency, and score filters, so only editorially approved articles appear in the sidebar list.
