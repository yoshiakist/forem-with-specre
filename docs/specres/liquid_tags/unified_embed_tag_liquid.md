---
id: "01KHY7Q1A26S1QDNJEW2AZM336"
name: "unified_embed_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/cloud_run_tag.rb
- app/liquid_tags/codepen_tag.rb
- app/liquid_tags/codesandbox_tag.rb
- app/liquid_tags/comment_tag.rb
- app/liquid_tags/cta_tag.rb
- app/liquid_tags/details_tag.rb
- app/liquid_tags/dotnet_fiddle_tag.rb
- app/liquid_tags/forem_tag.rb
- spec/liquid_tags/unified_embed/tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `UnifiedEmbed::Tag` within the liquid_tags domain.

### Behavioral Areas

- **minimal keyword**: uses OpenGraphTag for non-allowlisted URLs when minimal is specified
- **SSRF protection**: bypasses SSRF protection for Twitter/X URLs
- **private_ip?**: handles AddressFamilyError gracefully in private_ip?
- **validate_link with SSRF protection**: bypasses SSRF protection for Twitter/X URLs
- **HTTP timeout settings**: handles https://guides.rubyonrails.org
- **CloudFlare-compatible User-Agent**: sanitizes community_name into safe user-agent string
- **redirect and auth handling**: repeats validation when link returns redirect

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cta_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: handles https://guides.rubyonrails.org

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles https://guides.rubyonrails.org

### S-2: delegates parsing to the link-matching class

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** delegates parsing to the link-matching class

### S-3: delegates parsing to the link-matching class when there are options

- **Given** the system is in a standard operational state
- **When** there are options
- **Then** delegates parsing to the link-matching class

### S-4: raises an error when link cannot be found

- **Given** the system is in a standard operational state
- **When** link cannot be found
- **Then** raises an error

### S-5: repeats validation when link returns not-allowed

- **Given** the system is in a standard operational state
- **When** link returns not-allowed
- **Then** repeats validation

### S-6: raises an error when link returns not-allowed too many times

- **Given** the system is in a standard operational state
- **When** link returns not-allowed too many times
- **Then** raises an error

### S-7: repeats validation when link returns redirect

- **Given** the system is in a standard operational state
- **When** link returns redirect
- **Then** repeats validation

### S-8: raises error when link redirects too many times in a row

- **Given** the system is in a standard operational state
- **When** link redirects too many times in a row
- **Then** raises error

### S-9: calls OpenGraphTag when no link-matching class is found

- **Given** the system is in a standard operational state
- **When** no link-matching class is found
- **Then** calls OpenGraphTag

### S-10: falls back to a simple link card when validation raises a network/SSL error

- **Given** the system is in a standard operational state
- **When** validation raises a network/SSL error
- **Then** falls back to a simple link card

### S-11: sanitizes community_name into safe user-agent string

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sanitizes community_name into safe user-agent string

### S-12: uses OpenGraphTag for non-allowlisted URLs when minimal is specified

- **Given** the system is in a standard operational state
- **When** minimal is specified
- **Then** uses OpenGraphTag for non-allowlisted URLs

