---
id: "01KHY7Q19Z56D755QQ2C012XTX"
name: "unified_embed_registry_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/unified_embed/registry.rb
- app/liquid_tags/unified_embed.rb
- app/liquid_tags/unified_embed/tag.rb
- spec/liquid_tags/unified_embed/registry_spec.rb

## Functional Overview

This specification defines the expected behavior of `UnifiedEmbed::Registry` within the liquid_tags domain.

### Behavioral Areas

- **.find_liquid_tag_for**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/unified_embed/registry.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/unified_embed.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/unified_embed/tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: returns AsciinemaTag for an asciinema url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns AsciinemaTag for an asciinema url

### S-2: returns BlogcastTag for a valid blogcast url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns BlogcastTag for a valid blogcast url

### S-3: returns CodesandboxTag for a valid codesandbox url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns CodesandboxTag for a valid codesandbox url

### S-4: returns CodepenTag for a codepen url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns CodepenTag for a codepen url

### S-5: returns DotnetFiddleTag for a dotnetfiddle url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns DotnetFiddleTag for a dotnetfiddle url

### S-6: returns ForemTag for a Forem-specific url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns ForemTag for a Forem-specific url

### S-7: returns OpenGraphTag for pathless or invalid Forem url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns OpenGraphTag for pathless or invalid Forem url

### S-8: returns GistTag for a gist url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns GistTag for a gist url

### S-9: returns GithubTag for a github repository url (with or without option)

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns GithubTag for a github repository url (with or without option)

### S-10: returns GithubTag for a github issue url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns GithubTag for a github issue url

### S-11: returns GlitchTag for a valid glitch url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns GlitchTag for a valid glitch url

### S-12: returns InstagramTag for a valid instagram post url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns InstagramTag for a valid instagram post url

