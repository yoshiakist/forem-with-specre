---
id: "01KHZ466X2VM8VAWD6RE82CF9J"
name: "user_can_manage_personal_settings"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/users/settings_controller.rb`
- `app/helpers/settings_helper.rb`
- `app/javascript/packs/initializers/initializeSettings.js`
- `app/javascript/packs/userProfileSettings.js`
- `app/javascript/settings/copyOrgSecret.js`
- `app/javascript/settings/mobilePageSel.js`
- `app/javascript/settings/rssFetchTime.js`
- `app/models/users/setting.rb`
- `app/views/users/edit.html.erb` (Template)
- `app/views/users/_customization.html.erb` (Template)
- `app/views/users/_theme_selector.html.erb` (Template)
- `app/views/users/_font_selector.html.erb` (Template)
- `app/views/users/_navbar_selector.html.erb` (Template)
- `app/views/users/_experience_selector.html.erb` (Template)
- `app/views/users/_editor_selector.html.erb` (Template)
- `app/views/users/_extensions.html.erb` (Template)
- `app/views/users/_publishing_from_rss.html.erb` (Template)
- `app/views/users/_content_preferences.html.erb` (Template)
- `app/views/users/_additional_authentication.html.erb` (Template)
- `app/views/users/_account_providers_emails.html.erb` (Template)
- `app/views/users/_account_providers_settings.html.erb` (Template)
- `app/views/users/_notifications.html.erb` (Template)
- `app/views/comments/settings.html.erb` (Template)
- `spec/models/users/setting_spec.rb` (Test)
- `spec/requests/user/user_settings_spec.rb` (Test)
- `spec/factories/users_settings.rb` (Test)
- `spec/system/user/user_edits_customization_spec.rb` (Test)
- `spec/system/user/user_edits_extensions_spec.rb` (Test)
- `spec/system/user/user_settings_response_templates_spec.rb` (Test)
- `spec/system/organization/user_updates_org_settings_spec.rb` (Test)
- `spec/views/users/settings_spec.rb` (Test)
- `app/javascript/settings/__tests__/copyOrgSecret.test.js` (Test)
- `app/javascript/settings/__tests__/mobilePageSel.test.js` (Test)
- `app/javascript/settings/__tests__/rssFetchTime.test.js` (Test)

## Functional Overview

An authenticated user can manage their personal display preferences, content settings, and account configuration through the multi-tab settings page. The settings page has tabs for Profile, Customization, Notifications, Account, Organization, and Extensions. The `Users::SettingsController` handles the update action for customization-related preferences: theme, font, navbar style, display options (announcements, sponsors), feed URL for RSS import, experience level, inbox type, and editor version. When a feed URL is provided, the controller triggers an async `Feeds::ImportArticlesWorker`. The experience level is also stored as a persistent cookie. After any update, the user's `profile_updated_at` timestamp is touched and auto audience segments are refreshed. JavaScript modules provide client-side enhancements including organization secret copying, RSS fetch time localization, mobile page navigation, and profile field character counting.

## Scenarios

### User updates display preferences

1. User navigates to the Customization tab in settings
2. User selects `config_theme` (light or dark), `config_font` (sans-serif, serif, open-dyslexic, etc.), and `config_navbar` (default or static)
3. User toggles `display_announcements`, `display_sponsors`, and `permit_adjacent_sponsors`
4. System persists the preferences to the user's `Users::Setting` record
5. User's `profile_updated_at` is updated; auto audience segments are refreshed

### User imports RSS feed

1. User enters a `feed_url` on the Extensions tab
2. System validates the URL format and persists it
3. System enqueues `Feeds::ImportArticlesWorker` to asynchronously fetch and import articles
4. The RSS fetch time is displayed in the user's local timezone via `rssFetchTime.js`

### User sets experience level

1. User selects an experience level from the scale (Novice through Expert, mapped to scores 1-10)
2. System persists the value and sets a persistent browser cookie for `experience_level`

### User manages OAuth identity providers

1. User views connected providers on the Account tab via `_account_providers_settings.html.erb`
2. User can remove an OAuth identity (e.g., disconnect GitHub)
3. On removal, the provider username is cleared, `profile_updated_at` is updated, and associated data (e.g., GitHub repos) is cleaned up
4. System validates that at least one authentication method remains active

### User manages comment notification subscriptions

1. User views per-comment notification settings via `comments/settings.html.erb`
2. User toggles between muted and all-comments notification mode
3. User can unsubscribe from parent article notifications
