# Inventobots Academy — Environment Configuration Guide

---

## 1. Overview

The application uses a `.env` file in the `backend/` directory to manage environment-specific settings. This keeps sensitive data (secret keys, database credentials) out of version control and makes it easy to switch between development and production configurations.

The `.env` file is loaded automatically by `python-dotenv` in `settings.py`. If `python-dotenv` is not installed, the app has a built-in fallback parser.

> **File location:** `backend/.env`

---

## 2. Environment Variables Reference

### Application Settings

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Yes (production) | Insecure dev key | Django secret key for cryptographic signing — sessions, CSRF, passwords |
| `DEBUG` | ✅ Yes | `False` | Set to `True` for development, **must be `False` in production** |
| `ALLOWED_HOSTS` | ✅ Yes | `127.0.0.1,localhost` | Comma-separated domains that can serve the app |
| `ADMIN_URL` | Recommended | `admin/` | Custom admin panel URL path (security measure) |

### Database Settings

These are configured directly in `settings.py` but can be moved to environment variables for production:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DATABASE_URL` | Optional | — | Full database connection string (requires `dj-database-url` package) |
| `DB_NAME` | If no `DATABASE_URL` | `inventobots_db` | PostgreSQL database name |
| `DB_USER` | If no `DATABASE_URL` | `inventobots_user` | PostgreSQL username |
| `DB_PASSWORD` | If no `DATABASE_URL` | — | PostgreSQL password |
| `DB_HOST` | If no `DATABASE_URL` | `127.0.0.1` | Database server host |
| `DB_PORT` | If no `DATABASE_URL` | `5432` | Database server port |

### Production-Only Settings

These should be added to `.env` or set in your hosting platform's environment when deploying:

| Variable | Value | Purpose |
|----------|-------|---------|
| `CSRF_TRUSTED_ORIGINS` | `https://yourdomain.com` | Required for CSRF protection with custom domains |

---

## 3. Development Configuration

Create `backend/.env` with the following for local development:

```env
# ==============================================
# Inventobots Academy — Development Environment
# ==============================================

# Application
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
ALLOWED_HOSTS=127.0.0.1,localhost

# Admin Panel (custom URL for security)
ADMIN_URL=super_secure_admin/

# Database (PostgreSQL)
DB_NAME=inventobots_db
DB_USER=inventobots_user
DB_PASSWORD=your_local_password
DB_HOST=127.0.0.1
DB_PORT=5432
```

---

## 4. Production Configuration

For production deployments, use these hardened settings:

```env
# ==============================================
# Inventobots Academy — Production Environment
# ==============================================

# Application
DEBUG=False
SECRET_KEY=your-strong-randomly-generated-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Admin Panel (use a hard-to-guess URL)
ADMIN_URL=my_secret_admin_panel_2026/

# Database (PostgreSQL — production)
DB_NAME=inventobots_db
DB_USER=inventobots_user
DB_PASSWORD=strong_production_password
DB_HOST=your-db-host.com
DB_PORT=5432

# OR use a single DATABASE_URL (Railway, Render, etc.)
# DATABASE_URL=postgresql://user:password@host:5432/dbname
```

---

## 5. Generating a Secret Key

Run this command to generate a cryptographically secure secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Example output:
```
a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4
```

Copy the output and set it as `SECRET_KEY` in your `.env` file.

---

## 6. Security Checklist

| Check | Development | Production |
|-------|-------------|------------|
| `DEBUG` | `True` ✅ | `False` ✅ |
| `SECRET_KEY` | Dev default OK | **Must be unique & random** |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | Your actual domain(s) |
| `ADMIN_URL` | Any value | **Non-obvious, hard-to-guess path** |
| Database password | Local password | **Strong, unique password** |
| `.env` in `.gitignore` | ✅ | ✅ |

> **Never commit the `.env` file to version control.** Always add it to `.gitignore`.

---

## 7. Platform-Specific Setup

### Railway / Render

Set environment variables in the platform dashboard instead of a `.env` file:

| Variable | Where to Set |
|----------|-------------|
| `SECRET_KEY` | Dashboard → Variables |
| `DEBUG` | Dashboard → Variables → `False` |
| `ALLOWED_HOSTS` | Dashboard → Variables → `your-app.up.railway.app` |
| `DATABASE_URL` | Auto-provided by the PostgreSQL plugin/addon |
| `ADMIN_URL` | Dashboard → Variables |

### PythonAnywhere

Create the `.env` file on the server:

```bash
nano /home/yourusername/inventobots-academy/backend/.env
```

Or set variables in the WSGI configuration file.

---

## 8. `.env.example` File

A `.env.example` file is included in the repository as a reference template. It contains all variable names with placeholder values but **no real secrets**. Copy it to create your actual `.env`:

```bash
cp .env.example .env
# Then edit .env with your actual values
```

---

*Document prepared by Nithil Suganthan — February 2026*
