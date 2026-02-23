---
id: "01KJ43E9107K5RBF375S75E2PV"
name: "system_checks_comment_for_spam"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/ai/comment_check.rb`
- `app/workers/comments/handle_spam_worker.rb`
- `app/services/spam/handler.rb`
- `spec/services/spam/handler_spec.rb` (Test)

## Functional Overview

When a comment is created, `Comments::HandleSpamWorker` enqueues an asynchronous job that invokes `Spam::Handler.handle_comment!` on the comment. `Spam::Handler` is a shared module that handles spam detection across multiple content types (articles, users, profiles, and comments); this card covers only the comment spam path. The handler first bypasses checking for users with more than six badge achievements or an active base subscriber role. It then checks whether the comment's first linked domain has been used in more than ten other low-scoring recent comments (domain-based spam), and if not, falls back to a rate-limit text trigger and an AI analysis via `Ai::CommentCheck`. When spam is confirmed by any path, the system issues a negative "vomit" reaction from the mascot user against the comment and, if the commenter has accumulated too many spammy reactions overall, automatically suspends the account and creates an audit note.

## Design Intent

The handler applies a graduated escalation strategy: trusted users are exempted first to avoid false positives, then low-cost deterministic checks (domain reputation, rate-limit keyword matching) run before invoking the AI to minimize unnecessary API calls. The AI check is only attempted when a link is present in the comment and an API key is configured, keeping inference costs proportional to actual risk signals.

## Key Members

- `badge_achievements_count` — users with more than 6 badges are unconditionally trusted and bypass all checks
- `base_subscriber?` — users with the base subscriber role are unconditionally trusted
- `extensive_domain_spam?` threshold — requires more than 10 other comments in the past 48 hours sharing the same domain, with over 80% of those comments scoring below -100
- `Ai::CommentCheck#spam?` — sends a YES/NO prompt to the AI backend with comment body, parent post body, and the user's last 10 comments as context; returns `false` on any error

## Scenarios

### Trusted user bypasses all checks

1. A background job receives a comment ID and loads the comment.
2. The handler checks the commenter's badge count and subscriber status.
3. Because the user has more than 6 badge achievements or holds the base subscriber role, the handler returns `:not_spam` immediately without running any further checks.

### Domain-based spam is detected

1. The handler extracts the first hyperlink domain from the comment's processed HTML.
2. It queries comments from the past 48 hours containing that domain (excluding the current comment).
3. More than 10 such comments exist, and over 80% of them have a score below -100.
4. The handler issues a "vomit" reaction from the mascot user against the comment and checks whether the commenter is a repeat offender.
5. If the commenter has received too many spammy reactions, the system suspends the account and records an automatic suspension note. The handler returns `:spam` without running rate-limit or AI checks.

### Rate-limit text trigger detects spam

1. No domain-based spam is found (or no link is present).
2. The handler passes the comment body text to `Settings::RateLimit.trigger_spam_for?`, which matches against configured spam trigger terms.
3. The rate-limit check returns true, so the handler issues a "vomit" reaction and conditionally suspends the commenter if they are a repeat offender.

### AI check detects spam

1. The rate-limit check returns false, but the comment's processed HTML contains a hyperlink and an AI API key is configured.
2. `Ai::CommentCheck` builds a prompt containing the comment body, parent post content, and the commenter's recent comment history, then queries the AI backend.
3. The AI responds "YES", so the handler issues a "vomit" reaction and conditionally suspends the commenter if they are a repeat offender.

### No spam detected

1. The commenter is not a trusted user.
2. The domain check finds fewer than 11 matching recent comments, or fewer than 80% are low-scoring.
3. The rate-limit check returns false, and either no link is present, no API key is configured, or the AI responds "NO".
4. The handler returns `:not_spam` and takes no further action.

## Failures / Exceptions

- If `Ai::CommentCheck#spam?` raises any `StandardError`, the error is logged and the method returns `false`, preventing a failed AI call from being treated as a positive spam signal.
- If the comment record cannot be found by ID in the worker, `Spam::Handler.handle_comment!` is not called and the job exits silently.
- If the domain URI in the comment link is malformed, `URI::InvalidURIError` is rescued and `extract_first_domain_from` returns `nil`, skipping the domain-based check.
