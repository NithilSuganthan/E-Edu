# BACKEND AUDIT — Inventobots Academy
Date: 26 Aug 2026. All findings verified against code + live DB + runtime tests.

## Authentication

### FIXED
1. **[CRITICAL] Student login leaked account existence + debug internals**
   - `parents/views.py::student_login_view` queried `User.objects.get(username=username)`
     on failure and displayed `"Debug: User 'X' does not exist."` /
     `"exists but password failed (Active: ...)"`. This is exactly the message reported;
     it always echoed the submitted username (the 'teststudent' string came from dev
     scripts/browser autofill — nothing hardcoded in the request path).
   - Also removed all `print("DEBUG LOGIN...")` calls.
   - Now: generic `"Invalid username or password."`; portal-mismatch message only when
     credentials are VALID but the account lacks a student profile.

2. **[HIGH] Wrong redirect target for logged-out students** — anonymous access to student
   pages redirected to the *parent* login. Fixed with `login_url='/parents/student/login/'`
   on all 10 student-only views (parent views unchanged).

### REMAINING (documented)
3. [MEDIUM] No rate limiting / lockout on login endpoints (Django default). Acceptable for demo; add `django-axes` before real users.
4. [MEDIUM] No password reset flow at all (no email backend configured).
5. [LOW] `add_student_view` creates student passwords without Django password validators.
6. [LOW] Several DB users have BOTH parent_profile and student_profile (test artifacts); role checks are profile-based so no bypass, but data hygiene could improve.
7. [INFO] User "Nithil" is a superuser with no student/parent profile — cannot log into either portal (by design).

## Authorization

### VERIFIED SAFE (tested)
- Parent A requesting Parent B's child detail → 404 (view scopes by `parent=request.user.parent_profile`). Tested.
- Lesson-complete API returns 403 without enrollment. Tested.
- Report download scoped by parent ownership. Code-reviewed.
- Alert read/report download/mark-alert all scope by parent. Code-reviewed.

### REMAINING
8. [MEDIUM] `/api/course/<id>/learn/` (CoursePlayerView) serves full lesson content to ANY authenticated student regardless of enrollment (progress tracking is enrollment-aware, content is not). Enrollment gate should be enforced server-side before charging for courses.

## Security

9. **[FIXED] Unvalidated profile image upload** — `student_settings_view` accepted arbitrary
   files as profile images (stored-XSS vector since media is same-origin). Now validates
   real image content (Pillow decode) + 5 MB limit. Tested: HTML-as-png rejected,
   valid PNG accepted.
10. [LOW] Razorpay success callback is `@csrf_exempt` — standard for gateway callbacks; signature IS verified before activating enrollment. OK.
11. [LOW] `SECRET_KEY` fallback hardcoded in settings (dev convenience). Production must set env var (documented).
12. [VERIFIED] No secrets exposed in templates/rendered HTML. CSRF tokens present on all POST forms checked.

## Database & Data Quality

13. [VERIFIED] All migrations applied; `makemigrations --check` clean; local PostgreSQL intact.
14. [MEDIUM] Legacy dual content hierarchy (`Topic`/`TopicProgress` AND `Subject→Module→Lesson`) increases complexity and query cost.
15. [LOW] ~15 leftover test users (`testUser_*`, `verify_user_*`) in dev DB. Not deleted (non-destructive policy).

## API

16. [LOW] `/api/login/` returns different messages for bad credentials vs success but does not leak existence — OK. DRF used only minimally; most "API" is Django views.

## Error Handling & Code Quality

17. **[FIXED] Debug `print()` statements removed** from auth/enrollment/player views.
18. [LOW] Broad `except Exception` blocks swallow error details in registration/payment flows (log-and-continue). Acceptable for demo; add logging later.
19. [LOW] `core_extras.get_item` filter made type-tolerant (was crashing course player for non-enrolled visitors).

## Performance

20. [MEDIUM] N+1 patterns:
    - `parent_dashboard_view`: per-student loop issues ~8 queries each.
    - `student_dashboard_view`: nested subject/module/lesson counts per enrollment.
    - Fine at current scale (<25 students); annotate before scaling.
21. [LOW] `CoursePlayerView` prefetches correctly — good as-is.

## Deployment Risks

22. [MITIGATED] Media served by Django in production (ephemeral disk on Render) — fine for short demo, documented.
23. [VERIFIED] App boots and passes regression under DEBUG=False (collectstatic: 305 files, WhiteNoise serving, media route working).
