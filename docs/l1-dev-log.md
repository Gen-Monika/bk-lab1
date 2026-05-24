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

- Visiting `/user/` or `/post/` can fail before a corresponding `WeChatUser` record exists. This is expected for the course demo.
- After logging in, use `/admin/` to add a `WeChatUser` and bind it to the current BlueKing user before testing post submission.
