# Inventobots - EdTech Platform

## 1. Project Overview

A complete **EdTech web platform** designed for startups to manage courses, student enrollment, learning dashboards, and admin-controlled content updates. Suitable for training institutes, academies, and early-stage startups launching digital learning solutions.

---

## 2. Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 4.x (Python) |
| **Frontend** | Django Templates + Alpine.js |
| **Styling** | Tailwind CSS |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Icons** | Lucide Icons |
| **API** | Django REST Framework |

---

## 3. Project Structure

```
Inventobots/
├── backend/
│   ├── config/          # Django settings & URL routes
│   ├── core/            # Course, Quiz, Topic, Badge models
│   ├── parents/         # Parent/Student auth & dashboards
│   ├── certifications/  # Certificate issuance & verification
│   ├── templates/       # HTML templates (frontend)
│   ├── static/          # CSS, JS, images
│   └── media/           # User-uploaded files
└── venv/                # Python virtual environment
```

---

## 4. Core Features

### 4.1 Public Website
- **Home Page** (`index.html`) - Dynamic hero slider, course showcase
- **Courses** (`courses.html`) - Category-filtered course catalog
- **About** (`about.html`) - Company info, team, legal pages
- **Coding/Robotics** - Specialized course landing pages
- **Online Lab** (`lab.html`) - Interactive learning tools

### 4.2 Student Portal
- **Dashboard** - Progress overview, enrolled courses, XP/Level
- **My Courses** - Active enrollments with progress bars
- **Online Lab** - Code Studio, Circuit Lab, Virtual Abacus, Memory Games
- **Settings** - Profile management, password change

### 4.3 Parent Portal
- **Dashboard** - Track all children's progress
- **Student Registration** - Enroll children in courses
- **Attendance & Feedback** - View trainer feedback, attendance records
- **Reports & Alerts** - Download reports, notifications

### 4.4 Admin Panel
- **Course Management** - CRUD courses, topics, quizzes
- **Hero Slider** - Manage homepage carousel
- **Student Management** - Enrollments, progress tracking
- **Certificate Issuance** - Generate & manage certificates

### 4.5 Certifications
- **Public Verification** - Certificate lookup by ID
- **Certificate Management** - Issue, revoke, track certificates

---

## 5. Database Models

### Core App
| Model | Purpose |
|-------|---------|
| `Course` | Main course with categories, pricing, hero slider fields |
| `Topic` | Course modules with video links & resources |
| `Quiz` / `Question` | Assessments with multiple-choice questions |
| `TopicProgress` | Track student completion per topic |
| `Badge` / `StudentBadge` | Gamification rewards |

### Parents App
| Model | Purpose |
|-------|---------|
| `Parent` | Parent account linked to Django User |
| `Student` | Child profile with level, XP, enrollment date |
| `CourseEnrollment` | Enrollment with status (Pending/Active/Completed) |
| `Attendance` | Daily attendance tracking |
| `ProgressTracker` | Proficiency level tracking |
| `TrainerFeedback` | Instructor feedback per student |

### Certifications App
| Model | Purpose |
|-------|---------|
| `CertificationCourse` | Courses eligible for certification |
| `Certificate` | Issued certificates with unique IDs |

---

## 6. Key URLs

| Route | View | Description |
|-------|------|-------------|
| `/` | `HomeView` | Homepage with hero slider |
| `/courses/` | Template | Course catalog |
| `/lab/` | Template | Online Lab tools |
| `/parents/login/` | `parent_login_view` | Parent login |
| `/parents/dashboard/` | `parent_dashboard_view` | Parent dashboard |
| `/parents/students/login/` | `student_login_view` | Student login |
| `/parents/students/dashboard/` | `student_dashboard_view` | Student dashboard |
| `/certifications/` | Certifications app | Certificate verification |
| `/admin/` | Django Admin | Admin panel |

---

## 7. Course Categories

- Robotics
- Coding
- Abacus
- Academic
- Inventowrite
- Inventoshastra
- Inventothunai
- Inventophonics
- Inventobeads
- Inventohindi

---

## 8. Running the Project

```bash
# 1. Navigate to backend
cd Inventobots/backend

# 2. Activate virtual environment
..\venv\Scripts\activate  # Windows

# 3. Run migrations
python manage.py migrate

# 4. Create superuser (first time)
python manage.py createsuperuser

# 5. Start development server
python manage.py runserver
```

Access at: `http://127.0.0.1:8000/`

---

## 9. Environment Variables

Create `.env` file in `backend/`:
```
SECRET_KEY=your-secret-key
DEBUG=True
```

---

## 10. Key Features Summary

| Feature | Status |
|---------|--------|
| Dynamic Hero Slider | ✅ |
| Course Catalog with Filters | ✅ |
| Parent Registration & Login | ✅ |
| Student Registration & Login | ✅ |
| Student Dashboard | ✅ |
| Parent Dashboard | ✅ |
| Course Enrollment | ✅ |
| Progress Tracking | ✅ |
| Certificate Verification | ✅ |
| Online Lab (Code/Circuit/Abacus/Games) | ✅ |
| Dark/Light Mode | ✅ |
| Mobile Responsive | ✅ |
| WhatsApp Integration | ✅ |
| Admin Panel | ✅ |
