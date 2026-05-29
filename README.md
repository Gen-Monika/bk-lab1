# CialloChat

CialloChat is a BlueKing Django SaaS course project. It keeps BlueKing as the outer platform login and implements an in-app social account system backed by the project database.

## Features

- In-app CialloChat accounts with registration, login, profile editing, avatar and background selection.
- Default course administrator account for content management.
- Moments feed with real post creation, preset images, uploaded images, likes, comments and deletion permissions.
- Django admin integration for users, moments, comments, likes and behavior logs.
- User action logging middleware that records request method, path, status code, BlueKing user and current CialloChat user.
- Responsive UI with CialloChat branding and curated course demo visual assets.
- Paged Help guide with feature screenshots. The guide opens once on the main frontend page and can be reopened from the navigation bar.

## Account Model

BlueKing login remains the outer SaaS access control. Inside the app, CialloChat uses `ChatUser` records for social identities. A visitor who has passed BlueKing login enters as the default administrator unless they switch to another CialloChat account.

Default course administrator:

```text
username: admin
password: admin123456
```

For deployment, the administrator password can be overridden with:

```text
CIALLO_ADMIN_PASSWORD=your-strong-password
```

## Main Routes

- `/status/`: Moments feed
- `/post/`: Create a moment
- `/user/`: Edit current CialloChat profile
- `/login/`: Switch in-app account
- `/register/`: Create in-app account
- `/admin-panel/`: CialloChat content moderation panel
- `/admin/`: Django admin

## Local Development

Use Python 3.11.10 and install dependencies from `requirements.txt`.

```bash
uv pip install -r requirements.txt
python manage.py migrate
python manage.py runserver dev.ce.bktencent.com:8001
```

Local secrets and database settings belong in `dev.env` and `local_settings.py`; they are intentionally ignored by Git.

## Verification

Recommended checks before deployment:

```bash
python manage.py makemigrations --check
python manage.py migrate
python manage.py check
python manage.py test moments
```

## Deployment Notes

The BlueKing app descriptor runs database migrations in the `preRelease` hook:

```text
python manage.py migrate --no-input
```

Uploaded moment images are encoded into database-backed data URLs so user posts survive BlueKing container rebuilds and repeated deployments. Preset visual assets are stored under `moments/static/ciallo/`.

The feature guide uses compressed screenshots stored under `moments/static/ciallo/help/` so the course evaluator can quickly review the implemented base and extended functions from the frontend.

## Asset Notice

Visual assets are used only for course experiment demonstration. Copyright belongs to the original rights holders. The repository intentionally includes only selected assets needed by the demo instead of the full source material collection.
