---
id: "01KHZ3ZSMNQ8VSYTC2EGQJT5RS"
name: "admin_can_configure_analytics_and_monetization"
status: "draft"
---

## Related Files

- `app/controllers/admin/settings/general_settings_controller.rb`
- `app/models/settings/general.rb`
- `app/lib/constants/settings/general.rb`
- `app/services/settings/general/upsert.rb`
- `app/views/admin/settings/forms/_google_analytics.html.erb` (Template)
- `app/views/admin/settings/forms/_ahoy.html.erb` (Template)
- `app/views/admin/settings/forms/_monetization.html.erb` (Template)
- `app/views/admin/settings/forms/_credits.html.erb` (Template)
- `app/views/admin/settings/forms/_api_tokens.html.erb` (Template)

## Functional Overview

A super-admin can configure analytics tracking, cookie consent banners, payment integration, credit pricing, and platform API tokens. Analytics settings include Google Analytics 4 measurement ID, Ahoy tracking toggle, and cookie banner context for both user and platform levels. Monetization covers Stripe API keys, credit tier pricing (small, medium, large, xlarge in cents), and billboard-enabled countries (validated as ISO 3166-2 codes). The general settings controller parses `billboard_enabled_countries` from JSON and coerces `credit_prices_in_cents` values to integers before upsert. API tokens include a health check token and video encoder key.

## Scenarios

### Admin configures Google Analytics and cookie consent

1. Admin enters `ga_analytics_4_id` (GA4 measurement ID)
2. Admin selects `cookie_banner_user_context` and `cookie_banner_platform_context` from dropdown options
3. System persists the values; GA tracking script is injected into page templates when the ID is set

### Admin toggles Ahoy analytics

1. Admin enables or disables `ahoy_tracking` via checkbox
2. System persists the boolean; when enabled, Ahoy records page visits and events for internal analytics

### Admin configures Stripe payment integration

1. Admin enters `stripe_api_key` and `stripe_publishable_key`
2. System persists the keys; Stripe integration becomes available for payment-related features on the platform

### Admin sets credit tier pricing

1. Admin enters prices in cents for each tier: small, medium, large, xlarge via nested `credit_prices_in_cents` fields
2. `Settings::General::Upsert` coerces values to integers before persistence
3. Credit prices are used by the platform's credit purchasing flow

### Admin configures billboard-enabled countries

1. Admin sets `billboard_enabled_countries` (visible only when geolocation feature flag is enabled)
2. The general settings controller parses the JSON input and coerces country codes to symbols
3. System validates each code against ISO 3166-2 with `with_regions` or `without_regions` markers
4. Billboards are only shown to users in the configured countries

### Admin sets API tokens

1. Admin enters the `health_check_token` used by monitoring systems to verify platform health
2. Admin enters the `video_encoder_key` for video processing integration
3. System persists the token values
