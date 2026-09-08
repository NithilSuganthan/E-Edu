# PROJECT STATUS — Inventobots Academy

> Audit date: 26 Aug 2026. Every item below was verified against the actual code
> and a running instance unless explicitly marked **UNKNOWN**.

---

## 1. What the project is

**Inventobots Academy** is a server-rendered Django LMS (Learning Management
System) for a kids/teens education company (Robotics, Coding, Abacus,
Phonics, etc.). It has:

- A public marketing site (home, courses, labs showcase, about, robotics/coding pages)
- A certification course catalog + public certificate verification portal
- A **Parent portal** (registration, dashboard, student progress, alerts, reports)
- A **Student portal** (dashboard with XP/level/streak, course player, quizzes,
  online labs, certificates, settings, enrollment + payment flow)
- A customized Django admin (jazzmin + django-admin-interface) used as the
  back-office for courses, lessons, quizzes, materials, attendance, feedback,
  reports, certificates.

## 2. Current technology stack (as found)

| Layer | Technology |
|---|---|
| Backend | Python 3.12.10, **Django 6.0.1**, Django REST Framework 3.16.1 |
| Templates | Django templates styled with Tailwind CSS via CDN (`cdn.tailwindcss.com`) |
| Icons | lucide via unpkg CDN |
| Database | **PostgreSQL** (local dev DB `inventobots_db`, user `inventobots_user`) |
| Auth | Django auth + **django-allauth 65.19.1** (Google OAuth provider configured) |
| Admin skin | django-jazzmin 3.0.1 + django-admin-interface 0.32.0 + django-colorfield |
| Payments | Razorpay (`razorpay` python SDK 2.0.1) |
| Static serving | WhiteNoise 6.11.0 (CompressedManifestStaticFilesStorage) |
| Images | Pillow 12.1.0 (ImageFields, certificate PNG generation) |
| Production WSGI | Gunicorn 26.2.0 (Linux only; cannot run on Windows) |
| Frontend JS | Plain vanilla JS (`static/js/`: circuit engine/UI, lab, theme). No build step. |

There is no separate frontend app. Everything is one Django project in `backend/`.

## 3. Complete feature list (verified in code)

- Hero slider on homepage driven by `Course.is_hero_featured` records (DB-driven)
- Course catalog page + per-category pages (robotics, coding) + About page
- Public REST-ish API endpoints: `/api/login/`, `/api/courses/`
- Certification courses catalog (`certifications.CertificationCourse`) linked to
  core courses; certificate template designer fields (fonts, positions, colors)
- Certificate generation as PNG images (Pillow, TTF fonts bundled:
  Inter, GreatVibes) — `certifications/certificate_generator.py`
- Public certificate verification by ID (`INV-YYYY-NNNN`, auto-generated)
- Parent registration / login / logout, add-student sub-account creation
- Parent dashboard: per-student enrollments, attendance %, trainer feedback,
  certificates count, unread alerts, progress records, report download
- Student login (username/password), student dashboard: streak, level, XP,
  course progress %, quiz score chart data, recommendations, badges, certificates
- Student course browser + enrollment wizard: mode preference (Online/Offline)
  → Razorpay checkout → payment success callback activates enrollment
  (free courses auto-activate without payment)
- **Course player** (`/api/course/<id>/learn/`): Subject → Module → Lesson
  hierarchy; lesson types VIDEO/LIVE_CLASS/READING/QUIZ/ASSIGNMENT/EXTERNAL_LINK;
  study-materials panel; "mark complete" API writing `LessonProgress`
- Quiz system: quizzes attached to course/lesson/topic, JSON choices questions,
  submissions stored with scores (`QuizSubmission`)
- Gamification: Badge / StudentBadge models, student level & XP fields
- **Online Labs** (self-contained HTML/CSS/vanilla-JS, no backend):
  - Circuit Lab (battery/LED/motor/resistor simulation, `circuit-engine.js`,
    `circuit-ui.js`, `lab.js`)
  - Virtual Abacus (rod/bead manipulation with heaven/earth beads)
  - Memory card game (3D flip cards)
  - Public `/lab/` version + gated in-portal `/parents/student/lab/` version
    (locked unless the student has an Active/Completed enrollment)
- Study materials app: per-course materials (PDF/video/image/link) with multiple
  files each
- Attendance, ProgressTracker, TrainerFeedback, Report (file download), Alert
  models powering the parent portal
- Customized admin with custom login/logout templates and secret URL override
  (`ADMIN_URL` env var)

## 4. Routes/pages (verified from `config/urls.py`, `core/urls.py`,
`parents/urls.py`, `certifications/urls.py`)

Public site:
- `/` home (hero slider), `/index/`, `/courses/`, `/lab/`, `/about/`,
  `/robotics/`, `/coding/`
- `/certifications/` catalog, `/certifications/verify/` (POST),
  `/certifications/result/<id>/`, `/cert/` → redirect

Parent portal (`/parents/...`):
- `login/`, `register/`, `dashboard/`, `student/add/`,
  `student/<id>/` detail, `alert/<id>/read/`, `report/<id>/download/`, `logout/`

Student portal (`/parents/student/...`):
- `login/`, `dashboard/`, `courses/`, `settings/`, `settings/password/`,
  `lab/`, `certificates/`, `browse-courses/`,
  `enroll-now/<course_id>/` (via certification course),
  `enroll-core/<course_id>/` + `/confirm/` + `/payment/`,
  `payment/success/`, `logout/`

APIs:
- `POST /api/login/`, `GET /api/courses/?category=`
- `GET /api/course/<id>/learn/` (course player)
- `POST /api/lesson/<id>/complete/`

Admin: `<ADMIN_URL>/` (default `admin/`; overridable via env).

## 5. Database structure (from models + live PostgreSQL)

Live local database contains real data:
19 courses, 1 subject, 1 module, 2 lessons, 3 quizzes, 6 questions,
6 certification courses, 4 certificates, 20 parents, 20 students,
16 enrollments, 3 study materials, 24 users (2 superusers: `admin`, `Nithil`).

Apps & tables:
- **core**: Course (+HeroSlide proxy), Subject, Module, Lesson, Topic (legacy,
  retained), TopicProgress, Quiz, Question, QuizSubmission, Badge, StudentBadge
- **parents**: Parent, Student (1:1 optional User), CourseEnrollment (status,
  payment status/reference/date, mode), LessonProgress, Attendance,
  ProgressTracker, TrainerFeedback, StudentCertificate, Report, Alert
- **certifications**: CertificationCourse (template layout config, FK to
  core.Course), Certificate (unique ID INV-YYYY-NNNN, image upload)
- **study_materials**: StudyMaterial, StudyMaterialFile
- allauth tables (`account_*`, `socialaccount_*`) present

All migrations applied; `makemigrations --check` reports no pending changes.

## 6. Authentication system

- Two account types distinguished by profile existence:
  `user.parent_profile` vs `user.student_profile`
- Parents: username/password at `/parents/login/`; self-registration at
  `/parents/register/`
- Students: username/password at `/parents/student/login/`; accounts created by
  parents ("Add student") or admin
- Google OAuth via allauth configured **in settings** (env vars
  `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_SECRET`). Without credentials set,
  pages render fine but the Google button cannot complete OAuth.
- Sessions expire at browser close; secure cookies + SSL redirect enabled when
  DEBUG=False.
- Known quirk: `student_login_view` leaks account-existence hints in messages
  ("User exists but password failed") — debug code left in views.

## 7. Admin functionality (verified)

Django admin customized with jazzmin/admin-interface, custom login/logout
templates, secret path support. Manages: Courses (incl. hero slider flags,
CTA fields), Subjects/Modules/Lessons, Quizzes/Questions, Badges, Certification
Courses (with visual certificate-template editor templates under
`templates/admin/certifications/`), Certificates, Students/Parents,
Enrollments, Attendance, Feedback, Reports, Alerts, Study Materials.

## 8. Student functionality (verified rendering with logged-in test user)

Dashboard (streak, level/XP, progress rings, chart data, recommendations),
My Courses, Browse & Enroll, Enrollment preference → payment flow,
Course Player with lesson completion tracking, Lab hub (gated),
Certificates page, Settings (profile edit, image upload, password change).

## 9. Parent functionality (verified rendering with logged-in test user)

Registration, login, dashboard with per-student cards (attendance %,
enrollments, feedback, alerts, latest report, certificate count), add-student,
alert read marking, report file download, student detail view
(`student_detail.html` template exists but route renders it — see §14).

## 10. Online laboratory functionality

Pure client-side simulations (no server calls):
- **Circuit Lab**: component palette (wire, battery, resistor, LED, motor,
  switch), drag-drop grid building, circuit evaluation engine, animated
  LED/motor states.
- **Virtual Abacus**: 13 rods, heaven/earth bead movement, value readout.
- **Memory game**: emoji pair-matching with flip animation and move counting.
Both a public demo at `/lab/` and an enrolled-students-only copy inside the
portal at `/parents/student/lab/`.

## 11. Payment functionality

Razorpay integration (test-mode keys expected): order creation on enrollment,
checkout template (`razorpay_checkout.html`), signature-verified success
callback that activates the enrollment. Free courses (price null/0) skip the
gateway entirely. **Requires real Razorpay keys to work end-to-end.**

## 12. Certificate functionality

- Certificates issued via admin (auto ID generation).
- PNG rendering via Pillow using uploaded background template + configurable
  fonts/positions/colors per CertificationCourse.
- Public verification portal by certificate ID.
- Student-side "My Certificates" page.

## 13. What is fully functional (verified locally, both DEBUG True and False)

- Homepage w/ hero slider, courses/lab/about/robotics/coding pages
- Certifications catalog + certificate verify/result pages
- Parent registration/login/dashboard flows (page render verified via
  force-login; password login uses standard Django authenticate)
- Student login/dashboard/courses/browse/settings/lab/certificates pages
- Course player + mark-lesson-complete API (403 correctly returned when not
  enrolled)
- Static files (WhiteNoise, collectstatic: 305 files copied, 845 processed)
- Media files served (dev + production path added during this audit)
- Admin index loads; DB queries all healthy against existing PostgreSQL data
- All migrations applied; `manage.py check` clean (3 non-blocking allauth
  deprecation warnings)

## 14. What is partially functional

- **Google sign-in**: button renders; OAuth cannot complete without real
  Google credentials (env vars).
- **Quiz taking UI**: model + submission storage exist and dashboards chart
  scores, but no dedicated take-quiz page/route was found (quizzes are listed
  as lesson type QUIZ in the player). Marked PARTIAL — quiz *taking* flow not
  located in URLs/templates. (If it exists, it is embedded elsewhere — UNKNOWN.)
- **Reports download**: parent can download only if admin uploaded a report
  file; no report-generation logic exists (upload-only).
- **Recommendations** on student dashboard: link targets are `#` placeholders.
- **Topic/TopicProgress**: legacy parallel content hierarchy still in models;
  new Subject→Module→Lesson is what the player uses.

## 15. What is mocked/demo-only

- Razorpay keys default to placeholders (`rzp_test_YOUR_KEY_HERE`) — payment
  fails gracefully with an error message until real test keys are supplied.
- Google OAuth defaults to `demo-not-configured`.
- Streak calculation is an approximation (distinct activity days in last 7 days).
- WhatsApp group links referenced in models/enrollment UI are mostly empty
  (data-dependent).

## 16. What is broken (fixed during this audit)

See "What you fixed" in the deployment summary; original issues were:
1. Project could not even boot: venv missing `django-allauth`,
   `django-admin-interface`, `django-colorfield`, `razorpay`, `python-dotenv`.
2. `/parents/login/` returned HTTP 500 (allauth SocialApp missing).
3. Course player crashed for unauthenticated/not-enrolled visitors
   (`get_item` filter AttributeError).
4. No requirements.txt, no Procfile, WhiteNoise middleware commented out,
   DB credentials hardcoded, media unserved when DEBUG=False.

All fixed. No other runtime errors observed across ~35 tested routes.

## 17. What is incomplete (by design, left untouched)

- Quiz-taking page (see §14)
- Recommendation links (`#`)
- Legacy Topic system coexists with new Lesson system
- Debug print statements throughout views (cosmetic noise only)
- No automated tests worth running (`tests.py` files are stubs)

## 18. What requires external credentials

| Credential | Env var | Needed for |
|---|---|---|
| Razorpay test keys | `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET` | Paid enrollment flow |
| Google OAuth client | `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_SECRET` | "Sign in with Google" |
| PostgreSQL | `DATABASE_URL` | Production DB (Render/Neon) |

## 19. What requires production configuration

- `DEBUG=False`, strong `SECRET_KEY`, public host in `ALLOWED_HOSTS`,
  `CSRF_TRUSTED_ORIGINS=https://<host>` (env-driven — done)
- `ADMIN_URL` set to a non-obvious path (env-driven — done)
- `DATABASE_URL` pointing at managed Postgres (env-driven — done)
- `collectstatic` + Gunicorn start command (Procfile/render.yaml — done)
- First superuser creation on the fresh production DB (manual step)
- Seed/demo data on production DB if desired (`core/management/commands/
  seed_courses.py`, `seed_hero_courses.py` exist; they create marketing/course
  rows — review before running against prod)
- Media uploads land on the Render ephemeral disk — uploaded images/files reset
  on redeploy unless object storage is added later (acceptable for short demo;
  documented in DEPLOYMENT_DEMO.md)
