# Inventobots Academy — Quotation & Cost Breakdown

**Prepared for:** Inventobots Academy
**Prepared by:** Nithil Suganthan
**Date:** February 2026
**Quotation Valid Until:** March 2026

---

## Total Project Cost: ₹1,00,000 (One Lakh Only)

---

## 1. Page-Wise Breakdown

### Public Website (8 Pages)

| # | Page | Complexity | Cost |
|---|------|-----------|------|
| 1 | Homepage (`index.html`) — Hero slider, categories, dark/light mode, animations | High | ₹8,000 |
| 2 | Courses (`courses.html`) — Filterable catalog, detail modals, enroll/inquiry | High | ₹6,000 |
| 3 | About (`about.html`) — Team, mission, legals, terms, privacy | Medium | ₹3,000 |
| 4 | Online Lab (`lab.html`) — Code Studio, Circuit Lab, Abacus, Memory Games | Very High | ₹10,000 |
| 5 | Robotics Landing (`robotics.html`) | Low | ₹2,000 |
| 6 | Coding Landing (`coding.html`) | Low | ₹2,000 |
| 7 | Certifications (`certifications/index.html`) — Verification form | Medium | ₹3,000 |
| 8 | Certificate Result (`certifications/result.html`) — Valid/invalid display | Medium | ₹2,000 |
| | **Subtotal — Public Website** | **8 pages** | **₹36,000** |

### Student Portal (5 Pages)

| # | Page | Complexity | Cost |
|---|------|-----------|------|
| 1 | Student Dashboard (`student_dashboard.html`) — Progress, XP, schedule, payments | High | ₹5,000 |
| 2 | My Courses (`student_courses.html`) — Enrolled courses, progress bars | Medium | ₹3,000 |
| 3 | Student Lab (`student_lab.html`) — Full lab access for enrolled students | Very High | ₹6,000 |
| 4 | Settings (`student_settings.html`) — Profile, password, theme preferences | Medium | ₹3,000 |
| 5 | Base Layout (`student_base.html`) — Portal navigation, sidebar, responsiveness | Medium | ₹2,000 |
| | **Subtotal — Student Portal** | **5 pages** | **₹19,000** |

### Parent Portal (4 Pages)

| # | Page | Complexity | Cost |
|---|------|-----------|------|
| 1 | Parent Dashboard (`parents/dashboard.html`) — Children overview, stats, alerts | High | ₹5,000 |
| 2 | Parent Login (`parents/login.html`) — Email auth, CSRF-protected | Medium | ₹2,000 |
| 3 | Student Login (`parents/student_login.html`) — Separate student auth | Medium | ₹2,000 |
| 4 | Student Register (`parents/student_register.html`) — Registration form | Medium | ₹2,000 |
| | **Subtotal — Parent Portal** | **4 pages** | **₹11,000** |

### Shared / Admin Templates (3 Pages)

| # | Page | Complexity | Cost |
|---|------|-----------|------|
| 1 | Base Layout (`base.html`) — Shared header, footer, nav, dark/light toggle | High | ₹3,000 |
| 2 | Admin Login Override (`admin/login.html`) | Low | ₹500 |
| 3 | Admin Logout Override (`admin/logout.html`) | Low | ₹500 |
| | **Subtotal — Shared/Admin** | **3 pages** | **₹4,000** |

### Page Summary

| Section | Pages | Cost |
|---------|-------|------|
| Public Website | 8 | ₹36,000 |
| Student Portal | 5 | ₹19,000 |
| Parent Portal | 4 | ₹11,000 |
| Shared / Admin | 3 | ₹4,000 |
| **Total Frontend Pages** | **20 pages** | **₹70,000** |

---

## 2. Frontend / Backend Breakdown

### Frontend Development — ₹70,000

| Component | Details | Cost |
|-----------|---------|------|
| **20 Responsive Pages** | HTML/CSS/JS — fully designed and functional | ₹52,000 |
| **Dark / Light Mode** | System-wide toggle with persistent preference | ₹3,000 |
| **Responsive Design** | Mobile, tablet, desktop — all breakpoints tested | ₹5,000 |
| **Animations & Micro-interactions** | Hover effects, transitions, smooth scrolling | ₹3,000 |
| **Hero Slider** | Dynamic, admin-configurable, animated slider | ₹3,000 |
| **Online Lab UI** | Code Studio, Circuit Lab, Abacus, 5 Memory Games | ₹4,000 |
| | **Subtotal** | **₹70,000** |

### Backend Development — ₹30,000

| Component | Details | Cost |
|-----------|---------|------|
| **Django Project Setup** | Config, settings, URL routing, WSGI/ASGI | ₹2,000 |
| **Core App** | 9 models (Course, HeroSlide, Topic, Quiz, Question, QuizSubmission, Badge, StudentBadge, TopicProgress) | ₹5,000 |
| **Parents App** | 9 models (Parent, Student, Enrollment, Attendance, Progress, Feedback, Certificate, Report, Alert) | ₹6,000 |
| **Certifications App** | 2 models (CertificationCourse, Certificate) + public verification | ₹3,000 |
| **REST API** | Django REST Framework — course/hero endpoints | ₹3,000 |
| **Authentication System** | Parent login, student login, registration, session management | ₹3,000 |
| **Admin Panel Customization** | Jazzmin theme, custom fieldsets, inline editing, bulk actions, 15+ admin classes | ₹4,000 |
| **Signals & Automation** | Auto-profile creation, enrollment triggers | ₹2,000 |
| **Database Design** | PostgreSQL schema, migrations, relationships | ₹2,000 |
| | **Subtotal** | **₹30,000** |

### Frontend / Backend Summary

| Layer | Cost | % |
|-------|------|---|
| Frontend (UI/UX, pages, interactivity) | ₹70,000 | 70% |
| Backend (Django, API, database, admin) | ₹30,000 | 30% |
| **Total** | **₹1,00,000** | **100%** |

---

## 3. Time & Hourly Rate Breakdown

### Hourly Rate: ₹250/hour

| Phase | Tasks | Hours | Cost |
|-------|-------|-------|------|
| **Planning & Design** | Requirements, wireframes, architecture design | 20 hrs | ₹5,000 |
| **Frontend — Public Site** | 8 pages with responsive design, dark mode, animations | 80 hrs | ₹20,000 |
| **Frontend — Student Portal** | Dashboard, courses, lab, settings | 50 hrs | ₹12,500 |
| **Frontend — Parent Portal** | Login, dashboard, registration forms | 30 hrs | ₹7,500 |
| **Frontend — Online Lab** | Code Studio, Circuit Lab, Abacus, 5 Memory Games | 40 hrs | ₹10,000 |
| **Backend — Models & Database** | 20 models, migrations, relationships | 30 hrs | ₹7,500 |
| **Backend — Views & API** | REST endpoints, template views, auth views | 25 hrs | ₹6,250 |
| **Backend — Admin Panel** | Jazzmin, 15+ admin classes, fieldsets, actions | 20 hrs | ₹5,000 |
| **Backend — Auth & Signals** | Login, registration, sessions, auto-profiles | 15 hrs | ₹3,750 |
| **Integration & Testing** | Frontend-backend integration, API testing, cross-browser | 30 hrs | ₹7,500 |
| **UI Polish & Responsiveness** | Mobile optimization, animations, dark/light mode | 25 hrs | ₹6,250 |
| **Documentation** | Setup guide, deployment guide, admin manual, env config | 15 hrs | ₹3,750 |
| **Deployment Support** | Initial deployment assistance (up to 7 days) | 20 hrs | ₹5,000 |
| **Total** | | **400 hrs** | **₹1,00,000** |

### Time Summary

| Metric | Value |
|--------|-------|
| **Total Development Hours** | 400 hours |
| **Hourly Rate** | ₹250/hr |
| **Effective Weekly Hours** | ~30 hrs/week |
| **Total Duration** | ~13.5 weeks (~3.5 months) |
| **Total Cost** | **₹1,00,000** |

---

## 4. LMS Package Breakdown

This project is a **complete Learning Management System (LMS)** package. Here's what's included:

### LMS Core Features — Included

| Module | Features | Market Value |
|--------|----------|-------------|
| **Course Management** | CRUD, categories, thumbnails, duration, mode, syllabus | ₹15,000 |
| **Content Management** | Topics with ordering, video URLs, downloadable resources | ₹10,000 |
| **Quiz & Assessment Engine** | Quizzes, MCQs (JSON), scoring, time limits, submissions | ₹12,000 |
| **Student Dashboard** | Progress tracking, XP/Levels, schedule, payment status | ₹10,000 |
| **Parent Portal** | Multi-child management, attendance, feedback, reports | ₹12,000 |
| **Enrollment System** | Course enrollment, payment tracking, status management | ₹8,000 |
| **Attendance Tracking** | Per-student, per-course, daily records with notes | ₹5,000 |
| **Progress Tracking** | Skill-based, proficiency levels, scored assessments | ₹5,000 |
| **Trainer Feedback** | Category-based, star ratings, per-student | ₹4,000 |
| **Badge & Achievement System** | Custom badges, criteria-based, auto-award ready | ₹5,000 |
| **Certification System** | Issue, revoke, public verification by ID | ₹8,000 |
| **Report Generation** | Period-based reports, file uploads, parent access | ₹5,000 |
| **Alert System** | Student alerts with severity, bulk mark read/unread | ₹3,000 |
| **Online Lab** | Code Studio, Circuit Lab, Abacus, 5 Memory Games | ₹15,000 |
| **Admin Panel** | Jazzmin theme, 15+ admin classes, bulk actions | ₹8,000 |
| **Website (Public)** | Homepage, courses, about, responsive, dark/light mode | ₹15,000 |
| **Authentication** | Multi-role login (parent, student, admin), registration | ₹5,000 |
| **Documentation** | Setup, deployment, admin manual, environment config | ₹5,000 |
| **Total Market Value** | | **₹1,50,000+** |

### What You Pay

| | |
|---|---|
| **Market Value** | ₹1,50,000+ |
| **Your Price** | **₹1,00,000** |
| **You Save** | **₹50,000+ (33% discount)** |

### LMS Package Comparison

| Feature | Inventobots LMS | Generic Templates | Custom Build |
|---------|----------------|-------------------|-------------|
| Ready to deploy | ✅ Immediate | ❌ Needs customization | ❌ 3–6 months |
| Admin panel | ✅ Full Django admin | ❌ Basic or none | ✅ Custom built |
| Student portal | ✅ Complete | ❌ Not included | ✅ Custom built |
| Parent portal | ✅ Complete | ❌ Not included | ✅ Custom built |
| Certification system | ✅ With public verification | ❌ Not included | ✅ Custom built |
| Online lab / tools | ✅ 8+ interactive tools | ❌ Not included | ✅ Custom built |
| Quiz engine | ✅ Built-in | ❌ Basic or plugin | ✅ Custom built |
| Dark/light mode | ✅ System-wide | ❌ Rare | ⚠️ Extra cost |
| Mobile responsive | ✅ All pages | ⚠️ Varies | ✅ Custom built |
| Source code | ✅ Full ownership | ⚠️ License restrictions | ✅ Full ownership |
| **Price** | **₹1,00,000** | **₹10,000–₹30,000** | **₹2,00,000–₹5,00,000** |

---

## 5. Payment Schedule

| Milestone | Amount | When |
|-----------|--------|------|
| **Advance Payment** | ₹50,000 (50%) | Before project handover |
| **Final Payment** | ₹50,000 (50%) | Upon delivery & successful deployment |

> Full source code and admin access are handed over only after final payment is received.

---

## 6. What's Included at ₹1,00,000

| # | Deliverable |
|---|-------------|
| 1 | Complete source code (GitHub + ZIP) |
| 2 | 20 fully designed, responsive pages |
| 3 | 20 database models across 3 Django apps |
| 4 | Django admin panel — Jazzmin themed, fully configured |
| 5 | Student Portal, Parent Portal & Certifications |
| 6 | Online Lab (Code Studio, Circuit Lab, Abacus, 5 Memory Games) |
| 7 | REST API (Django REST Framework) |
| 8 | Dark/light mode, responsive design, animations |
| 9 | Deployment support (up to 7 days) |
| 10 | Full documentation (Setup, Deployment, Admin, Env Config) |
| 11 | 30 days free bug fixes |

---

## 7. What's NOT Included

| Item | Estimated Cost | Notes |
|------|---------------|-------|
| Domain name | ₹500 – ₹1,500/year | Client purchases directly |
| Web hosting | ₹500 – ₹3,000/month | Railway / Render / PythonAnywhere |
| Third-party API costs | Varies | If integrations are added later |
| New feature development | ₹5,000 – ₹15,000/feature | Quoted separately |
| Monthly maintenance | ₹3,000 – ₹5,000/month | Optional add-on |

---

*Quotation prepared by Nithil Suganthan — February 2026*
