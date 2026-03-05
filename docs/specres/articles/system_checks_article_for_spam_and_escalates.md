---
id: "01KJBN5DYZS4T9WNQYC16YKBD0"
name: "system_checks_article_for_spam_and_escalates"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/workers/articles/handle_spam_worker.rb`
- `app/workers/articles/label_cleanup_worker.rb`
- `app/services/spam/handler.rb` (shared — also covers `system_handles_spam_for_articles_and_comments`)
- `app/services/spam/domain_detector.rb`
- `app/services/ai/article_check.rb` (shared — also covers `system_checks_article_for_spam_and_escalates`)
- `app/services/slack/messengers/potential_spammer.rb`
- `spec/workers/articles/handle_spam_worker_spec.rb` (Test)
- `spec/workers/articles/label_cleanup_worker_spec.rb` (Test)
- `spec/services/spam/handler_spec.rb` (Test, shared)
- `spec/services/spam/domain_detector_spec.rb` (Test)
- `spec/services/slack/messengers/potential_spammer_spec.rb` (Test)

## Functional Overview

When an article is published or re-evaluated, the system runs a multi-layered spam detection pipeline. `LabelCleanupWorker` periodically identifies recently published articles that still carry the `no_moderation_label` and enqueues each for reprocessing via `HandleSpamWorker`. `HandleSpamWorker` calls `Spam::Handler.handle_article!`, which first uses an AI content-moderation labeler to classify the article; clear violations trigger an immediate spam reaction and potential user suspension, while high-quality labels bypass further checks entirely. For borderline articles the handler additionally checks rate-limit word patterns and, when an AI key is configured, invokes `Ai::ArticleCheck` to ask the AI model whether the article is clearly spam. If spam is confirmed and the author has accumulated too many prior spam reactions, the user is suspended. Independently, `Spam::DomainDetector` examines the author's email domain: if three or more accounts registered within the past two weeks from a non-popular domain are already marked spam or suspended — and no older legitimate account from that domain exists — the domain is flagged for bulk suspension via a background job. Throughout the pipeline, `Slack::Messengers::PotentialSpammer` can post an alert to the `potential-spam` Slack channel so moderators are notified in real time.

## Scenarios

### Periodic re-evaluation of unlabeled articles

1. `LabelCleanupWorker` runs on a schedule and queries for published articles that were published between 15 minutes and 12 hours ago, have a score above -80, and still carry the `no_moderation_label`.
2. Up to 75 articles are selected in random order.
3. A `HandleSpamWorker` job is enqueued for each selected article.

### Article receives a clear-violation label

1. `HandleSpamWorker` receives an article ID and loads the article.
2. `Spam::Handler.handle_article!` calls the AI content-moderation labeler, which sets the article's `automod_label` to `clear_and_obvious_spam`, `clear_and_obvious_harmful`, or `clear_and_obvious_inciting`.
3. The system immediately issues a spam ("vomit") reaction from the platform mascot account against the article.
4. If the author has already received too many spam reactions across their content, the user is suspended and an automatic-suspension note is created.
5. If the `unpublish_all_posts_when_user_auto_suspended` feature flag is active, all of the user's articles are unpublished.

### Article receives a high-quality label and bypasses spam checks

1. The AI content-moderation labeler assigns a positive label such as `very_good_and_on_topic` or `great_and_on_topic`.
2. `Spam::Handler.handle_article!` returns `:not_spam` immediately without evaluating rate-limit patterns or invoking `Ai::ArticleCheck`.

### Article fails rate-limit or AI-based spam detection

1. The article's label is not a clear violation and not a high-quality label.
2. `Spam::Handler` checks the article's title and body against rate-limit trigger terms.
3. If the article contains links and an AI key is available, `Ai::ArticleCheck` builds a prompt that includes the article content, the author's last 10 article titles, and the community description, then asks the AI model whether the article is clearly spam.
4. If either check indicates spam, a spam reaction is issued against the article.
5. If the author has accumulated too many spam reactions, the user is suspended.

### Domain-level spam pattern triggers domain block

1. After spam is detected for an article's author, `Spam::DomainDetector` extracts the domain from the user's email address.
2. Popular shared email providers (e.g., gmail.com, outlook.com) are immediately skipped.
3. The detector checks whether any user with the same domain registered more than two weeks ago; if so, the domain is considered legitimate and no action is taken.
4. If at least three recently registered accounts from that domain already carry spam or suspended roles, `Spam::BlockDomainAndSuspendUsersWorker` is enqueued to block the domain and suspend all associated users in the background.

### Slack alert for potential spammer

1. When the system determines a user may be a spammer, `Slack::Messengers::PotentialSpammer` is called with the user.
2. A message containing the user's profile URL is dispatched asynchronously to the `potential-spam` Slack channel under the `spam_account_checker_bot` identity.

## Design Intent

The pipeline is deliberately staged and escalating: AI content labels act as a fast first pass, allowing high-confidence decisions (clear violations or high quality) to short-circuit the rest of the checks. This avoids expensive AI calls for the majority of articles while ensuring the most harmful content is caught first. Rate-limit term matching is kept as a cheap secondary gate before the slower `Ai::ArticleCheck` call. Domain-level detection is kept separate so that a single spam article can trigger a broader sweep of coordinated spam campaigns without overloading the primary per-article flow. The 75-article cap and randomised selection in `LabelCleanupWorker` prevents runaway processing during high-traffic periods.

## Failures / Exceptions

- If the AI content-moderation labeler raises an error, `Spam::Handler` logs the error and sets `automod_label` to `no_moderation_label` as a safe default so the article is not incorrectly penalised.
- If `Ai::ArticleCheck#spam?` raises an error, it is rescued and returns `false`, meaning the article is treated as not spam in that check.
- If `HandleSpamWorker` cannot find the article by ID, it exits silently without calling any downstream services.
- If article enhancement (clickbait scoring, tag generation) raises an error inside `HandleSpamWorker`, the error is logged and suppressed so spam handling results are preserved.
- If a user's email address is blank or malformed, `Spam::DomainDetector` extracts `nil` as the domain and silently skips domain analysis.
