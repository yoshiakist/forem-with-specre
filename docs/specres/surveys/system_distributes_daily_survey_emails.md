---
id: "01KJ2HPEMKQB5YCRAJ8PVF25SD"
name: "system_distributes_daily_survey_emails"
status: "draft"
---

## Related Files

- `app/workers/emails/survey_daily_email_worker.rb`
- `spec/workers/emails/survey_daily_email_worker_spec.rb` (Test)

## Functional Overview

`Emails::SurveyDailyEmailWorker` is a Sidekiq job that runs daily to distribute pulse survey invitation emails. It iterates over all active surveys that have a positive `daily_email_distributions` count, selects eligible users, randomly samples the configured number of recipients, and enqueues a `SurveyMailer#pulse_survey` email for each. The worker uses concurrency throttling (limit 1) and the `until_and_while_executing` lock to prevent overlapping runs.

## Design Intent

The eligibility pipeline filters users in the database rather than loading all users into memory. For surveys that do not allow resubmission, the worker excludes any user who has already interacted with the survey in any way — completions, votes, skips, or text responses — ensuring that only fresh, uninvolved users are reached. Random sampling is performed via `ORDER BY RANDOM() LIMIT N` in PostgreSQL, providing a uniform distribution without needing application-level shuffling.

## Key Members

- `sidekiq_throttle(concurrency: { limit: 1 })` — ensures only one instance of this worker runs at a time
- `sidekiq_options queue: :low_priority, retry: 5, lock: :until_and_while_executing` — runs on the low-priority queue with up to 5 retries and an execution lock
- `User.email_eligible` — scope returning users who have opted in to receiving emails
- `last_presence_at >= 3.months.ago` — limits recipients to users active within the last 3 months
- `survey.daily_email_distributions` — integer set by the admin, controlling how many emails are sent per day for this survey

## Scenarios

### Daily distribution for a survey without resubmission

1. The worker runs and finds an active survey with `daily_email_distributions: 50` and `allow_resubmission: false`.
2. It loads email-eligible users active in the last 3 months.
3. It excludes users who have a `SurveyCompletion` record for this survey.
4. It further excludes users who have any `PollVote`, `PollSkip`, or `PollTextResponse` for any poll in this survey.
5. From the remaining pool, it randomly samples 50 users via `ORDER BY RANDOM() LIMIT 50`.
6. For each sampled user, it enqueues `SurveyMailer.with(user: user, survey: survey).pulse_survey.deliver_later`.

### Daily distribution for a survey with resubmission allowed

1. The worker finds an active survey with `allow_resubmission: true`.
2. It loads email-eligible users active in the last 3 months without excluding prior respondents.
3. It randomly samples the configured number of users and enqueues emails for each.

### Survey with zero distribution count

1. The worker loads an active survey with `daily_email_distributions: 0`.
2. The initial query (`WHERE daily_email_distributions > 0`) excludes this survey entirely; no processing occurs.

### No eligible users remain

1. All email-eligible, recently active users have already interacted with the survey.
2. The exclusion filters remove all candidates; `sampled_users` is empty.
3. No emails are enqueued.

## Failures / Exceptions

- If the worker fails (e.g., database connection error), Sidekiq retries up to 5 times as configured.
- The concurrency throttle and execution lock prevent duplicate runs from sending duplicate emails in the event of overlapping scheduling.
