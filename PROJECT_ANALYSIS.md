# PROJECT ANALYSIS — Inventobots Academy

> **Analysis Date:** July 2026  
> **Repository:** `V:\Inventobots`  
> **Developer:** Nithil Suganthan  

---

## 1. PROJECT OVERVIEW

### What It Does
Inventobots Academy is a **commercial EdTech (Learning Management System) web platform** sold as a ready-made product to training institutes and academies. It provides course management, student enrollment, parent/student portals, online lab tools, quiz/assessment engine, certification system, and an admin panel.

### Primary Purpose
Sell as a white-label LMS product to startup academies. The project documentation lists a price of ₹1,00,000 (≈$1,200 USD).

### Target Users
- **Students** (children) — access courses, labs, quizzes, certificates
- **Parents** — register children, track progress, attendance, payments
- **Admin/Trainers** — manage content, enrollments, certificates (via Django Admin + Jazzmin)
- **Public Visitors** — browse courses, verify certificates

### Main User Flows
1. **Public visitor** → Home → Browse Courses → Enroll → Payment (Razorpay)
2. **Parent** → Register → Add Student → Enroll in Course → Dashboard → Track Progress
3. **Student** → Login → Dashboard → Course Player → Lessons → Quizzes → Certificates
4. **Student** → Lab → Code Studio / Circuit Lab / Abacus / Memory Games
5. **Admin** → Django Admin → Course CRUD → Hero Slider → Certificates → Users

### Current Development Status
**Pre-deployment / Ready for sale.** The documentation says "Ready for deployment" (v1.0, Feb 2026). However, several issues indicate it is **not yet production-ready** without fixes.

### Features Status

| Feature | Status | Notes |
|---------|--------|-------|
| Public Homepage (Hero Slider) | COMPLETE | Dynamic, admin-configurable |
| Course Catalog | COMPLETE | Category filtering, detail modals |
| About / Legal Pages | COMPLETE | Static templates |
| Robotics / Coding Landing | COMPLETE | Static templates |
| Online Lab (Code Studio) | MOCKED | Simulated output, no real compilation |
| Online Lab (Circuit Lab) | COMPLETE | Client-side JS circuit simulator |
| Online Lab (Virtual Abacus) | COMPLETE | Interactive |
| Online Lab (Memory Games) | COMPLETE | 5 card games in lab.html |
| Parent Registration | COMPLETE | Username/password/email |
| Parent Login | COMPLETE | CSRF-protected |
| Parent Dashboard | COMPLETE | Multi-child tracking |
| Student Login | COMPLETE | Separate auth flow |
| Student Dashboard | COMPLETE | Progress, XP, badges, quizzes |
| Student Registration (by parent) | COMPLETE | Via parent dashboard |
| Course Enrollment | COMPLETE | With Razorpay payment |
| Course Player | COMPLETE | Subject > Module > Lesson hierarchy |
| Lesson Progress Tracking | COMPLETE | Auto-mark complete |
| Quiz Engine | COMPLETE | MCQs, scoring, submissions |
| Badge System | PARTIAL | Models + admin exist, auto-award logic not implemented |
| Attendance Tracking | COMPLETE | Admin record |
| Trainer Feedback | COMPLETE | Admin record |
| Report Generation | PARTIAL | Models exist, no auto-generation logic |
| Alert System | COMPLETE | Admin-push notifications |
| Certifications | COMPLETE | Issue, revoke, verify, image generation |
| Certificate Image Generation | COMPLETE | Pillow-based overlay on template |
| Google OAuth | PARTIAL | Allauth configured, untested |
| Razorpay Integration | COMPLETE | Checkout + webhook callback |
| REST API (DRF) | PARTIAL | Login + CourseList endpoints only |
| Study Materials | COMPLETE | Per-course file uploads |
| Subject/Module/Lesson Hierarchy | COMPLETE | Deep nested admin |
| Admin Panel (Jazzmin) | COMPLETE | Fully customized |
| WhiteNoise Static Serving | BROKEN | Commented out, missing package |
| Dark Mode | COMPLETE | Force-enabled, no toggle |

---

## 2. COMPLETE TECH STACK

| Technology | Where | Why |
|------------|-------|-----|
| **Django 6.0.1** | `backend/` | Web framework — all backend logic |
| **Python 3.12+** | `backend/` | Runtime language |
| **Django REST Framework 3.16.1** | `core/views.py` | JSON API for courses and login |
| **Django Jazzmin 3.0.1** | `settings.py` | Modern admin theme with sidebar |
| **django-admin-interface** | `settings.py` INSTALLED_APPS | Additional admin UI theming |
| **django-colorfield** | `settings.py` INSTALLED_APPS | Color picker fields in admin |
| **django-cors-headers 4.9.0** | `settings.py` | CORS headers middleware |
| **django-allauth** | `settings.py` | Google OAuth + account management |
| **django.contrib.sites** | `settings.py` | Required by allauth |
| **Tailwind CSS (CDN)** | All templates | Utility-first CSS via CDN script tag |
| **Alpine.js 3.x (CDN)** | All templates | Client-side reactivity (sliders, modals, tabs) |
| **Lucide Icons (CDN)** | All templates | SVG icon set (unpkg CDN) |
| **Google Fonts (Inter, Rajdhani, Poppins)** | `base.html`, `student_base.html` | Typography |
| **PostgreSQL** | `settings.py` | Production database (configured but pointing to localhost) |
| **SQLite** | `backend/db.sqlite3` | Development database (actually used) |
| **psycopg2-binary 2.9.11** | venv | PostgreSQL adapter |
| **Pillow 12.1.0** | `certificate_generator.py` | Certificate image generation |
| **Razorpay** | `parents/views.py` | Payment gateway (Indian market) |
| **WhiteNoise 6.11.0** | venv/installed, BUT COMMENTED OUT in middleware | Static file serving in production |
| **Gunicorn** | RECOMMENDED in docs (not in venv) | Production WSGI server |
| **gevent** | venv | Async worker pool (for gunicorn) |
| **python-dotenv** | `settings.py`, `manage.py`, `wsgi.py` | Load .env file |
| **dj-database-url** | RECOMMENDED in docs (not in venv) | Parse DATABASE_URL |
| **requests, tldextract, future** | venv | Various utility dependencies |

### Notable
- **No frontend build tool** (no webpack, vite, npm) — everything is CDN-loaded
- **No JavaScript framework** — vanilla JS + Alpine.js
- **No TypeScript**
- **No testing framework** beyond Django's built-in `tests.py` (mostly empty)
- **No CI/CD configuration**

---

## 3. COMPLETE PROJECT STRUCTURE

```
V:\Inventobots\
├── .vscode/
│   └── settings.json                          # Live Server port config
│
├── js/                                        # Shared JS files (served at /js/)
│   ├── theme.js                               # Dark mode force-enabler (Alpine.js data)
│   ├── circuit-engine.js                      # Circuit simulation engine (BFS-based)
│   └── circuit-ui.js                          # Circuit lab UI (SVG rendering, drag-drop)
│
├── backend/                                   # Django project root
│   ├── manage.py                              # Django CLI entry point
│   ├── .env                                   # Environment variables (COMMITTED - RISK)
│   ├── .env.example                           # Template for env vars
│   ├── db.sqlite3                             # SQLite dev database
│   │
│   ├── config/                                # Django project configuration
│   │   ├── __init__.py
│   │   ├── settings.py                        # ALL settings (DB, apps, middleware, etc.)
│   │   ├── urls.py                            # Root URL routing
│   │   ├── wsgi.py                            # WSGI application (production entry)
│   │   └── asgi.py                            # ASGI application
│   │
│   ├── core/                                  # Courses, content, quizzes, badges, API
│   │   ├── __init__.py
│   │   ├── apps.py                            # AppConfig
│   │   ├── models.py                          # Course, HeroSlide, Subject, Module, Lesson,
│   │   │                                     # Topic, TopicProgress, Quiz, Question,
│   │   │                                     # QuizSubmission, Badge, StudentBadge
│   │   ├── admin.py                           # All admin registrations (CourseAdmin, etc.)
│   │   ├── views.py                           # HomeView, LoginView, CourseListView,
│   │   │                                     # CoursePlayerView, MarkLessonCompleteView
│   │   ├── urls.py                            # /api/* endpoints
│   │   ├── serializers.py                     # CourseSerializer (DRF)
│   │   ├── tests.py                           # Empty
│   │   ├── templatetags/
│   │   │   ├── __init__.py
│   │   │   └── core_extras.py                 # Custom template filter: get_item
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── seed_courses.py            # Seed sample courses/topics/quizzes
│   │   │       └── seed_hero_courses.py       # Seed hero slider courses
│   │   └── migrations/                        # 11 migration files
│   │
│   ├── parents/                               # Parent & Student portal
│   │   ├── __init__.py
│   │   ├── apps.py                            # AppConfig (loads signals)
│   │   ├── models.py                          # Parent, Student, CourseEnrollment,
│   │   │                                     # Attendance, LessonProgress,
│   │   │                                     # ProgressTracker, TrainerFeedback,
│   │   │                                     # StudentCertificate, Report, Alert
│   │   ├── admin.py                           # All admin registrations (15+ classes)
│   │   ├── views.py                           # All portal views (848 lines)
│   │   ├── urls.py                            # /parents/* routes (29 patterns)
│   │   ├── signals.py                         # Progress tracking → enrollment updates
│   │   │                                     # → certificate generation
│   │   ├── tests.py                           # Empty
│   │   └── migrations/                        # 7 migration files
│   │
│   ├── certifications/                        # Certificate system
│   │   ├── __init__.py
│   │   ├── apps.py                            # AppConfig (loads signals)
│   │   ├── models.py                          # CertificationCourse, Certificate
│   │   ├── admin.py                           # Admin with visual template editor
│   │   ├── views.py                           # Index, verify, result
│   │   ├── urls.py                            # /certifications/* routes
│   │   ├── signals.py                         # Auto-generate certificate on completion
│   │   ├── certificate_generator.py           # Pillow-based image generator
│   │   ├── tests.py                           # Empty
│   │   ├── fonts/                             # TTF fonts for certificate generation
│   │   └── migrations/                        # 9 migration files
│   │
│   ├── study_materials/                       # Per-course study material files
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py                          # StudyMaterial, StudyMaterialFile
│   │   ├── admin.py                           # Inline admin
│   │   ├── views.py                           # Empty (no views)
│   │   ├── tests.py                           # Empty
│   │   └── migrations/                        # 2 migration files
│   │
│   ├── templates/                             # All HTML templates
│   │   ├── base.html                          # Public site layout with header/footer
│   │   ├── index.html                         # Homepage with hero slider
│   │   ├── courses.html                       # Course catalog page
│   │   ├── lab.html                           # Public lab page (non-student)
│   │   ├── course_player.html                 # Course content player with lessons
│   │   ├── about.html                         # About/legal page
│   │   ├── robotics.html                      # Robotics landing
│   │   ├── coding.html                        # Coding landing
│   │   ├── student_base.html                  # Student portal layout with sidebar
│   │   ├── student_dashboard.html             # Student dashboard
│   │   ├── student_courses.html               # My courses
│   │   ├── student_lab.html                   # Student lab (1234 lines)
│   │   ├── student_settings.html              # Profile settings
│   │   ├── student_browse_courses.html        # Browse & enroll
│   │   ├── student_certificates.html          # Student certificate list
│   │   ├── student_enrollment_preference.html # Online/offline choice
│   │   ├── components/
│   │   │   └── lab_styles.html                # Shared lab styles
│   │   ├── admin/
│   │   │   ├── login.html                     # Custom admin login
│   │   │   └── logout.html                    # Custom admin logout
│   │   ├── registration/
│   │   │   └── logged_out.html                # Post-logout page
│   │   └── parents/
│   │       ├── dashboard.html                 # Parent dashboard
│   │       ├── login.html                     # Parent login
│   │       ├── parent_register.html           # Parent registration
│   │       ├── student_login.html             # Student login
│   │       ├── student_register.html          # Student self-register
│   │       ├── razorpay_checkout.html          # Razorpay payment page
│   │       └── student_detail.html            # NEEDS VERIFICATION
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── admin_theme.css                # Custom admin login styling
│   │   ├── js/
│   │   │   ├── theme.js                       # Dark mode enabler
│   │   │   ├── lab.js                         # Lab Alpine.js data (coding, abacus)
│   │   │   ├── circuit-ui.js                  # Circuit lab UI handler
│   │   │   ├── circuit-engine.js              # Circuit simulation engine
│   │   │   └── circuit-components.js          # Component registry & SVG renders
│   │   └── Logo.png                           # Site logo
│   │
│   ├── media/                                 # User uploads directory
│   ├── staticfiles/                           # Collectstatic output dir
│   │
│   ├── debug_seed.py                          # Debug seeding script
│   ├── debug_course.py                        # Debug script
│   ├── debug_error.txt                        # Error log (NOT NULL violation)
│   ├── seed_log.txt                           # Seeding log
│   ├── schema.txt                             # DB schema dump (binary)
│   ├── fix_db.py                              # DB fix script
│   ├── inspect_course_columns.py              # Column inspection
│   ├── download_fonts.py                      # Font downloader
│   ├── create_superuser_script.py             # Superuser creation
│   ├── create_test_students.py                # Test student creation
│   ├── verify_login.py                        # Login verification script
│   ├── verify_lms.py                          # LMS verification
│   ├── verify_enrollment.py                   # Enrollment verification
│   ├── verify_automation.py                   # Automation verification
│   └── verify_output.txt                      # Verification output
│
├── venv/                                      # Python virtual environment
│
├── PROJECT_OVERVIEW.md                        # Quick overview doc
├── PROJECT_DOCUMENTATION.md                   # Full project documentation
├── FEATURES_AND_MODULES.md                    # Feature list
├── SETUP_GUIDE.md                             # Setup instructions
├── DEPLOYMENT_GUIDE.md                        # Deployment instructions
├── ENVIRONMENT_CONFIG.md                      # Environment variable guide
├── ADMIN_MANUAL.md                            # Admin user manual
├── QUOTATION.md                               # Pricing & quotation
├── Logo.png                                   # Project logo
└── (no .gitignore, no .git/, no requirements.txt, no Procfile, no Dockerfile)
```

---

## 4. FRONTEND ARCHITECTURE

### Pages
- **Public site**: Home, Courses, About, Robotics, Coding, Lab, Certifications + Result
- **Student portal**: Dashboard, My Courses, Browse Courses, Lab, Settings, Certificates
- **Parent portal**: Login, Register, Dashboard, Student Detail
- **Admin**: Django Admin (Jazzmin themed)

### Routes
Django server-rendered templates; no client-side routing.

### Components
- `base.html` — shared header, footer, nav, mobile bottom nav, dark mode
- `student_base.html` — sidebar layout, mobile tabs, user profile
- Alpine.js components within templates (hero slider, course filters, lab tools)

### State Management
- Alpine.js `x-data` per-component / per-page
- No global state store
- Dark mode is forced via `theme.js` (always dark, no toggle)

### API Communication
- `core/views.py` provides two DRF API endpoints
- Templates communicate with the API via standard Django form posts and template context
- No SPA-style fetch/axios usage

### Authentication Flow
1. **Parent**: Login form → `authenticate()` → check `parent_profile` → redirect dashboard
2. **Student**: Login form → `authenticate()` → check `student_profile` → redirect student dashboard
3. **Registration**: Parent registers → auto-login → add students → enroll courses
4. **Session-based** (Django sessions), no JWT
5. Google OAuth via allauth is configured but untested

### Forms
All HTML forms with Django CSRF tokens. No Django Forms/ModelForms used — raw `request.POST` handling.

### Error Handling
- `messages.error()` / `messages.success()` for user feedback
- Try/except around Razorpay calls
- Debug print statements scattered throughout views
- Empty exception handlers in signals (`pass` on DoesNotExist)

### Loading States
Minimal spinner/loading states. The code studio shows a `Compiling...` message with `setTimeout`. No skeleton loaders.

### Responsive Design
- Full responsive via Tailwind breakpoints
- Mobile bottom navigation
- `pb-safe` for iOS safe areas
- `overflow-y-auto` scrollable areas

### Accessibility
- Basic semantic HTML
- No ARIA attributes
- No keyboard navigation optimization
- No focus management
- No screen reader testing evident

### Performance Considerations
- CDN-loaded libraries (no bundling) — multiple HTTP requests
- No code splitting
- No lazy loading for images
- Template rendering is server-side (good for SEO)
- Large templates (student_lab.html: 1234 lines)

### Major Frontend Features
- Dynamic hero slider with autoplay + progress bar
- Course catalog with category filtering + detail modals
- Subject/Module/Lesson tree navigation in course player
- Code Studio (mock — no real compilation)
- Circuit Lab (fully client-side with SVG rendering + BFS simulation)
- Virtual Abacus
- 5 Memory/Card Games
- Certificate verification lookup
- Razorpay checkout page

---

## 5. BACKEND ARCHITECTURE

### Backend Entry Point
- **WSGI**: `config/wsgi.py` — `application = get_wsgi_application()`
- **ASGI**: `config/asgi.py` — `application = get_asgi_application()`
- **Settings**: `config/settings.py`
- **URL routing**: `config/urls.py` (root)

### API Endpoints Table

| Method | Route | Purpose | Auth Required |
|--------|-------|---------|---------------|
| POST | `/api/login/` | Authenticate user, start session | No |
| GET | `/api/courses/` | List all courses (with optional `?category=` filter) | No |
| GET | `/api/course/<id>/learn/` | Course player page with hierarchy + progress | Optional (full data for enrolled) |
| POST | `/api/lesson/<id>/complete/` | Mark lesson complete | Yes (student) |
| GET | `/` | Homepage with hero slider | No |
| GET | `/courses/` | Course catalog page | No |
| GET | `/about/` | About page | No |
| GET | `/lab/` | Public lab page | No |
| GET | `/robotics/` | Robotics landing | No |
| GET | `/coding/` | Coding landing | No |
| GET | `/certifications/` | Certificate lookup | No |
| POST | `/certifications/verify/` | Verify certificate by ID | No |
| GET | `/certifications/result/<id>/` | Certificate result page | No |
| GET | `/parents/login/` | Parent login page | No |
| POST | `/parents/login/` | Parent login action | No |
| GET | `/parents/student/login/` | Student login page | No |
| POST | `/parents/student/login/` | Student login action | No |
| GET | `/parents/register/` | Parent registration | No |
| POST | `/parents/register/` | Parent registration action | No |
| GET | `/parents/dashboard/` | Parent dashboard | Yes (parent) |
| GET | `/parents/student/dashboard/` | Student dashboard | Yes (student) |
| GET | `/parents/student/courses/` | Student courses | Yes (student) |
| GET | `/parents/student/lab/` | Student lab | Yes (student) |
| GET | `/parents/student/settings/` | Student settings | Yes (student) |
| POST | `/parents/student/settings/` | Update student profile | Yes (student) |
| POST | `/parents/student/settings/password/` | Change password | Yes (student) |
| GET | `/parents/student/browse-courses/` | Browse all courses | Yes (student) |
| GET | `/parents/student/enroll-core/<id>/` | Enrollment preference | Yes (student) |
| POST | `/parents/student/enroll-core/<id>/confirm/` | Confirm enrollment | Yes (student) |
| GET | `/parents/student/enroll-core/<id>/payment/` | Razorpay checkout | Yes (student) |
| POST | `/parents/student/payment/success/` | Razorpay callback | No (csrf_exempt) |
| GET | `/parents/student/certificates/` | Student certificate list | Yes (student) |
| GET | `/parents/student/<id>/` | Student detail (parent view) | Yes (parent) |
| GET | `/parents/logout/` | Parent logout | No |
| GET | `/parents/student/logout/` | Student logout | No |
| GET | `/admin/...` | Django Admin (Jazzmin) | Yes (staff) |
| GET | `/accounts/...` | Allauth URLs (Google OAuth, etc.) | Varies |

### Controllers / Views
Django function-based views + class-based views (`TemplateView`, `APIView`). All in `core/views.py` and `parents/views.py`.

### Services
No dedicated service layer — logic is in views.py files. Certificate generation is in `certifications/certificate_generator.py`.

### Middleware
- SecurityMiddleware
- SessionMiddleware
- CorsMiddleware
- CommonMiddleware
- CsrfViewMiddleware
- AuthenticationMiddleware
- MessageMiddleware
- XFrameOptionsMiddleware
- Allauth AccountMiddleware

### Authentication & Authorization
- Django's built-in `django.contrib.auth`
- Session-based (no JWT)
- Role checks via `hasattr(user, 'parent_profile')` or `hasattr(user, 'student_profile')`
- `@login_required` decorator on protected views
- Allauth for Google OAuth (configured in settings)

### Validation
Minimal server-side validation. Most forms validate in view logic (check password length, check username uniqueness via DB queries).

### Error Handling
- try/except around Razorpay
- `messages.error()` for user feedback
- Signals silently pass on `DoesNotExist`

### Background Jobs
- None implemented. Certificate generation runs synchronously during request.
- No Celery, no Redis, no task queue.

### Scheduled Tasks
- None. No cron jobs.

### WebSockets
- None. No real-time features.

### External API Integrations
- **Razorpay** — payment order creation + signature verification
- **Google OAuth** — configured in allauth (untested in codebase)
- **WhatsApp** — static link (wa.me) in templates, not dynamic API

---

## 6. DATABASE ARCHITECTURE

### Database Provider
- **Configured:** PostgreSQL (`django.db.backends.postgresql`)
- **Actually used:** SQLite (`backend/db.sqlite3`) — local dev file exists
- **Production target:** PostgreSQL (via Neon, Railway, Render)

### ORM
Django ORM throughout.

### All Detected Tables/Models

#### Core App (`core/models.py`)

| Model | Key Columns | Relationships |
|-------|-------------|---------------|
| `Course` | id, title, description, image, image_url, thumbnail, price, category, badge, subtitle, tagline, highlights (JSON), color_gradient, is_hero_featured, display_order, cta_primary_url/text, cta_secondary_url/text, created_at, duration (int), total_offline_classes, syllabus, mode, start_date, certification_details, notes | FK to Subject, Module, Lesson, Topic, Quiz, StudyMaterial |
| `HeroSlide` | Proxy model of Course | `is_hero_featured=True` |
| `Subject` | id, course (FK), title, description, order | FK → Course |
| `Module` | id, subject (FK), title, description, order | FK → Subject |
| `Lesson` | id, module (FK), title, lesson_type, order, video_url, live_link, whatsapp_link, file_upload, content_text, external_link, is_preview, duration_minutes | FK → Module |
| `Topic` (deprecated) | id, course (FK), title, description, order, video_url, resources | FK → Course |
| `TopicProgress` | id, student (FK), topic (FK), is_completed, time_spent_minutes, last_accessed | FK → Student, Topic |
| `Quiz` | id, course (FK), lesson (FK nullable), topic (FK nullable), title, description, time_limit_minutes, passing_score | FK → Course, Lesson, Topic |
| `Question` | id, quiz (FK), text, choices (JSON), correct_answer, explanation | FK → Quiz |
| `QuizSubmission` | id, student (FK), quiz (FK), score, answers (JSON), submitted_at | FK → Student, Quiz |
| `Badge` | id, name, description, image, criteria | — |
| `StudentBadge` | id, student (FK), badge (FK), earned_at | FK → Student, Badge (unique_together) |

#### Parents App (`parents/models.py`)

| Model | Key Columns | Relationships |
|-------|-------------|---------------|
| `Parent` | id, user (FK→User), phone_number, address, emergency_contact | 1:1 with User |
| `Student` | id, parent (FK), user (FK→User nullable), full_name, date_of_birth, grade_level, enrollment_date, profile_image, level (int), xp (int), is_active | FK → Parent, nullable FK → User |
| `CourseEnrollment` | id, student (FK), course (FK→core.Course), enrollment_date, status, mode, completion_percentage, current_level, is_manually_modified, last_activity_date, payment_status, payment_reference, payment_date | FK → Student, FK → Course (unique_together: student, course) |
| `LessonProgress` | id, student (FK), lesson (FK→core.Lesson), status, watched_percentage, completed_at, last_accessed | FK → Student, Lesson (unique_together) |
| `Attendance` | id, student (FK), course (FK), lesson (FK nullable), date, status, notes | FK → Student, Course, Lesson |
| `ProgressTracker` | id, student (FK), course (FK), skill_name, proficiency_level, score, last_updated | FK → Student, Course |
| `TrainerFeedback` | id, student (FK), course (FK), trainer_name, feedback_date, feedback_text, rating, category | FK → Student, Course |
| `StudentCertificate` | id, student (FK), certificate (FK→Certificate), awarded_date, status | FK → Student, Certificate |
| `Report` | id, student (FK), report_type, period_start, period_end, report_file, generated_date, notes | FK → Student |
| `Alert` | id, student (FK), alert_type, message, severity, is_read, created_at | FK → Student |

#### Certifications App (`certifications/models.py`)

| Model | Key Columns | Relationships |
|-------|-------------|---------------|
| `CertificationCourse` | id, name, description, duration, level, price, image, core_course (FK→core.Course), whatsapp_group_link, certificate_template (image), font_family, name_position_x/y, name_font_size, name_color, detail_font_family, detail_font_size, detail_color, course_position_x/y, date_position_x/y, certid_position_x/y | FK → core.Course (nullable) |
| `Certificate` | id, certificate_id (unique, auto-generated INV-YYYY-NNNN), student_name, course (FK→core.Course), issue_date, issued_by, status, certificate_image | FK → core.Course |

#### Study Materials App (`study_materials/models.py`)

| Model | Key Columns | Relationships |
|-------|-------------|---------------|
| `StudyMaterial` | id, course (FK), title, description, material_type, file, video_url | FK → core.Course |
| `StudyMaterialFile` | id, study_material (FK), file, description | FK → StudyMaterial |

### Key Relationships
```
User ──1:1──> Parent ──1:N──> Student ──1:N──> CourseEnrollment ──N:1──> Course
                                 │                    │
                                 ├──1:N──> LessonProgress ──N:1──> Lesson
                                 ├──1:N──> TopicProgress ──N:1──> Topic
                                 ├──1:N──> QuizSubmission ──N:1──> Quiz
                                 ├──1:N──> StudentBadge ──N:1──> Badge
                                 └──1:N──> StudentCertificate ──N:1──> Certificate

Course ──1:N──> Subject ──1:N──> Module ──1:N──> Lesson
Course ──1:N──> Topic (deprecated)
Course ──1:N──> Quiz ──1:N──> Question
Course ──1:N──> StudyMaterial ──1:N──> StudyMaterialFile
Course ──1:1──> CertificationCourse (via core_course FK)
CertificationCourse ──1:N──> Certificate (via course FK on Certificate)
```

### Indexes
- `certificate_id` on Certificate: unique, db_index=True
- `unique_together` on: StudentBadge, TopicProgress, QuizSubmission (no), CourseEnrollment, LessonProgress, Attendance

### Constraints
- `Course.duration` has `default=0` (NOT NULL) — the debug_error.txt shows a NOT NULL violation when duration was omitted
- Various `default` values and `blank=True, null=True` for optional fields

### Migrations
- `core/`: 11 migrations (0001 through 0011)
- `parents/`: 7 migrations (0001 through 0007)
- `certifications/`: 9 migrations (0001 through 0009)
- `study_materials/`: 2 migrations (0001, 0002)

### Seed Data
- `seed_courses.py` creates 3 sample courses (Python, Robotics, Abacus) with topics and quizzes
- `seed_hero_courses.py` creates hero slider data

### Database Communication
Django ORM via `models.py`. Connection configured in `settings.py` DATABASES. The `CONN_MAX_AGE=60` for connection pooling.

### Neon PostgreSQL Compatibility
**YES, compatible.** The project uses standard PostgreSQL via psycopg2. Neon provides a standard PostgreSQL connection string. The deployment guide recommends `dj-database-url` to parse `DATABASE_URL`, which works with Neon. No database-specific extensions are used.

---

## 7. AUTHENTICATION AND SECURITY

### Registration
- **Parent**: Username + password + email, creates Django User + Parent profile
- **Student**: Created by parent via `add_student_view()` — creates Django User + Student profile
- Manual superuser creation via `manage.py createsuperuser`

### Login
- Session-based authentication (`django.contrib.auth`)
- Separate login views for parents and students
- Checks `hasattr(user, 'parent_profile')` or `hasattr(user, 'student_profile')` after auth

### Logout
- `logout()` from `django.contrib.auth`
- Separate logout views

### Password Handling
- Django's `set_password()` and `check_password()` (PBKDF2 + bcrypt via settings)
- Password change via `update_session_auth_hash()`

### Sessions
- Django database-backed sessions
- `SESSION_EXPIRE_AT_BROWSER_CLOSE = True`
- `SESSION_COOKIE_SECURE = not DEBUG`

### JWT
**Not used.** All authentication is session-based.

### Cookies
- Session cookie + CSRF cookie
- `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` are set based on DEBUG

### OAuth
- Google OAuth configured via django-allauth
- `SOCIALACCOUNT_PROVIDERS` configured in settings.py
- Google client ID/secret need to be set via admin or env vars (NEEDS VERIFICATION)

### Role-Based Access Control
- Custom check: `hasattr(user, 'parent_profile')` for parent routes
- Custom check: `hasattr(user, 'student_profile')` for student routes
- `@login_required` decorator on protected views
- `user.is_staff` for admin panel

### Admin Permissions
- Django's built-in permission system
- Jazzmin admin with groups

### Protected Routes
- All `/parents/*` routes behind `@login_required` and profile checks
- API lesson complete requires authentication
- Course player provides limited data to unauthenticated users

### CORS
- `django-cors-headers` is installed and middleware is active
- No explicit `CORS_ALLOWED_ORIGINS` set in settings.py (uses defaults)

### CSRF Protection
- `CsrfViewMiddleware` is active
- `CSRF_COOKIE_SECURE = not DEBUG`
- `@csrf_exempt` on Razorpay callback (acceptable for webhook)
- Django forms include `{% csrf_token %}`

### Rate Limiting
**Not implemented.** No rate limiting on login, registration, or API endpoints.

### Input Validation
- Minimal — raw `request.POST.get()` in views
- Password length checked (>= 6)
- Username uniqueness checked via DB query
- No sanitization libraries used

### SQL Injection Risks
**LOW.** Django ORM is used throughout, which parameterizes queries. No raw SQL detected.

### XSS Risks
**MEDIUM.** Template variables are auto-escaped by Django's template engine (`{{ }}`). However:
- `{{ hero_slides_json|safe }}` in index.html bypasses escaping (JSON is from server, acceptable)
- Debug print statements in views reveal data

### File Upload Risks
- Admin panels for file uploads (course images, student profiles, study materials, certificates)
- File uploads to `media/` directory
- No file type validation beyond Django's model field type
- No virus scanning
- No size limits configured

### Exposed Secrets (CRITICAL)
The following secrets are hardcoded or committed:
1. **`.env` file is committed** — contains `DEBUG=True`, `SECURE_ADMIN_URL`, `ALLOWED_HOSTS`
2. **`settings.py` line 41**: Hardcoded fallback SECRET_KEY: `django-insecure-w4i1wehn)hnc*l@&z+(zo+kny$k0mu1udux*u$kcu*mh*7%o1j`
3. **`settings.py` line 117**: Hardcoded database password: `@inventobots123`
4. **`settings.py` line 237**: Hardcoded Razorpay test keys: `rzp_test_YOUR_KEY_HERE` / `YOUR_SECRET_HERE`

---

## 8. ENVIRONMENT VARIABLES

| Variable | Used In | Purpose | Required | Environment |
|----------|---------|---------|----------|-------------|
| `SECRET_KEY` | `settings.py:41` | Django cryptographic signing | Yes (prod) | Both |
| `DEBUG` | `settings.py:45` | Debug mode toggle | Yes | Both |
| `ALLOWED_HOSTS` | `settings.py:47` | Allowed hostnames | Yes | Both |
| `ADMIN_URL` / `SECURE_ADMIN_URL` | `config/urls.py:26` | Custom admin panel path | No (default `admin/`) | Both |
| `DB_NAME` | `.env.example` | PostgreSQL database name | If no DATABASE_URL | Both |
| `DB_USER` | `.env.example` | PostgreSQL user | If no DATABASE_URL | Both |
| `DB_PASSWORD` | `.env.example` | PostgreSQL password | If no DATABASE_URL | Both |
| `DB_HOST` | `.env.example` | PostgreSQL host | If no DATABASE_URL | Both |
| `DB_PORT` | `.env.example` | PostgreSQL port | If no DATABASE_URL | Both |
| `DATABASE_URL` | `.env.example`, `DEPLOYMENT_GUIDE.md` | Full connection string | Platform-dependent | Production |
| `CSRF_TRUSTED_ORIGINS` | `DEPLOYMENT_GUIDE.md` | CSRF trusted origins | Yes (prod with custom domain) | Production |
| `RAZORPAY_KEY_ID` | `settings.py:237` | Razorpay API key | Yes (for payments) | Both |
| `RAZORPAY_KEY_SECRET` | `settings.py:238` | Razorpay API secret | Yes (for payments) | Both |

### Notes
- `SECURE_ADMIN_URL` is read as `ADMIN_URL` in `config/urls.py` but documented as `SECURE_ADMIN_URL` — **inconsistency**
- `.env` is committed to the repo (found at `backend/.env`) — **SECURITY RISK**
- No variables for: email (SMTP), database URL parsing, Sentry/logging, or any secret management

---

## 9. CURRENT DEPLOYMENT CONFIGURATION

### Vercel
**Not currently configured.** The frontend is Django server-rendered templates, not a static SPA. Vercel is designed for static frontends or serverless functions. The project would need:
- Frontend separation (React/Vue) OR
- Vercel Python runtime for Django (experimental, limited)
- The deployment guide does NOT mention Vercel

**Verdict: NOT SUPPORTED out of the box.**

### Render
**Configured in documentation.** The `DEPLOYMENT_GUIDE.md` has a full Render section with:
- Root directory: `backend`
- Build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- Start command: `gunicorn config.wsgi:application`
- Sample `render.yaml` is provided

**Issues:** No `requirements.txt` file exists, no `Procfile`, no `runtime.txt`.

### Neon PostgreSQL
**Compatible.** Standard PostgreSQL connection. The deployment guide recommends `dj-database-url` to parse `DATABASE_URL`.

### Current Build/Start Commands
- **Build:** `pip install -r requirements.txt` (no requirements.txt exists!)
- **Start:** `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` (gunicorn not in venv)
- **Python version:** 3.12+ (no `runtime.txt`)
- **Static files:** `python manage.py collectstatic --noinput`

### CORS Configuration
- Middleware active but no `CORS_ALLOWED_ORIGINS` set in settings.py
- Documentation suggests adding `CSRF_TRUSTED_ORIGINS` manually

### Database Connection Handling
- PostgreSQL configured directly in `settings.py` with hardcoded values
- Documentation shows `dj-database-url` approach but it's in the guide, not in the code
- SQLite `.db.sqlite3` exists for local dev

### Production URLs
No production URLs configured. The `ALLOWED_HOSTS` defaults to `127.0.0.1,localhost`.

### Static Files
- `STATIC_URL = 'static/'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- WhiteNoise is **commented out** in middleware
- No `STATICFILES_STORAGE` set

### Persistent Filesystem Requirements
- **Media files** (`media/`): Course images, student profiles, study materials, certificate images, reports
- **SQLite**: Not used in production (PostgreSQL is target)
- Render free tier uses ephemeral filesystem — media uploads will **not persist** across deploys
- **Need object storage (Cloudinary, S3, etc.)** for media files

---

## 10. ₹0-COST HOSTING FEASIBILITY

### Intended Architecture
```
Frontend → Vercel Free Tier
Backend/API → Render Free Tier
Database → Neon Free Tier
Monitoring → Free uptime service
```

### Current Architecture Reality
```
Frontend ← Django renders HTML templates (no separate frontend)
Backend ← Django (same process)
Database ← PostgreSQL / SQLite
```

### Analysis

#### Features That Will Work Without Changes
- Course browsing (public pages)
- Certificate verification (read-only queries)
- API endpoints (low traffic)
- Quiz scoring and submissions
- Static page serving (basic)
- Authentication (session-based, works with PostgreSQL)

#### Features Requiring Changes
- **Frontend separation**: Django renders HTML — cannot deploy to Vercel Free Tier without extracting frontend. Would need to rewrite as a standalone SPA (React/Vue) and use DRF as pure API, OR deploy the entire Django app on Render (Vercel not suitable).
- **Media uploads**: Render free tier has ephemeral storage (files deleted on redeploy). Need Cloudinary, S3, or similar for media persistence.
- **WhiteNoise**: Must be installed and activated for static file serving without nginx.
- **requirements.txt**: Must be generated via `pip freeze > requirements.txt`.
- **Procfile** and **runtime.txt**: Need to be created for Render.

#### Features That May Exceed Free-Tier Limits
- **Render free tier**: 512 MB RAM, 1 CPU, sleeps after 15 min inactivity (cold starts), 100 GB bandwidth/month, 750 hours/month. For a small academy, this is likely sufficient initially.
- **Neon free tier**: 0.5 GB storage, 100 compute hours/month, shared compute. Storage and compute hours for a small LMS should be adequate.
- **Certificate image generation**: Uses Pillow. May use significant memory for large images. Pillow is already installed.

#### Features Requiring Persistent Storage
- User-uploaded images (course images, student profile photos)
- Study material files (PDFs, videos)
- Certificate images (auto-generated PNGs)
- Student report files

#### Features Requiring Background Processes
- Certificate auto-generation (currently runs synchronously — may timeout on free tier)
- Report generation (not yet implemented)
- **No solution** — would need Celery + Redis (not free) or a paid Render worker

#### Features That May Create Unexpected Costs
- **Razorpay**: Pay-per-transaction fees (standard Razorpay pricing)
- **Email sending**: No SMTP configured yet. If email verification or notifications are added, need SendGrid (free: 100/day) or similar
- **SMS**: Not implemented
- **Google OAuth**: Free
- **Domain**: ~$10-15/year

#### Services Requiring Credit Cards
- **Render**: Requires credit card for signup (even free tier)
- **Neon**: Requires credit card for signup (even free tier)
- **Vercel**: Requires credit card for signup (even free tier)

#### Paid APIs or Dependencies
- None currently. Razorpay takes per-transaction fees from payments processed.

### Verdict
**Partially feasible with significant changes.** The current monolithic Django architecture cannot use Vercel + Render split as intended. The full Django app must run on Render (or similar). Media storage requires an additional free-tier service (Cloudinary). Session-based auth works fine with Neon.

---

## 11. ADVANCED CIRCUIT LAB INTEGRATION

The project already has a **fully client-side circuit simulator** built from scratch:
- `js/circuit-engine.js` — BFS-based simulation engine
- `js/circuit-ui.js` — SVG rendering, drag-drop, wiring UI
- `backend/static/js/circuit-components.js` — 15+ component definitions (battery, LED, switch, sensor, etc.)
- Integrated in `student_lab.html` and `lab.html`

### Architecture Recommendation for "Advanced Circuit Lab"

**Location:** Already at `/parents/student/lab/` (student) and `/lab/` (public)

**Route structure:** Already routes exist. If wanting a dedicated page, add:
- `/lab/circuit/` → dedicated circuit lab page
- Or `/parents/student/lab/circuit/` → student-only

**Frontend integration:** Already integrated. The circuit lab is accessed via a tab in the student lab. To make it "Advanced":
1. Create a standalone template `circuit_lab.html`
2. Move the circuit tab content from `student_lab.html` (which is 1234 lines) into its own file
3. Use an iframe or a separate URL

**iframe vs direct source:**
- **Direct source integration is already working** — the circuit engine is vanilla JS embedded in the template
- **iframe** could provide isolation but would require duplicating JS includes and state management
- **Recommendation:** Use direct source with a dedicated template URL (`/lab/circuit/`)

**Client-side only:** YES — the circuit simulator is 100% client-side JavaScript. No backend calls needed during simulation.

**Saving circuit data:** Could save to current database:
- Add a `CircuitProject` model with fields: `student (FK)`, `name`, `components (JSON)`, `wires (JSON)`, `created_at`, `updated_at`
- Add API endpoints for CRUD: `POST /api/circuit/save/`, `GET /api/circuit/list/`, `GET /api/circuit/<id>/`, `PUT /api/circuit/<id>/`, `DELETE /api/circuit/<id>/`

**Authentication:** Student-only for saving. The current student auth system handles this.

**Database changes:** One new table (see above). Add migrations. No Neon-incompatible changes.

**Performance impact:** Minimal — circuit simulation runs in browser. JSON CRUD on a small table.

**Hosting impact:** None beyond the new API endpoint + DB table.

### Open-Source Alternative
Before building more on the custom engine, consider integrating **CircuitJS1** (Falstad's circuit simulator) or **QuCs** (quantum circuit simulator) via iframe. The existing custom engine is basic (BFS net tracing, no SPICE, no AC analysis, no oscilloscope). For an "Advanced" lab, Falstad's simulator would be far more capable.

---

## 12. DEPENDENCY AUDIT

### Installed Dependencies (from venv site-packages)
Packages identified in venv:

| Package | Version | Risks |
|---------|---------|-------|
| Django | 6.0.1 | Latest stable |
| djangorestframework | 3.16.1 | Latest stable |
| django-jazzmin | 3.0.1 | Active project |
| django-cors-headers | 4.9.0 | Active project |
| django-allauth | (present) | Standard |
| django-admin-interface | (present) | Standard |
| django-colorfield | (present) | Standard |
| psycopg2-binary | 2.9.11 | Standard |
| pillow | 12.1.0 | Latest |
| whitenoise | 6.11.0 | **NOT in middleware (commented out)** |
| python-dotenv | (present) | Standard |
| sqlparse | 0.5.5 | Standard |
| gevent | 25.9.1 | Async worker — may not be needed |
| greenlet | 3.3.0 | Dependency of gevent |
| requests | 2.32.5 | Standard |
| tldextract | 5.3.1 | Utility — may be unused |
| future | 1.0.0 | Python 2/3 compat — legacy, **likely unused** |
| argparse | 1.4.0 | Legacy, included in Python stdlib |
| PySocks | 1.7.1 | Proxy support — **likely unused** |
| cffi | 2.0.0 | C foreign function — **likely unused** |
| certifi | 2026.1.4 | SSL cert bundle |
| charset-normalizer | 3.4.4 | Requests dependency |
| urllib3 | 2.6.3 | Requests dependency |
| zope-interface | 8.2 | gevent dependency |
| zope-event | 6.1 | gevent dependency |

### Missing Dependencies for Production
- **gunicorn** — documented as production WSGI server, not in venv
- **dj-database-url** — documented for DATABASE_URL parsing, not in venv

### Risks
- **`future` (1.0.0)**: Python 2 compatibility. Only needed if running Python 2 code. Remove.
- **`argparse` (1.4.0)**: Bundled with Python stdlib since 3.2. The pip package is outdated.
- **`PySocks`**: Proxy support. Not used anywhere in codebase.
- **`cffi`**: Required by... unknown. Possibly cryptography or another package.
- **WhiteNoise is commented out**: Static files will 404 in production.
- **No requirements.txt**: Cannot install on deployment platform.

---

## 13. CODE QUALITY ANALYSIS

| Category | Score | Explanation |
|----------|-------|-------------|
| **Project Organization** | 7/10 | Good Django project structure with separated apps. Some concerns: study_materials has no views, signals are in apps but could be better organized. |
| **Naming Consistency** | 6/10 | Mixed naming conventions. Some routes use `student_login`, others `login`. Views mix `_view` suffix inconsistently. URLs use both `-` and `_`. Environment variable `ADMIN_URL` vs `SECURE_ADMIN_URL` mismatch. |
| **Code Duplication** | 5/10 | Student and parent login views share similar logic. Template `lab.html` (public) vs `student_lab.html` (student) overlap. Error handling is copied across views. Course admin registered twice (unregistered and re-registered). |
| **Separation of Concerns** | 5/10 | Business logic mixed with view handling (fat views.py — parents/views.py is 848 lines). No service layer. No form classes. No serializers for most data. |
| **Maintainability** | 6/10 | Clean Django structure with migrations. However, the monolithic views, lack of tests, and scattered debug prints hurt maintainability. |
| **Scalability** | 4/10 | Synchronous certificate generation will fail under load. No background task queue. Session-based auth doesn't scale horizontally without sticky sessions or Redis. SQLite used locally but PostgreSQL scales better. |
| **Error Handling** | 3/10 | Some try/except blocks but many broad `except Exception` catches. Signals silently fail on `DoesNotExist`. Debug prints used instead of logging. No structured error responses for API. |
| **Type Safety** | 3/10 | Python type hints absent. Django model fields provide some typing. View parameters are not type-annotated. |
| **Documentation** | 7/10 | Extensive project documentation (SETUP_GUIDE.md, DEPLOYMENT_GUIDE.md, ADMIN_MANUAL.md, etc.). However, inline code comments are minimal and some are misleading/outdated. |

**Overall Code Quality Score: 5.5/10**

---

## 14. BUGS AND TECHNICAL RISKS

### CRITICAL

1. **Hardcoded secrets in settings.py** — `SECRET_KEY` fallback, database password `@inventobots123`, Razorpay test keys. Anyone with the code can access production if deployed without override.
2. **`.env` file committed to repo** — exposes environment configuration.
3. **WhiteNoise commented out** — `whitenoise.middleware.WhiteNoiseMiddleware` is commented in `settings.py:78`. Static files will NOT be served in production without this.
4. **No requirements.txt** — `DEPLOYMENT_GUIDE.md` references `requirements.txt` but none exists. Deployment will fail.
5. **Database credentials in source** — `settings.py:113-121` has hardcoded PostgreSQL credentials with password `@inventobots123`.

### HIGH

6. **ADMIN_URL / SECURE_ADMIN_URL inconsistency** — `config/urls.py:26` reads `ADMIN_URL` but documentation references `SECURE_ADMIN_URL`. Will cause admin panel 404.
7. **No email SMTP configuration** — Password reset, email verification, notifications will not work.
8. **Synchronous certificate generation** — Pillow image generation runs during request. Large images or many concurrent requests will timeout on free tier.
9. **Razorpay callback is csrf_exempt** — necessary for webhooks, but no additional verification (e.g., source IP check) is implemented.
10. **No file upload validation** — No file type, size, or virus scanning. Malicious file uploads are possible.

### MEDIUM

11. **Empty test files** — `core/tests.py`, `parents/tests.py`, `certifications/tests.py`, `study_materials/tests.py` are all empty stubs. No test coverage.
12. **Debug print statements** — `print(f"DEBUG ...")` scattered throughout views. Will pollute production logs.
13. **No database migration for production** — The db.sqlite3 has development data. Fresh PostgreSQL will need migrations run (which work).
14. **No CSRF_TRUSTED_ORIGINS configured** — Will cause CSRF denial on custom domains.
15. **Debug=True in production risk** — No safeguard against deploying with DEBUG=True.
16. **Session-based auth + horizontal scaling** — Sessions are DB-stored. Needs sticky sessions or Redis cache on multi-instance deployments.

### LOW

17. **Duplicate Topic model** — `core/models.py` has both Subject/Module/Lesson hierarchy AND legacy Topic model. Code has conditional fallbacks, increasing complexity.
18. **Deprecated outdated dependencies** — `future`, `argparse`, `PySocks` are unused legacy packages.
19. **`@csrf_exempt` on certificate verify** — Could be abused for CSRF-based certificate lookup.
20. **No HTTPS redirect configuration** — `SECURE_SSL_REDIRECT` depends on DEBUG setting, not explicit.

---

## 15. GIT AND REPOSITORY STATUS

- **No Git repository found.** The `.git/` directory does not exist at `V:\Inventobots`. The codebase appears to be a local copy that was not initialized with Git.
- **No `.gitignore`** — sensitive files (`.env`, `db.sqlite3`, `*.pyc`, `venv/`) are not protected from accidental commits.
- **No commit history** available.
- **No remote repository** configured.

This is a significant finding. The project documentation mentions "GitHub repository handover" as a deliverable, but no Git state exists in this copy.

---

## 16. WHAT IS ACTUALLY COMPLETE?

| Feature | Status | Frontend | Backend | Database | Production Ready? |
|---------|--------|----------|---------|----------|-------------------|
| Public Homepage | COMPLETE | Template + Alpine slider + CSS | HomeView | Course model | YES |
| Course Catalog | COMPLETE | courses.html + Alpine filters | TemplateView | Course model | YES |
| Course Player | COMPLETE | course_player.html with lesson nav | CoursePlayerView | Subject/Module/Lesson | YES |
| Lesson Progress | COMPLETE | JS lesson complete button | MarkLessonCompleteView | LessonProgress | YES |
| Parent Registration | COMPLETE | parent_register.html | parent_register_view | User + Parent | YES |
| Parent Login | COMPLETE | login.html | parent_login_view | User + Parent | YES |
| Parent Dashboard | COMPLETE | dashboard.html | parent_dashboard_view | Multiple models | YES |
| Student Login | COMPLETE | student_login.html | student_login_view | User + Student | YES |
| Student Dashboard | COMPLETE | student_dashboard.html | student_dashboard_view | Multiple models | YES |
| Student Settings | COMPLETE | student_settings.html | student_settings_view | Student | YES |
| Course Enrollment | COMPLETE | enrollment UI | Multiple views | CourseEnrollment | YES (with payment) |
| Razorpay Payment | COMPLETE | razorpay_checkout.html | Payment views | CourseEnrollment | YES (test mode) |
| Quiz Engine | COMPLETE | Template-based | View logic | Quiz/Question/Submission | PARTIAL (no UI) |
| Badge System | PARTIAL | StudentBadge admin | Model only | Badge/StudentBadge | NO (no award logic) |
| Attendance | COMPLETE | Admin only | Admin only | Attendance | YES (admin) |
| Trainer Feedback | COMPLETE | Admin only | Admin only | TrainerFeedback | YES (admin) |
| Reports | PARTIAL | Admin + parent download | View for download | Report | PARTIAL (no auto-gen) |
| Alerts | COMPLETE | Admin + parent view | Alert CRUD | Alert | YES |
| Certifications | COMPLETE | Multiple templates | Full verification flow | Certificate/CertificationCourse | YES |
| Certificate Image Gen | COMPLETE | Admin template editor | certificate_generator.py | Certificate ImageField | YES (Pillow) |
| Google OAuth | PARTIAL | Allauth configured | Settings only | None in DB | NO (untested) |
| Code Studio | MOCKED | Fake compile output | N/A | N/A | NO (mock only) |
| Circuit Lab | COMPLETE | JS engine + UI | N/A | N/A | YES (client-side) |
| Virtual Abacus | COMPLETE | JS interactive | N/A | N/A | YES |
| Memory Games | COMPLETE | JS card games | N/A | N/A | YES |
| Study Materials | COMPLETE | Admin inline + course player | Model + Admin | StudyMaterial/File | YES |
| Admin Panel | COMPLETE | Jazzmin theme | All admin classes | All models | YES |
| Dark Mode | COMPLETE | Force-enabled | N/A | N/A | YES |
| REST API | PARTIAL | N/A | 2 endpoints | Course | NO (minimal) |
| Online Lab (Public) | COMPLETE | lab.html | TemplateView | N/A | YES |
| Mobile Responsive | COMPLETE | All templates | N/A | N/A | YES |

---

## 17. RECOMMENDED ₹0 DEPLOYMENT ARCHITECTURE

Since the project is a **monolithic Django application** (not a separate frontend + backend), the Vercel + Render split is **not feasible** without a major rewrite.

### Recommended Architecture

```
User's Browser
    │
    ▼
┌──────────────────────┐
│    Render Free Tier   │  ← Single Django app instance
│                      │
│  Django (gunicorn)   │  ← WSGI + DRF + templates
│  WhiteNoise (static) │  ← Fixed by uncommenting middleware
│  PostgreSQL connect  │  ← Points to Neon
│  Media via Cloudinary│  ← or S3 for persistent uploads
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│   Neon Free Tier      │  ← PostgreSQL database
│   inventobots_db      │
└──────────────────────┘
           │
           ▼
┌──────────────────────┐
│   Cloudinary Free     │  ← Media file storage (images, PDFs)
│   (or Render disk)    │  ← Or Render persistent disk (paid)
└──────────────────────┘
```

### What Runs Where

| Component | Location | Notes |
|-----------|----------|-------|
| Django (app + API + admin) | **Render Web Service** | gunicorn, port $PORT |
| PostgreSQL database | **Neon** | DATABASE_URL connection |
| Media files (uploads) | **Cloudinary Free** | Or S3-compatible. Render storage is ephemeral. |
| Static files (CSS/JS) | **WhiteNoise via Django** | Uncomment middleware + collectstatic |
| Circuit simulation | **Client browser** | 100% JS, no server |
| Code Studio | **Client browser** | Mock — no compilation needed |
| Domain + SSL | **Render** | Free SSL, custom domain (paid) |
| Uptime monitoring | **UptimeRobot Free** | 50 monitors, 5-min checks |
| Email | **SendGrid Free** | 100 emails/day (for future notifications) |

### Key Configuration Changes Needed
1. Uncomment WhiteNoise middleware → `settings.py:78`
2. Add `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`
3. Generate `requirements.txt`: `pip freeze > requirements.txt` (venv is at `V:\Inventobots\venv`)
4. Create `Procfile` in `backend/`: `web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
5. Create `runtime.txt`: `python-3.12.17`
6. Install `gunicorn` and `dj-database-url` in venv
7. Add `DATABASE_URL` parsing to `settings.py`
8. Configure `CORS_ALLOWED_ORIGINS` and `CSRF_TRUSTED_ORIGINS`
9. Add Cloudinary or similar for media upload persistence
10. Set `DEBUG=False`, generate new `SECRET_KEY`

---

## 18. DEPLOYMENT BLOCKERS

### MUST FIX BEFORE DEPLOYMENT

1. **Create `requirements.txt`** — `pip freeze > requirements.txt` from venv
2. **Uncomment WhiteNoise middleware** — `settings.py:78`
3. **Add `STATICFILES_STORAGE`** — `whitenoise.storage.CompressedManifestStaticFilesStorage`
4. **Fix hardcoded secrets** — Remove database password, SECRET_KEY fallback, Razorpay keys from `settings.py`. Use env vars.
5. **Generate new SECRET_KEY** — `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
6. **Add `gunicorn`** — `pip install gunicorn`
7. **Add `dj-database-url`** — `pip install dj-database-url`
8. **Add `DATABASE_URL` parsing** — Add code to `settings.py` to read `DATABASE_URL`
9. **Create `Procfile`** — `web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
10. **Create `runtime.txt`** — `python-3.12.17`
11. **Set `DEBUG=False`** — Or ensure env var is set
12. **Configure `ALLOWED_HOSTS`** — Set to production domain
13. **Add `CSRF_TRUSTED_ORIGINS`** — Set to `https://yourdomain.com`
14. **Add `CORS_ALLOWED_ORIGINS`** — In `settings.py`
15. **Remove debug print statements** — Or replace with proper logging
16. **Add `.gitignore`** — `.env`, `*.pyc`, `venv/`, `db.sqlite3`, `media/`, `staticfiles/`, `__pycache__/`
17. **Remove committed `.env` file** — Add to `.gitignore`, never commit again
18. **Run `collectstatic`** — `python manage.py collectstatic --noinput`

### SHOULD FIX

19. **Add media file storage** — Cloudinary, S3, or Render persistent disk for uploads
20. **Fix `ADMIN_URL` / `SECURE_ADMIN_URL` mismatch** — Align env var name in code and docs
21. **Add rate limiting** — Protect login/registration from brute force
22. **Add email configuration** — SMTP settings for password reset, notifications
23. **Add file upload validation** — Type checking, size limits
24. **Remove unused dependencies** — `future`, `argparse`, `PySocks`
25. **Add tests** — At minimum: login, enrollment, certificate verification
26. **Replace debug prints with logging** — Use Python's `logging` module
27. **Fix `@inventobots123` password reference** — Use env var throughout

### OPTIONAL IMPROVEMENTS

28. **Extract circuit lab** — Separate from 1234-line student_lab.html into own template
29. **Add offline fallback** — PWA support or offline-capable circuit lab
30. **Add real code compiler** — Piston API, Judge0, or similar
31. **Add Celery/Redis** — For async certificate generation
32. **Add Sentry** — Error monitoring
33. **Add Google Analytics** — Usage tracking
34. **Add SEO meta tags** — For public pages
35. **Add sitemap.xml** — SEO
36. **Add RSS/Atom feeds** — Course updates
37. **Add WebSocket support** — Real-time quiz, attendance
38. **Add backup automation** — Database backup to cloud storage

---

## 19. QUESTIONS FOR THE DEVELOPER

1. **Is there a Git repository for this project?** No `.git/` was found. Was this expected? All documentation mentions GitHub handover.

2. **What is the intended frontend hosting architecture?** The documentation mentions Railway/Render/PythonAnywhere but not Vercel. The intended stack mentions Vercel in ₹0 scenarios — is frontend separation planned?

3. **Where should media files be stored in production?** Render free tier has ephemeral storage. Is Cloudinary/S3 planned? Or should we use Render's $7/mo persistent disk?

4. **Are there Google OAuth credentials configured?** `SOCIALACCOUNT_PROVIDERS` is set up but no client ID/secret env vars are documented. Is this feature tested?

5. **What email service should be used?** No SMTP settings exist. Is email functionality (password reset, notifications) required before launch?

6. **Is the Code Studio meant to be a real code compiler or just a demo/mock?** Currently it shows fake output. If real compilation is needed, what service (Judge0, Piston, etc.)?

7. **Are the existing 5 memory games sufficient, or are more planned?**

8. **What is the expected user scale?** This affects whether we need Celery, caching, or just keep it simple.

9. **Is there a staging/QA environment planned?** Currently only development and production.

10. **What is the budget for paid services?** The ₹0-cost constraint suggests max $0/mo. If Cloudinary/SendGrid/persistent disk is needed, is there budget?

11. **Should we remove the legacy `Topic` model and migrate fully to Subject/Module/Lesson?** The dual system adds complexity.

12. **Are the fonts in `certifications/fonts/` properly licensed for commercial use?** They are bundled TTF files.

---

## 20. EXECUTIVE SUMMARY FOR ANOTHER AI

```
PROJECT: Inventobots Academy
TYPE: Commercial EdTech LMS (white-label product)
PRICE: ₹1,00,000 (~$1,200)
DEVELOPER: Nithil Suganthan
STATUS: Pre-deployment, marked "Ready for deployment" v1.0 Feb 2026

--- TECH STACK ---
- Backend: Django 6.0.1 + DRF 3.16.1 (Python 3.12)
- Frontend: Django server-rendered templates + Alpine.js 3.x + Tailwind CSS (CDN)
- Database: PostgreSQL (configured) / SQLite (local dev)
- Payments: Razorpay (Indian market)
- Auth: Django sessions + django-allauth (Google OAuth configured)
- Admin: Jazzmin theme + django-admin-interface + colorfield
- Certificates: Pillow-based image generation
- CDN: Tailwind, Alpine.js, Lucide icons, Google Fonts (no build step)

--- MAJOR FEATURES ---
1. Public website: Hero slider, course catalog with filters, lab, certifications
2. Student portal: Dashboard, courses, lab, settings, certificates
3. Parent portal: Multi-child dashboard, enrollment, attendance, feedback
4. Admin panel: Full Django admin (Jazzmin), 20+ models, 15+ admin classes
5. Online Lab: Code Studio (fake compile), Circuit Lab (real JS simulation),
   Virtual Abacus, 5 Memory/Card Games
6. Certification: Issue, revoke, public verification, image generation
7. Payments: Razorpay checkout with signature verification
8. Course hierarchy: Subject > Module > Lesson with progress tracking
9. Quiz engine: MCQs with JSON choices, scoring, submissions
10. Study material uploads per course

--- CURRENT STATE ---
- Fully functional locally with SQLite
- Razorpay integration works (test mode)
- Certificate image generation works (Pillow)
- Circuit lab is 100% client-side (no server needed)
- ~20 templates, 20 database models, 4 Django apps
- Extensive documentation (setup, deployment, admin manual)
- NO tests (empty test files)
- NO requirements.txt
- NO .gitignore, no .git repository
- NO WhiteNoise (commented out — static files won't serve)
- NO background task queue
- Hardcoded secrets in settings.py (CRITICAL)
- Debug print statements in production code

--- CRITICAL PROBLEMS ---
1. Hardcoded DB password in settings.py (`@inventobots123`)
2. Hardcoded SECRET_KEY fallback
3. WhiteNoise middleware commented out
4. No requirements.txt (deployment will fail)
5. No email SMTP configuration
6. ADMIN_URL env var name mismatch in code vs docs
7. Synchronous certificate generation (will timeout under load)
8. Session-based auth (no JWT, needs sticky sessions for scaling)
9. Uploaded files stored on ephemeral disk (lost on redeploy)
10. Generic exception handling throughout

--- DATABASE ---
- 20 models across 4 apps (core, parents, certifications, study_materials)
- PostgreSQL target, SQLite dev
- Compatible with Neon PostgreSQL
- Django ORM throughout (no raw SQL)
- 29 migration files total
- See full schema in Section 6 of the report

--- ₹0 HOSTING FEASIBILITY ---
NOT FEASIBLE with Vercel + Render split as monolithic Django.
Recommended: Deploy entire Django on Render Free Tier, Neon for DB,
Cloudinary Free for media. Requires ~15 fixes before deployment.

Major blockers:
- Cannot run on Vercel (Django templates, not static SPA)
- No requirements.txt or Procfile
- WhiteNoise needed for static files
- Cloudinary/S3 needed for persistent media uploads
- Session auth works with Neon (no modification needed)

--- ADVANCED CIRCUIT LAB ---
Already has a fully client-side circuit simulator with:
- 15+ components (battery, LED, switch, sensor, resistor, etc.)
- BFS-based net tracing simulation engine
- SVG rendering with drag-drop and wiring
- No server calls needed during simulation
- For "Advanced" version: Add CircuitProject model, CRUD API,
  consider integrating Falstad's CircuitJS1 for real SPICE simulation.
- All client-side, no hosting impact.

--- NEXT STEPS (Priority Order) ---
1. Generate requirements.txt and add gunicorn + dj-database-url
2. Fix WhiteNoise middleware (uncomment + add storage backend)
3. Remove hardcoded secrets to environment variables
4. Create .gitignore + remove committed .env
5. Create Procfile + runtime.txt
6. Add DATABASE_URL parsing in settings.py
7. Add CSRF_TRUSTED_ORIGINS + CORS_ALLOWED_ORIGINS
8. Add media file storage (Cloudinary or Render persistent disk)
9. Fix ADMIN_URL/SECURE_ADMIN_URL env var name
10. Replace debug prints with proper logging
11. Write basic tests (login, enrollment, cert verify)
12. Add file upload validation
13. Create Celery/Redis for async cert generation
14. Add email SMTP configuration
15. Add rate limiting + Sentry monitoring

--- FILE REFERENCE ---
Settings:    backend/config/settings.py
URL routing: backend/config/urls.py
WSGI:        backend/config/wsgi.py
Models:      backend/*/models.py (4 app directories)
Views:       backend/core/views.py, backend/parents/views.py
Templates:   backend/templates/ (13 templates)
JS:          js/*.js + backend/static/js/*.js
CSS:         backend/static/css/admin_theme.css
Deploy doc:  DEPLOYMENT_GUIDE.md
Setup doc:   SETUP_GUIDE.md
Admin doc:   ADMIN_MANUAL.md
```

---

*Report prepared by AI codebase auditor for Inventobots Academy — July 2026*
