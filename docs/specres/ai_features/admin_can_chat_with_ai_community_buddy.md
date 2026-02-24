---
id: "01KJ6SZXEKKJCHRY9A615KYNKV"
name: "admin_can_chat_with_ai_community_buddy"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/ai_chats_controller.rb`
- `app/services/ai/chat_service.rb`
- `app/views/ai_chats/index.html.erb` (Template)
- `spec/controllers/ai_chats_controller_spec.rb` (Test)
- `spec/services/ai/chat_service_spec.rb` (Test)

## Functional Overview

Admins can access an AI-powered chat interface called "Community Buddy" that provides personalized advice grounded in their recent community activity. The controller enforces both authentication and admin role before serving the chat page or processing messages. Each chat request passes the admin's message along with the full client-side conversation history to `Ai::ChatService`, which builds a context-rich prompt from the user's recently published articles, recently viewed articles, and reading list. The service sends this prompt to the Google Gemini API via `Ai::Base` and returns the AI reply, which is rendered from Markdown to HTML before being sent back to the browser. The frontend maintains conversation history locally and handles a typing indicator, disabled input during requests, and error display.

## Design Intent

Conversation history is maintained client-side and re-sent with every request. This keeps the server stateless and avoids any server-side session or database storage for chat history, at the cost of growing payload size over a long conversation.

The AI prompt is enriched with the user's actual community data (written, viewed, and saved articles) so the AI can give contextually relevant advice without requiring the user to describe their interests manually.

## Key Members

- `history` — array of `{ role, text }` pairs sent from the client and echoed back with each response; grows by two entries per exchange
- `Ai::ChatService#prompt` — assembles up to 10 authored articles, 20 recently viewed articles, and 10 reading-list articles into the system prompt sent to the API

## Scenarios

### Admin views the chat interface

1. An authenticated admin navigates to the AI chat page (`GET /ai_chats`).
2. The controller confirms the user is logged in and holds an admin role.
3. The chat interface is rendered, showing a greeting message from the Community Buddy.

### Admin sends a message and receives a personalized reply

1. The admin types a message and submits the chat form.
2. The browser disables the input, appends the user message to the conversation, and shows a typing indicator.
3. The browser posts the message and the current conversation history to `POST /ai_chats`.
4. The controller creates an `Ai::ChatService` with the current user and the supplied history.
5. The service fetches the user's recent authored articles, viewed articles, and reading list, then builds a prompt combining that context with the conversation history.
6. The service calls the Gemini API and appends both the user message and the AI reply to the history.
7. The controller converts the AI reply from Markdown to HTML and returns `{ message, history }` as JSON.
8. The browser removes the typing indicator, appends the rendered reply, and updates its local history copy.

### Non-admin is blocked from the chat interface

1. An authenticated user without an admin role requests `GET /ai_chats`.
2. The controller redirects them to the root path with an authorization alert.
3. For JSON requests to `POST /ai_chats`, the controller returns HTTP 401 Unauthorized instead of redirecting.

### Unauthenticated user is redirected to sign in

1. A visitor who is not logged in requests any action on `AiChatsController`.
2. Devise's `authenticate_user!` before-action redirects them to the sign-in page.

### Message is blank

1. An admin submits a POST request with a blank or missing message.
2. The controller detects the blank value before calling the chat service.
3. It returns HTTP 422 Unprocessable Entity with `{ error: "Message cannot be blank" }`.

## Failures / Exceptions

- If the Gemini API call raises a `StandardError` (network failure, API error, malformed response), the controller rescues it, logs the error, and returns HTTP 500 with `{ error: "Something went wrong. Please try again." }`.
- If the browser fetch itself fails (no network), the frontend catches the rejection and displays an inline error message without updating the conversation history.
