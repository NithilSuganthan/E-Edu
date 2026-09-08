# Inventobots Academy - Project Documentation

---

## 1️⃣ Cover / Basic Details

| | |
|---|---|
| **Project** | Inventobots Academy Website |
| **Type** | EdTech Platform |
| **Developer** | Nithil Suganthan |
| **Date** | February 2026 |
| **Version** | v1.0 |
| **Status** | Ready for deployment |

---

## 2️⃣ Project Overview

A complete EdTech web platform designed for startups to manage courses, student enrollment, learning dashboards, and admin-controlled content updates. Suitable for training institutes, academies, and early-stage startups launching digital learning solutions.

---

## 3️⃣ Architecture Overview

### Project Structure

```
inventobots-academy/
├── backend/                    # Django project root
│   ├── config/                 # Project configuration
│   │   ├── settings.py         # Settings (DB, apps, middleware, Jazzmin)
│   │   ├── urls.py             # Root URL routing
│   │   ├── wsgi.py             # WSGI entry point (production)
│   │   └── asgi.py             # ASGI entry point
│   ├── core/                   # Main app — courses, content, quizzes, badges
│   │   ├── models.py           # Course, HeroSlide, Topic, Quiz, Badge models
│   │   ├── admin.py            # Admin registrations with fieldsets & inlines
│   │   ├── views.py            # API views & homepage view
│   │   └── urls.py             # /api/ endpoints
│   ├── parents/                # Parent & student portal
│   │   ├── models.py           # Parent, Student, Enrollment, Attendance, Feedback, Reports, Alerts
│   │   ├── admin.py            # Full admin with custom forms, actions, inlines
│   │   ├── views.py            # Login, dashboard, registration, reports
│   │   └── urls.py             # /parents/ endpoints
│   ├── certifications/         # Certificate system
│   │   ├── models.py           # CertificationCourse, Certificate
│   │   ├── admin.py            # Certificate issuance & management
│   │   ├── views.py            # Public verification view
│   │   └── urls.py             # /certifications/ endpoints
│   ├── templates/              # All Django-rendered HTML templates
│   │   ├── base.html           # Shared base layout
│   │   ├── index.html          # Homepage with hero slider
│   │   ├── courses.html        # Course catalog
│   │   ├── lab.html            # Online Lab (Code Studio, Circuit Lab, etc.)
│   │   ├── student_base.html   # Student portal layout
│   │   ├── student_dashboard.html
│   │   ├── student_courses.html
│   │   └── student_settings.html
│   ├── static/                 # CSS, JS, images
│   ├── media/                  # User uploads (course images, certificates)
│   └── manage.py               # Django management script
├── js/                         # Shared JavaScript files
└── venv/                       # Python virtual environment
```

### Application Responsibilities

| App | Role | Key Models |
|-----|------|------------|
| **config** | Project settings, root URL routing, WSGI/ASGI | — |
| **core** | Courses, homepage, content, quizzes, badges, REST API | Course, HeroSlide, Topic, Quiz, Question, Badge |
| **parents** | Parent/student portals, enrollment, tracking, reports | Parent, Student, CourseEnrollment, Attendance, ProgressTracker, TrainerFeedback, Report, Alert |
| **certifications** | Certificate issuance & public verification | CertificationCourse, Certificate |

### URL Routing Map

| URL Pattern | Handler | Description |
|-------------|---------|-------------|
| `/` | `core.HomeView` | Homepage with dynamic hero slider |
| `/courses/` | Template view | Course catalog page |
| `/about/` | Template view | About, team, legal pages |
| `/lab/` | Template view | Online Lab (Code Studio, Circuit Lab, Abacus, Games) |
| `/robotics/` | Template view | Robotics landing page |
| `/coding/` | Template view | Coding landing page |
| `/api/` | `core.urls` | REST API endpoints (courses, hero slides) |
| `/parents/` | `parents.urls` | Parent portal (login, dashboard, registration) |
| `/certifications/` | `certifications.urls` | Certificate verification |
| `/<admin-url>/` | Django Admin | Admin panel (Jazzmin-themed) |

### Data Model Relationships

```
User (Django Auth)
 ├── Parent (1:1) ──── Student (1:N)
 │                       ├── CourseEnrollment ──── Course (core)
 │                       ├── Attendance ──── CertificationCourse
 │                       ├── ProgressTracker
 │                       ├── TrainerFeedback
 │                       ├── StudentCertificate ──── Certificate
 │                       ├── StudentBadge ──── Badge
 │                       ├── TopicProgress ──── Topic ──── Course
 │                       ├── QuizSubmission ──── Quiz ──── Course
 │                       ├── Report
 │                       └── Alert
 │
 └── Student (1:1, optional — for student login)

Course (core)
 ├── HeroSlide (proxy — hero-featured courses)
 ├── Topic (1:N, ordered)
 ├── Quiz (1:N) ──── Question (1:N, inline)
 └── CertificationCourse (linked via FK)
```

### Request Flow

```
Browser Request
    │
    ▼
Django URL Router (config/urls.py)
    │
    ├── Static pages → TemplateView → HTML template (Alpine.js + Tailwind)
    ├── /api/* → DRF ViewSets → JSON response
    ├── /parents/* → Parents views → Django templates (auth-protected)
    ├── /certifications/* → Certifications views → Django templates
    └── /admin/* → Django Admin (Jazzmin) → Admin templates
```

### Frontend Architecture

| Technology | Purpose |
|-----------|---------|
| **HTML + Django Templates** | Server-side rendering with template inheritance (`base.html`) |
| **Tailwind CSS** | Utility-first styling, responsive design, dark/light mode |
| **Alpine.js** | Client-side interactivity (modals, tabs, sliders, toggles) |
| **Lucide Icons** | Modern icon set used across all pages |
| **Google Fonts** | Inter (body) and Outfit (headings) |

The frontend uses a **server-rendered SPA-like pattern** — Django serves full HTML pages, while Alpine.js handles interactive elements (filtering, modals, dark mode toggle, hero slider) without requiring a JavaScript build step.

---

## 4️⃣ Features & Modules

### Public Website
- **Homepage** — Hero slider, course categories, dark/light mode
- **Courses** — Filterable catalog with details modal, enroll/inquiry buttons
- **About** — Team, mission, legal pages
- **Online Lab** — Code Studio, Circuit Lab, Abacus, Memory Games

### Student Portal
- **Login/Register** — Email auth with password management
- **Dashboard** — Progress, schedule, XP/Level, pending payments
- **My Courses** — Enrolled courses with progress bars
- **Settings** — Profile, password, theme preferences

### Parent Portal
- **Dashboard** — Children overview, stats, alerts, reports
- **Student Management** — Registration, attendance, feedback view
- **Reports** — Downloadable progress reports

### Certifications
- **Public Verification** — Certificate lookup by ID
- **Admin Management** — Issue, revoke, track certificates

### Admin Panel (Django)
- **Courses** — CRUD, categories, hero slider control
- **Content** — Topics, quizzes, resources
- **Users** — Parents, students, enrollments
- **Tracking** — Attendance, progress, feedback, badges

---

## 5️⃣ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | HTML, CSS (Tailwind CSS), JavaScript (Alpine.js) |
| **Backend** | Django (Python) |
| **Database** | SQLite (dev) / PostgreSQL (production-ready) |
| **API** | Django REST Framework |
| **Icons** | Lucide Icons |
| **Fonts** | Google Fonts (Inter, Outfit) |
| **Hosting-Ready** | Railway / Render / PythonAnywhere |
| **Version Control** | GitHub repository included |

---

## 6️⃣ Ownership & Rights

Upon full payment, the client (**Inventobots Academy**) receives:

| Right | Details |
|-------|---------|
| ✅ Full Source Code | Complete codebase delivered via GitHub/ZIP |
| ✅ Deployment-Ready Build | Production-ready with setup instructions |
| ✅ Modification Rights | Freedom to edit, extend, and customize |
| ✅ Commercial Use | Right to operate and monetize the platform |
| ✅ No Royalties | No recurring fees or revenue sharing |
| ✅ Database & Media | Full ownership of all data and assets |

### Retained by Developer (Nithil Suganthan)

| Right | Details |
|-------|---------|
| 📌 Portfolio Usage | Right to showcase in personal portfolio |
| 📌 Non-Compete | Will not resell to direct competitors |

### Not Included (Charged Separately)

| Item | Notes |
|------|-------|
| 🔧 Post-delivery bug fixes | Free for 30 days, paid after |
| 🆕 New feature development | Quoted separately |
| 🌐 Domain & hosting costs | Client's responsibility |
| 📧 Third-party API costs | Borne by client |

---

## 7️⃣ Value Proposition (Why Buy This Product)

### Development Effort Saved

| Component | Estimated Build Time (Solo Dev) |
|-----------|-------------------------------|
| Public Website (Home, Courses, About, Lab) | ~3 weeks |
| Student Portal (Auth, Dashboard, Courses, Settings) | ~2 weeks |
| Parent Portal (Dashboard, Registration, Reports) | ~2 weeks |
| Admin Panel (Courses, Users, Tracking, Certificates) | ~1.5 weeks |
| Certifications System | ~1 week |
| Online Lab (Code Studio, Circuit Lab, Abacus, Memory Games) | ~2 weeks |
| UI/UX Polish (Dark/Light Mode, Responsive, Animations) | ~1 week |
| Testing, Debugging & Integration | ~1 week |
| **Total** | **~13.5 weeks (~3.5 months)** |

### Cost Comparison

| Approach | Estimated Cost |
|----------|---------------|
| Hiring a freelance full-stack developer (3.5 months) | ₹70,000 – ₹1,50,000 |
| Hiring frontend + backend separately | ₹1,00,000 – ₹2,00,000+ |
| Agency/studio development | ₹2,00,000 – ₹5,00,000+ |
| **This ready-made platform** | **Fraction of above costs** |

### What You're Getting

- ✅ **Saves ~3.5 months of development time** — fully built, not a prototype
- ✅ **Saves hiring costs** — no need for separate frontend, backend, or UI/UX developers
- ✅ **Ready-to-launch product** — deploy to Railway, Render, or PythonAnywhere in under an hour
- ✅ **14+ major features** — all tested and functional (see Section 3)
- ✅ **Fully customizable** — clean code, well-structured, easy to rebrand for any academy
- ✅ **Modern tech stack** — Django + Alpine.js + Tailwind CSS, scalable for growth
- ✅ **Admin-controlled content** — no developer needed for day-to-day updates
- ✅ **Mobile responsive** — works across all devices out of the box
- ✅ **30-day free bug support** — peace of mind after delivery

> **Bottom Line:** Buying this website saves approximately **3–4 months of development** and **₹1,00,000+** in engineering costs. You receive a production-ready, professional EdTech platform — not a template, but a fully functional product tailored for an academy business.

---

## 8️⃣ Pricing & Payment Terms

### Website Cost: ₹1,00,000 (One Lakh Only)

> **Note:** This pricing does **not** include domain name registration or web hosting. These are the client's responsibility and are billed separately by third-party providers.

### What's Included in ₹1,00,000

| # | Deliverable |
|---|-------------|
| 1 | Complete source code (GitHub repository + ZIP) |
| 2 | Django admin panel — fully configured |
| 3 | Student Portal, Parent Portal & Certifications system |
| 4 | Online Lab (Code Studio, Circuit Lab, Abacus, Memory Games) |
| 5 | Dark/light mode, responsive design, animations |
| 6 | Deployment support (up to 7 days) |
| 7 | Setup documentation & environment guide |
| 8 | 30 days of free bug fixes post-delivery |

### What's NOT Included

| Item | Estimated Cost | Notes |
|------|---------------|-------|
| Domain name | ₹500 – ₹1,500/year | Client purchases directly |
| Web hosting | ₹500 – ₹3,000/month | Railway / Render / PythonAnywhere |
| Third-party API costs | Varies | If any integrations are added |

### Payment Schedule

| Milestone | Amount | When |
|-----------|--------|------|
| **Advance** | ₹50,000 (50%) | Before project handover |
| **Final Payment** | ₹50,000 (50%) | Upon delivery & successful deployment |

> Full source code and admin access are handed over only after final payment is received.

### Optional Add-Ons (Quoted Separately)

| Add-On | Estimated Cost |
|--------|---------------|
| Custom feature development | ₹5,000 – ₹15,000 per feature |
| Monthly maintenance & updates | ₹3,000 – ₹5,000/month |
| Domain + hosting setup assistance | ₹1,000 – ₹2,000 |
| Payment gateway integration (Razorpay/Stripe) | ₹5,000 – ₹8,000 |
| SMS/Email notification system | ₹3,000 – ₹5,000 |
| Mobile app (React Native) | Quoted separately |

### Terms

- All prices are exclusive of domain registration, hosting, and third-party API costs.
- Scope changes or new feature requests after delivery will be quoted separately.
- This quotation is valid for **30 days** from the date of this document.
- Payment can be made via UPI, bank transfer, or any mutually agreed method.

---

## 9️⃣ Demo & Handover

### Live Demo

A **fully functional live demo** is available for review before purchase. The demo includes:

| Area | What You'll See |
|------|----------------|
| Public Website | Homepage, courses, about, online lab — fully interactive |
| Student Portal | Login, dashboard, enrolled courses, settings |
| Parent Portal | Dashboard, student management, reports |
| Admin Panel | Course management, user control, certificate issuance |
| Certifications | Public certificate verification by ID |

> A demo walkthrough can be scheduled at a mutually convenient time. Screen-sharing or a staging link will be provided.

### GitHub Repository Handover

| Step | Details |
|------|---------|
| 1 | Private GitHub repository transferred to client's account |
| 2 | Full commit history preserved for transparency |
| 3 | `.env.example` and setup instructions included |
| 4 | ZIP archive of the complete codebase also provided |

### Documentation Provided

| Document | Contents |
|----------|----------|
| **Setup Guide** | Environment setup, dependency installation, database migration |
| **Deployment Guide** | Step-by-step instructions for Railway / Render / PythonAnywhere |
| **Admin Manual** | How to manage courses, users, certificates, and content |
| **Project Documentation** | Architecture overview, tech stack, feature breakdown (this document) |
| **Environment Config** | `.env.example` with all required variables documented |

### Support Period

| Support Type | Duration | Coverage |
|-------------|----------|----------|
| **Bug Fixes** | 30 days post-delivery | Any bugs in delivered features — free of charge |
| **Deployment Assistance** | Up to 7 days | Help with initial deployment and server setup |
| **Queries & Guidance** | 30 days post-delivery | Questions about codebase, admin panel, or configuration |
| **Extended Support** | Optional (paid) | ₹3,000 – ₹5,000/month for ongoing maintenance |

> After the 30-day support window, all maintenance and feature requests will be quoted separately.

---

## 🔟 Closing Statement

This project is **ready for immediate deployment** and can be adapted to your organization's needs with minimal changes. The codebase is clean, well-structured, and built with scalability in mind — making it easy to extend as your academy grows.

I am open to discussions regarding customization, pricing, and long-term collaboration. Feel free to reach out for a live demo or any questions.

---

*Document prepared by Nithil Suganthan — February 2026*
