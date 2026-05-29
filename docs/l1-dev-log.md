# L1 WeChat Moments Development Log

Date: 2026-05-25

## Summary

Implemented the L1 sample SaaS feature based on the BlueKing Django framework: a simple WeChat Moments app with profile, moments list, and post submission pages.

## Changes

- Added the `moments` Django app to `INSTALLED_APPS`.
- Added `WeChatUser` and `Status` models.
- Registered `WeChatUser` and `Status` in Django admin.
- Added app routes for `/`, `/user/`, `/status/`, and `/post/`.
- Added views for the homepage, user profile, moments list, and post submission.
- Added Bootstrap-based templates under `moments/templates/moments/`.
- Added course static assets under `moments/static/`.
- Enabled `/admin/` for the lab workflow.
- Added `BK_STATIC_URL` support in staging and production settings so static files work under the BlueKing app path prefix.
- Added `.DS_Store` to `.gitignore`.

## Database

- Generated migration `moments/migrations/0001_initial.py`.
- Applied the migration to the local MySQL database.

## Verification

- `python manage.py makemigrations moments`: OK
- `python manage.py migrate`: OK
- `python manage.py check`: OK
- `python manage.py test moments`: OK
- Django template loading check for all `moments` templates: OK

## Notes

- These notes describe the first L1 implementation. They were superseded by the CialloChat upgrade below.
- The upgraded version creates and switches in-app `ChatUser` accounts directly, so manual `WeChatUser` binding is no longer part of the normal workflow.

## CialloChat Upgrade

Date: 2026-05-25

### Summary

Upgraded the original WeChat demo into CialloChat, a more complete in-app social feed that keeps BlueKing login as the outer platform access control and uses database-backed CialloChat accounts inside the application.

### Changes

- Renamed the user-facing product from WeChat to CialloChat.
- Added in-app account registration, login, logout and profile editing.
- Added a default course administrator account through a database migration.
- Added real moments posting with preset images and uploaded images.
- Added real likes and comments with database persistence.
- Added content deletion permissions for owners and administrators.
- Added a CialloChat admin panel for feed moderation.
- Added user action logging middleware for request behavior collection.
- Added selected visual assets and a redesigned responsive UI.
- Added README documentation and expanded automated tests.

### Maintenance Notes

- Default administrator credentials are documented in README for course demonstration.
- Production-like deployments can override the administrator password with `CIALLO_ADMIN_PASSWORD`.
- Visual assets are curated rather than copied in full.

## CialloChat Interaction Polish

Date: 2026-05-25

### Summary

Added a small interaction-focused iteration after local QA: richer avatar/background choices, clearer like-member display, and threaded comment replies.

### Changes

- Added Nene and Meguru themed avatar choices from the course picture set.
- Renamed the lighthouse background options so their labels match the actual scenery.
- Added the feather sky background to the profile background selector.
- Upgraded the moment feed to display like members with avatars.
- Upgraded comments to show commenter avatar and timestamp.
- Added one-level replies so users can reply to a selected comment.

### Verification

- Added automated coverage for the new asset choices, like-member rendering, and comment reply flow.

## Uploaded Image Persistence Fix

Date: 2026-05-27

### Summary

Fixed a deployment persistence issue where user-uploaded moment images could disappear after a BlueKing rebuild because they were stored only in the container media directory.

### Changes

- Added a database-backed uploaded image data URL field for moments.
- Converted new uploaded images to data URLs during post submission.
- Kept the old media file field as a compatibility fallback for existing records.
- Updated the feed template and README to describe the deployment-safe storage behavior.

### Verification

- Added automated coverage confirming uploaded images are rendered from database data URLs.

## Frontend Feature Guide

Date: 2026-05-29

### Summary

Added a paged Help guide to the CialloChat frontend so course evaluators can review implemented base and extended features directly from the application.

### Changes

- Added a `Help` button to the navigation bar.
- Added a first-visit guide modal for the main frontend page using `localStorage` so it opens once and can be reopened manually.
- Added guide pages for the moments feed, post and upload flow, likes and threaded replies, profile customization, and administrator moderation.
- Added compressed guide screenshots under `moments/static/ciallo/help/`.

### Verification

- Parsed the updated Django template successfully.
- Checked the embedded guide JavaScript syntax with `node --check`.
