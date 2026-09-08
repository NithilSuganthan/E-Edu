# Inventobots Academy — Deployment Guide

---

## 1. Pre-Deployment Checklist

Before deploying to any platform, complete these steps:

| # | Task | Command / Action |
|---|------|-----------------|
| 1 | Set `DEBUG=False` | In `.env` or platform environment variables |
| 2 | Generate a strong `SECRET_KEY` | `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| 3 | Set `ALLOWED_HOSTS` | Add your domain: `yourdomain.com,www.yourdomain.com` |
| 4 | Add `CSRF_TRUSTED_ORIGINS` | Add to `settings.py`: `CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']` |
| 5 | Set up PostgreSQL | Create a production database (see Section 2) |
| 6 | Create `requirements.txt` | `pip freeze > requirements.txt` |
| 7 | Collect static files | `python manage.py collectstatic --noinput` |
| 8 | Run migrations | `python manage.py migrate` |
| 9 | Create admin superuser | `python manage.py createsuperuser` |

> [!CAUTION]
> **Never deploy with `DEBUG=True`** — it exposes sensitive error details, source code, and environment variables to the public.

---

## 2. Production Database (PostgreSQL)

All deployment platforms below support managed PostgreSQL. Here's how to configure it:

### Create the Database

```sql
CREATE DATABASE inventobots_db;
CREATE USER inventobots_user WITH PASSWORD 'strong_password_here';
ALTER ROLE inventobots_user SET client_encoding TO 'utf8';
ALTER ROLE inventobots_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE inventobots_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE inventobots_db TO inventobots_user;
```

### Update `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'inventobots_db'),
        'USER': os.getenv('DB_USER', 'inventobots_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
```

> [!TIP]
> Most platforms (Railway, Render) provide a single `DATABASE_URL`. You can use the `dj-database-url` package to parse it automatically. See platform-specific sections below.

---

## 3. Static Files & WhiteNoise

WhiteNoise lets Django serve static files in production without a separate web server.

### Install & Configure

```bash
pip install whitenoise
```

In `settings.py`, add WhiteNoise to middleware (after `SecurityMiddleware`):

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <— add here
    # ... rest of middleware
]
```

Add the storage backend:

```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Then collect static files:

```bash
python manage.py collectstatic --noinput
```

---

## 4. Create Required Files

### `requirements.txt`

Generate from your virtual environment:

```bash
pip freeze > requirements.txt
```

Your file should include at minimum:

```
Django==6.0.1
djangorestframework==3.16.1
django-jazzmin==3.0.1
django-cors-headers==4.9.0
psycopg2-binary==2.9.11
pillow==12.1.0
python-dotenv
whitenoise==6.11.0
gunicorn==23.0.0
```

### `Procfile` (for Railway & Render)

Create a `Procfile` in the `backend/` directory:

```
web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### `runtime.txt` (optional)

Specify the Python version:

```
python-3.12.0
```

---

## 5. Deploy to Railway

[Railway](https://railway.app) offers the simplest Django deployment experience.

### Step-by-Step

| Step | Action |
|------|--------|
| 1 | Push your code to a **GitHub repository** |
| 2 | Go to [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub** |
| 3 | Select your repository |
| 4 | Add a **PostgreSQL plugin** from the Railway dashboard |
| 5 | Set environment variables (see table below) |
| 6 | Set **Root Directory** to `backend` (in Service Settings) |
| 7 | Set **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |
| 8 | Deploy — Railway handles the rest |

### Environment Variables

Set these in the Railway dashboard under **Variables**:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | Your generated secret key |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `your-app.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.up.railway.app` |
| `DATABASE_URL` | Auto-provided by Railway PostgreSQL plugin |
| `SECURE_ADMIN_URL` | Your custom admin URL path |

### Using `DATABASE_URL`

Install `dj-database-url`:

```bash
pip install dj-database-url
```

Update `settings.py`:

```python
import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL)
    }
```

### Post-Deploy Commands

Run from the Railway shell or CLI:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## 6. Deploy to Render

[Render](https://render.com) offers free-tier Django hosting with managed PostgreSQL.

### Step-by-Step

| Step | Action |
|------|--------|
| 1 | Push code to **GitHub** |
| 2 | Go to [render.com](https://render.com) → **New** → **Web Service** |
| 3 | Connect your GitHub repository |
| 4 | Set **Root Directory** to `backend` |
| 5 | Set **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate` |
| 6 | Set **Start Command**: `gunicorn config.wsgi:application` |
| 7 | Add a **PostgreSQL database** from the Render dashboard |
| 8 | Set environment variables (same as Railway table above) |
| 9 | Deploy |

### Create a `render.yaml` (Optional — Blueprint)

Place in the project root for automated setup:

```yaml
services:
  - type: web
    name: inventobots-academy
    runtime: python
    rootDir: backend
    buildCommand: |
      pip install -r requirements.txt
      python manage.py collectstatic --noinput
      python manage.py migrate
    startCommand: gunicorn config.wsgi:application
    envVars:
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: "False"
      - key: DATABASE_URL
        fromDatabase:
          name: inventobots-db
          property: connectionString

databases:
  - name: inventobots-db
    plan: free
```

---

## 7. Deploy to PythonAnywhere

[PythonAnywhere](https://www.pythonanywhere.com) is well-suited for Django projects with a beginner-friendly interface.

### Step-by-Step

| Step | Action |
|------|--------|
| 1 | Sign up at [pythonanywhere.com](https://www.pythonanywhere.com) |
| 2 | Open a **Bash console** |
| 3 | Clone your repository (see commands below) |
| 4 | Set up virtual environment and install dependencies |
| 5 | Configure the **Web tab** |
| 6 | Set up static file mappings |
| 7 | Reload the web app |

### Console Commands

```bash
# Clone repository
git clone https://github.com/<your-username>/inventobots-academy.git
cd inventobots-academy

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Create .env file
nano .env
# Add: DEBUG=False, SECRET_KEY=..., ALLOWED_HOSTS=yourusername.pythonanywhere.com

# Run migrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Web Tab Configuration

| Setting | Value |
|---------|-------|
| **Source code** | `/home/yourusername/inventobots-academy/backend` |
| **Working directory** | `/home/yourusername/inventobots-academy/backend` |
| **Virtualenv** | `/home/yourusername/inventobots-academy/venv` |

### WSGI Configuration File

Edit the WSGI file (linked in the Web tab):

```python
import os
import sys

# Add project to path
path = '/home/yourusername/inventobots-academy/backend'
if path not in sys.path:
    sys.path.append(path)

# Load environment variables
from dotenv import load_dotenv
env_path = os.path.join(path, '.env')
load_dotenv(env_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Static File Mappings

Add these in the **Web tab** → **Static files** section:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/yourusername/inventobots-academy/backend/staticfiles` |
| `/media/` | `/home/yourusername/inventobots-academy/backend/media` |

---

## 8. Custom Domain Setup

After deploying, connect your custom domain:

| Platform | Steps |
|----------|-------|
| **Railway** | Settings → Domains → Add Custom Domain → Update DNS |
| **Render** | Settings → Custom Domains → Add Domain → Update DNS |
| **PythonAnywhere** | Web tab → Add a new web app with your domain (paid plan) |

### DNS Records to Add

| Type | Name | Value |
|------|------|-------|
| **CNAME** | `www` | `your-app.up.railway.app` (or platform URL) |
| **A** | `@` | Platform's IP address (if provided) |

> [!IMPORTANT]
> After adding a custom domain, update these in your environment:
> - `ALLOWED_HOSTS` — add your domain
> - `CSRF_TRUSTED_ORIGINS` — add `https://yourdomain.com`

---

## 9. SSL / HTTPS

| Platform | SSL |
|----------|-----|
| **Railway** | Automatic — free SSL via Let's Encrypt |
| **Render** | Automatic — free SSL via Let's Encrypt |
| **PythonAnywhere** | Automatic on paid plans; free plan has `*.pythonanywhere.com` SSL |

For production, add to `settings.py`:

```python
# HTTPS / Security Settings (only when DEBUG=False)
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
```

---

## 10. Post-Deployment Verification

After deployment, verify these pages load correctly:

| Page | URL | What to Check |
|------|-----|---------------|
| Homepage | `https://yourdomain.com/` | Hero slider, dark/light mode, course cards |
| Courses | `https://yourdomain.com/courses/` | Course catalog, filters, detail modals |
| About | `https://yourdomain.com/about/` | Team info, legal pages |
| Online Lab | `https://yourdomain.com/lab/` | Code Studio, Circuit Lab, games load |
| Certifications | `https://yourdomain.com/certifications/` | Certificate lookup form |
| Parent Login | `https://yourdomain.com/parents/login/` | Login form, CSRF token works |
| Admin Panel | `https://yourdomain.com/<admin-url>/` | Jazzmin theme, login works |
| Static Files | All pages | CSS, JS, images load correctly |
| Media Files | Admin uploads | Uploaded images display properly |

---

## 11. Maintenance & Updates

### Pushing Updates

```bash
git add .
git commit -m "description of changes"
git push origin main
```

Most platforms auto-deploy on push. Otherwise, trigger a manual deploy from the dashboard.

### Running Migrations After Updates

```bash
python manage.py migrate
```

### Backing Up the Database

```bash
# PostgreSQL backup
pg_dump -U inventobots_user inventobots_db > backup_$(date +%Y%m%d).sql

# Restore
psql -U inventobots_user inventobots_db < backup_file.sql
```

---

## 12. Environment Variables Reference

Complete list of environment variables used by the application:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Yes | Insecure default | Django secret key — **must change in production** |
| `DEBUG` | ✅ Yes | `False` | Set to `False` in production |
| `ALLOWED_HOSTS` | ✅ Yes | `127.0.0.1,localhost` | Comma-separated list of domains |
| `CSRF_TRUSTED_ORIGINS` | ✅ Yes | — | Full URLs: `https://yourdomain.com` |
| `SECURE_ADMIN_URL` | Recommended | `admin/` | Custom admin panel URL for security |
| `DATABASE_URL` | Platform-dependent | — | Full database connection string |
| `DB_NAME` | If no `DATABASE_URL` | `inventobots_db` | Database name |
| `DB_USER` | If no `DATABASE_URL` | `inventobots_user` | Database username |
| `DB_PASSWORD` | If no `DATABASE_URL` | — | Database password |
| `DB_HOST` | If no `DATABASE_URL` | `127.0.0.1` | Database host |
| `DB_PORT` | If no `DATABASE_URL` | `5432` | Database port |

---

*Document prepared by Nithil Suganthan — February 2026*
