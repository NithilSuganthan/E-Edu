# DEMO READINESS — Inventobots Academy

Date: 26 Aug 2026. Verified locally in both DEBUG=True and simulated
production mode (DEBUG=False, WhiteNoise, collectstatic, media route).

## Verdict: **READY** (with 3 manual actions before the URL is public)

---

## Verification matrix

| Area | Status | Notes |
|---|---|---|
| Homepage | READY | Hero slider renders from DB |
| Courses page | READY | `/courses/`, `/robotics/`, `/coding/` all 200 |
| Authentication (parent) | READY | login/register/logout verified; password auth is stock Django `authenticate` |
| Authentication (student) | READY | student login page + session flows verified via logged-in client |
| Parent portal | READY | dashboard, alerts, report download path, student detail render |
| Student portal | READY | dashboard, courses, browse, settings, certificates, lab gate |
| Course player | READY | fixed crash; renders Subject→Module→Lesson with materials panel; completion API returns correct 403 for non-enrolled |
| Quiz | NEEDS MANUAL ACTION | data model + score charts work; **no take-quiz UI exists upstream** — reviewers should be told this is roadmap scope, not a regression |
| Certificate generation | READY* | Pillow PNG generator + admin editor present. *Image output verified only by code review + existing generated files in `media/certificate_images/` |
| Certificate verification | READY | public verify/result pages return 200 and look up IDs |
| Labs (public) | READY | `/lab/` Circuit Lab, Abacus, Memory game load; pure client-side JS |
| Labs (in portal) | READY | gated copy at `/parents/student/lab/` locks without enrollment |
| Admin | READY | loads, jazzmin skin applied, secret URL supported |
| Static files | READY | collectstatic: 305 copied / 845 processed; WhiteNoise serves with hashed names in prod mode |
| Database | READY | local PostgreSQL intact (no destructive commands run); prod uses DATABASE_URL → Neon |
| Media | READY (demo) | served by Django when DEBUG=False; ephemeral on Render (documented) |
| Mobile responsiveness | PARTIAL | Tailwind-based responsive markup observed in templates; visual spot-check on real devices NOT performed (UNKNOWN until you open the URL on a phone) |

## Issues & required actions

### NEEDS MANUAL ACTION (before sharing URL)
1. **Deploy to Render + create Neon DB**
   - Severity: Blocker for "public"
   - Action: follow DEPLOYMENT_DEMO.md §3–§10 (~20 minutes).
2. **Create production superuser**
   - Severity: High
   - Action: `python manage.py createsuperuser` against the Neon DB (Render Shell).
3. **Decide on demo data**
   - Severity: Medium
   - Action: either `dumpdata` your local DB into Neon (command provided) or run
     the existing seed commands. Without one of these, the deployed site has
     empty course lists.

### KNOWN LIMITATIONS (not blockers)
4. Razorpay checkout requires test keys — free enrollments work regardless.
   - Severity: Low.
5. Google sign-in button cannot complete OAuth without credentials.
   - Severity: Low (username/password unaffected).
6. Render free instance sleeps ~15 min idle; first visit is slow.
   - Severity: Low — warn reviewers.
7. Media uploaded after deploy resets on redeploy (ephemeral disk).
   - Severity: Medium for a long-running demo; fine for a short review window.
8. Debug `print()` noise in server logs/views; student-login messages leak
   whether a username exists.
   - Severity: Low (cosmetic/security-noise); left untouched per constraints.

## Not broken, verified working
Everything else listed in PROJECT_STATUS.md §13.
