# DEPLOYMENT_DEMO — Temporary Public Demo on Render + Neon

Goal: put the **existing** Inventobots Academy online (free tier) so an external
software company can review it. No redesign, no new features.

---

## 1. Hosting provider — Render (free web service)
- Simplest option for a single Django app; supports `render.yaml` IaC, free TLS,
  auto-deploy from Git.
- Free tier caveats (verify current limits at deploy time): service sleeps after
  ~15 min idle (first request slow ~30–60s), 512 MB RAM, ephemeral disk.
- Alternative if you prefer: Railway / PythonAnywhere — not configured here.

## 2. Database provider — Neon PostgreSQL (free tier)
- Create a project at neon.tech → copy the connection string
  (`postgresql://user:pass@ep-xxx.aws.neon.tech/neondb?sslmode=require`).
- Neon free tier: ~0.5 GB storage, autosuspend. Sufficient for a demo.

## 3. Required environment variables (set in Render dashboard)

| Variable | Value |
|---|---|
| `DEBUG` | `False` |
| `SECRET_KEY` | random string (Render can generate) |
| `ALLOWED_HOSTS` | `your-app.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `https://your-app.onrender.com` |
| `ADMIN_URL` | a private path, e.g. `review-admin-7x9/` |
| `DATABASE_URL` | the Neon connection string |
| `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` | your Razorpay *test* keys (optional) |
| `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_SECRET` | optional (Google login button) |
| `PYTHON_VERSION` | `3.12.10` |

All of these are already wired into `backend/config/settings.py`. Placeholders
are documented in `backend/.env.example`.

## 4. Build command
```
pip install -r requirements.txt && python manage.py collectstatic --noinput
```

## 5. Start command
```
gunicorn config.wsgi:application --workers 2 --bind 0.0.0.0:$PORT
```
(Procfile included; render.yaml also included at repo root with rootDir=backend.)

## 6. Required deployment settings
Already applied in code:
- WhiteNoise middleware + CompressedManifestStaticFilesStorage
- `DATABASE_URL` parsing (urllib-based, no extra dependency), sslmode via `DB_SSLMODE`
- Media served by Django in production mode (temporary demo approach, see §9)
- Secure cookies / SSL redirect auto-enable when `DEBUG=False`

## 7. Database migration command
Run once against the Neon database (or use Render `preDeployCommand`, already set):
```
python manage.py migrate
```
This creates an empty schema. It does **not** touch your local PostgreSQL data.

To copy your existing local demo data to Neon instead of starting empty:
```
# local machine:
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission -e sessions -e admin.logentry -o data.json
# then, with DATABASE_URL pointing to Neon:
python manage.py loaddata data.json
```

Optional seed commands that exist in the repo:
- `python manage.py seed_courses` and `python manage.py seed_hero_courses`
(review their contents first; they create course/marketing rows).

## 8. Static file command
```
python manage.py collectstatic --noinput
```
(Already part of the build command.)

## 9. Media storage requirements
Current setup stores uploads on local disk (`backend/media`). Render's free disk
is **ephemeral**: images/materials uploaded after deploy disappear on redeploy or
restart.
- For this short review period: acceptable. Pre-existing media committed/pushed
  with the repo will be present (media/ is currently gitignored — see §14 note).
- If you need uploaded media to survive during the review: add a paid persistent
  disk (not required) or object storage later. Nothing was added now to avoid
  unnecessary infrastructure.
- Features affected without persistent media: admin image uploads, student
  profile photos, study-material file uploads (reset on redeploy). Everything
  already shipped with the code works fine.

## 10. How to create the first admin account
After the first deploy, from Render Shell (or locally with DATABASE_URL set):
```
python manage.py createsuperuser --username <you> --email <you@example.com>
```
Use a strong password. The admin lives at `https://<your-app>.onrender.com/<ADMIN_URL>/`.

## 11. How to test the deployed website
1. Open `https://<host>/` — homepage hero slider loads.
2. `/courses/`, `/lab/` (Circuit Lab, Abacus, Memory game all client-side),
   `/about/`, `/robotics/`, `/coding/`.
3. `/certifications/` → verify a certificate ID from the DB.
4. `/parents/register/` → create parent → add student → log in as student.
5. `/parents/student/browse-courses/` → enroll (free courses activate instantly;
   paid ones need Razorpay test keys).
6. `/api/course/43/learn/` (course player) — only for enrolled students.
7. Admin: create a Certificate, then verify it publicly.
8. Mobile: pages are Tailwind responsive; spot-check on a phone.

## 12. Known limitations
- Free instance sleeps (~30–60 s cold start).
- Ephemeral media (§9).
- Quiz-taking UI is not implemented upstream (quizzes exist as data + scores).
- Google sign-in needs real OAuth credentials; password login unaffected.
- Razorpay checkout needs test keys; free enrollment works without keys.
- Debug `print()` statements remain in views (cosmetic).
- Tailwind/lucide load from public CDNs (needs internet on reviewer side).

## 13. Free-tier limitations
- Render free plan: no persistent disk, limited RAM/workers, spin-down idle.
- Neon free plan: autosuspend on inactivity (first query reconnects), storage cap.
- These are provider terms today — re-check both pricing pages before deploying;
  nothing in this repo assumes a feature that must be purchased.

## 14. Shutting down / removing the demo
- Render Dashboard → your web service → **Settings → Delete** (or Suspend).
- Neon Console → delete the project/database.
- Local development is untouched throughout (local PostgreSQL + venv stay as-is).

Note on `media/`: it is in `.gitignore`. Your existing course/certificate images
live there. To make them appear on the demo, either force-add them
(`git add -f backend/media`) for the temporary demo or upload them again through
the admin after deploy. Choose deliberately — don't commit anything private.
