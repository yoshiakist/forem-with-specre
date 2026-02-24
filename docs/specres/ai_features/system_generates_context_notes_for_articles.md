---
id: "01KJ6T8JKWPBA7WFHVR2JD7XMM"
name: "system_generates_context_notes_for_articles"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/ai/context_note_generator.rb`
- `spec/services/ai/context_note_generator_spec.rb` (Test)

## Functional Overview

`Ai::ContextNoteGenerator` generates a context note for an article based on tag-specific instructions by sending a prompt to an AI backend. Given an article and a tag, the service builds a prompt containing the article's title, full body markdown, and the tag's `context_note_instructions`, then submits it to `Ai::Base`. If the AI returns a valid response, the service persists a `ContextNote` record linked to both the article and the tag. If any required input is absent, the AI signals that the article is unsuitable ("INVALID"), or an error occurs, the service exits cleanly without creating a record.

## Design Intent

The service delegates all AI communication to `Ai::Base`, keeping generation logic isolated. The "INVALID" sentinel allows the AI to signal irrelevance without raising an error, enabling silent no-ops for articles that do not fit a tag's criteria. Errors are caught and logged rather than re-raised so that a single failure does not disrupt batch processing of multiple articles or tags.

## Key Members

- `article` — the article whose title and `body_markdown` are included in the prompt
- `tag` — the tag whose `context_note_instructions` drive the prompt; also associated with the created note
- `Ai::Base#call(prompt)` — sends the prompt to the Gemini API and returns the text response

## Scenarios

### Successful context note creation

1. Caller instantiates `Ai::ContextNoteGenerator` with a valid article and a tag that has non-blank `context_note_instructions`.
2. The service builds a prompt that includes the article title, full body markdown, and the tag's instructions.
3. The prompt is passed to the AI client, which returns a non-blank, non-"INVALID" response.
4. The service creates a `ContextNote` record with the stripped AI response linked to the article and tag, then returns it.

### AI signals the article is unsuitable

1. The service builds and sends the prompt as usual.
2. The AI returns the exact string "INVALID" (possibly with surrounding whitespace).
3. The service discards the response without creating a `ContextNote`, and returns nil.

### AI returns a blank response

1. The service builds and sends the prompt as usual.
2. The AI returns a blank or whitespace-only response.
3. The service discards the response without creating a `ContextNote`, and returns nil.

### Missing article, tag, or instructions

1. Caller provides a nil article, a nil tag, or a tag whose `context_note_instructions` are blank.
2. The guard clause at the start of `call` detects the missing data.
3. The service returns nil immediately without building a prompt or contacting the AI.

### Error during generation

1. During prompt submission or record creation, a `StandardError` is raised.
2. The rescue block logs the error message via `Rails.logger.error`.
3. The exception is not re-raised; the method returns nil.

## Failures / Exceptions

- `StandardError` raised by the AI client or `ContextNote.create!` is rescued, logged, and swallowed — no re-raise.
- If `tag.context_note_instructions` is blank after stripping, `build_prompt` returns nil, and `call` treats that as a no-op.
