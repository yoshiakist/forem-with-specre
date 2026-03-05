---
id: "01KJ9H0CVY83030EB96383B8GA"
name: "admin_uploads_image_via_admin_panel"
status: "draft"
---

## Related Files

- `app/javascript/admin/controllers/image_upload_controller.js`
- `app/views/admin/shared/_image_uploader.html.erb` (Template)

## Functional Overview

Provides admins with a simple image upload tool accessible from the Developer Tools section of the admin panel. The admin selects an image file using a file picker that accepts any image type, then submits the form. A Stimulus controller intercepts the submission, sends the image to the server via a `FormData` POST request with CSRF protection, and on success reveals the hosted image URL in a read-only text field along with a thumbnail preview. If the upload fails for any reason, an error alert is displayed instead.

## Design Intent

This is a quick-upload utility designed so admins can obtain a hosted image URL without leaving the admin panel. The form submission is intercepted by a Stimulus controller rather than using a standard HTML form POST, allowing the result to be rendered inline on the same page instead of navigating away. The image result area is hidden until a successful upload occurs, keeping the interface uncluttered.

## Key Members

- `fileFieldTarget` — the file input element; holds the selected image file
- `imageResultTarget` — the hidden container that becomes visible and displays the URL and preview after a successful upload
- `urlValue` — the POST endpoint URL, passed from the server-rendered template via a Stimulus value attribute
- `onFormSubmit(event)` — intercepts the form submit event, builds `FormData`, and dispatches the fetch request
- `onUploadSuccess(result)` — reveals the result area and renders the image URL text field and a thumbnail
- `onUploadFailure(error)` — calls `displayErrorAlert` with the error message

## Scenarios

### Admin uploads a valid image successfully

1. Admin navigates to the Developer Tools section of the admin panel, which renders the image uploader partial.
2. Admin clicks the file picker, selects an image file (any `image/*` type), and clicks "Upload".
3. The Stimulus controller intercepts the form submit, builds a `FormData` payload containing the CSRF token and the selected file, and sends a POST request to `image_uploads_path`.
4. The server returns a JSON response containing a `links` field with the hosted image URL.
5. The controller calls `onUploadSuccess`, removes the `hidden` class from the result container, and renders the hosted image URL in a read-only text field and a 300px-wide thumbnail preview.

### Admin upload fails due to a server-side error

1. Admin selects an image and clicks "Upload".
2. The server returns a JSON response containing an `error` field.
3. The controller throws an error and calls `onUploadFailure`, which invokes `displayErrorAlert` with the error message.
4. An error alert is displayed; the image result area remains hidden.

### Admin upload fails due to a network or fetch error

1. Admin selects an image and clicks "Upload".
2. The fetch request rejects due to a network failure or non-JSON response.
3. The promise chain catches the error and calls `onUploadFailure`, which invokes `displayErrorAlert` with the error message.
4. An error alert is displayed; the image result area remains hidden.
