# Inventobots Academy — Setup Guide

---

## 1. Prerequisites

Ensure the following are installed on your system before proceeding:

| Requirement | Version | Download |
|-------------|---------|----------|
| **Python** | 3.12+ | [python.org](https://www.python.org/downloads/) |
| **PostgreSQL** | 14+ | [postgresql.org](https://www.postgresql.org/download/) |
| **Git** | Latest | [git-scm.com](https://git-scm.com/downloads) |
| **pip** | Bundled with Python | Comes pre-installed |

> [!NOTE]
> SQLite can be used for quick local testing (see Database section), but PostgreSQL is recommended for production.

---

## 2. Clone the Repository

```bash
git clone https://github.com/<your-username>/inventobots-academy.git
cd inventobots-academy
```

---

## 3. Create & Activate Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt once activated.

---

## 4. Install Dependencies

```bash
pip install django==6.0.1
pip install djangorestframework==3.16.1
pip install django-jazzmin==3.0.1
pip install django-cors-headers==4.9.0
pip install psycopg2-binary==2.9.11
pip install pillow==12.1.0
pip install python-dotenv
pip install whitenoise==6.11.0
```

Or install all at once using the requirements file (if provided):

```bash
pip install -r requirements.txt
```

---

## 5. Environment Configuration

Create a `.env` file inside the `backend/` directory:

```bash
cd backend
```

Create or edit `.env` with the following variables:

```env
# General
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# Admin Panel URL (security measure — change in production)
SECURE_ADMIN_URL=super_secure_admin/

# Database (only needed if overriding defaults in settings.py)
# DB_NAME=inventobots_db
# DB_USER=inventobots_user
# DB_PASSWORD=your_db_password
# DB_HOST=127.0.0.1
# DB_PORT=5432
```

> [!IMPORTANT]
> **For production:** Always set `DEBUG=False`, use a strong unique `SECRET_KEY`, and update `ALLOWED_HOSTS` to your domain name.

### Generating a Secret Key

Run this command to generate a secure key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 6. Database Setup

### Option A: PostgreSQL (Recommended)

1. **Create the database and user** in the PostgreSQL shell (`psql`):

```sql
CREATE DATABASE inventobots_db;
CREATE USER inventobots_user WITH PASSWORD 'your_password';
ALTER ROLE inventobots_user SET client_encoding TO 'utf8';
ALTER ROLE inventobots_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE inventobots_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE inventobots_db TO inventobots_user;
```

2. **Update `backend/config/settings.py`** if your credentials differ from the defaults:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'inventobots_db',
        'USER': 'inventobots_user',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

### Option B: SQLite (Quick Testing Only)

Replace the `DATABASES` block in `settings.py` with:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 7. Run Migrations

From the `backend/` directory:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates all necessary database tables for the `core`, `parents`, and `certifications` apps.

---

## 8. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

You will be prompted for:
- **Username**
- **Email** (optional)
- **Password**

This account is used to access the Django Admin Panel.

---

## 9. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

This gathers all static assets (CSS, JS, images) into the `staticfiles/` directory for serving.

---

## 10. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:

| Page | URL |
|------|-----|
| **Homepage** | [http://127.0.0.1:8000/](http://127.0.0.1:8000/) |
| **Admin Panel** | [http://127.0.0.1:8000/super_secure_admin/](http://127.0.0.1:8000/super_secure_admin/) |
| **Courses** | [http://127.0.0.1:8000/courses/](http://127.0.0.1:8000/courses/) |
| **About** | [http://127.0.0.1:8000/about/](http://127.0.0.1:8000/about/) |
| **Online Lab** | [http://127.0.0.1:8000/lab/](http://127.0.0.1:8000/lab/) |
| **Certifications** | [http://127.0.0.1:8000/certifications/](http://127.0.0.1:8000/certifications/) |
| **Parent Portal** | [http://127.0.0.1:8000/parents/login/](http://127.0.0.1:8000/parents/login/) |

> [!TIP]
> The admin panel URL is configurable via the `SECURE_ADMIN_URL` variable in `.env` for security.

---

## 11. Project Structure

```
inventobots-academy/
├── backend/
│   ├── config/             # Django project settings, URLs, WSGI/ASGI
│   │   ├── settings.py     # Main configuration file
│   │   ├── urls.py         # Root URL routing
│   │   ├── wsgi.py         # WSGI entry point
│   │   └── asgi.py         # ASGI entry point
│   ├── core/               # Main app — courses, homepage, API, online lab
│   ├── parents/            # Parent portal — login, dashboard, reports
│   ├── certifications/     # Certificate issuance & public verification
│   ├── templates/          # All HTML templates (Django-rendered)
│   ├── static/             # Static assets (CSS, JS, images)
│   ├── staticfiles/        # Collected static files (auto-generated)
│   ├── media/              # User-uploaded files
│   ├── manage.py           # Django management script
│   └── .env                # Environment variables (not committed)
├── js/                     # Shared JavaScript files
├── venv/                   # Python virtual environment (not committed)
└── README.md
```

---

## 12. Deployment

The application is deployment-ready for any of the following platforms:

### Railway

1. Push code to GitHub
2. Connect repo to [Railway](https://railway.app)
3. Add environment variables in Railway dashboard
4. Railway auto-detects Django and deploys

### Render

1. Push code to GitHub
2. Create a new Web Service on [Render](https://render.com)
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn config.wsgi:application`
5. Add environment variables in Render dashboard

### PythonAnywhere

1. Upload code or clone from GitHub
2. Create a virtual environment and install dependencies
3. Configure WSGI file to point to `config.wsgi`
4. Set up static file mappings in the Web tab
5. Add environment variables in the WSGI configuration

> [!IMPORTANT]
> For all production deployments, ensure:
> - `DEBUG=False`
> - A strong `SECRET_KEY` is set
> - `ALLOWED_HOSTS` includes your domain
> - Static files are collected (`collectstatic`)
> - PostgreSQL is used as the database

---

## 13. Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Ensure virtual environment is activated and all packages are installed |
| Database connection error | Verify PostgreSQL is running and credentials in `settings.py` are correct |
| Static files not loading | Run `python manage.py collectstatic` and check `STATIC_ROOT` |
| Admin panel 404 | Check `SECURE_ADMIN_URL` in `.env` matches the URL you're visiting |
| CSRF errors on login | Ensure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` include your domain |
| Port already in use | Run on a different port: `python manage.py runserver 8080` |

---

*Document prepared by Nithil Suganthan — February 2026*
