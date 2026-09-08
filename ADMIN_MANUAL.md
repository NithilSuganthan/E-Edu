# Inventobots Academy — Admin Manual

---

## 1. Accessing the Admin Panel

| Detail | Value |
|--------|-------|
| **URL** | `https://yourdomain.com/super_secure_admin/` |
| **Default local** | `http://127.0.0.1:8000/super_secure_admin/` |
| **Login** | Use the superuser account created during setup |

> [!TIP]
> The admin URL is set via the `SECURE_ADMIN_URL` environment variable in `.env`. Change it to any custom path for security (e.g., `my_secret_panel/`).

The admin panel uses **Jazzmin** — a modern, responsive admin theme with sidebar navigation, search, and quick links.

---

## 2. Admin Panel Overview

The sidebar organizes all models into the following groups:

| Section | Models |
|---------|--------|
| **Core** | Courses, Hero Slider Items, Topics, Quizzes, Badges, Student Badges, Topic Progress, Quiz Submissions |
| **Parents** | Parents, Students, Course Enrollments, Attendance, Progress Trackers, Trainer Feedback, Student Certificates, Reports, Alerts |
| **Certifications** | Certification Courses, Certificates |
| **Auth** | Users, Groups |

---

## 3. Managing Courses

### Adding a New Course

1. Go to **Core → Courses → Add Course**
2. Fill in the required fields:

| Field | Description | Required |
|-------|-------------|----------|
| **Title** | Course name (e.g., "Python for Kids") | ✅ |
| **Category** | Dropdown: Robotics, Coding, Abacus, Academic, etc. | ✅ |
| **Description** | Full course description | ✅ |
| **Image** | Upload a course thumbnail | Optional |
| **Price** | Course fee (decimal) | Optional |
| **Duration** | e.g., "12 Weeks" | Optional |
| **Mode** | Online / Offline / Hybrid | ✅ |
| **Start Date** | When the course begins | Optional |
| **Syllabus** | Detailed topics covered | Optional |
| **Certification Details** | Info about the certificate issued | Optional |
| **Notes** | Any additional notes | Optional |

3. Click **Save**

### Editing & Deleting Courses

- Click any course title in the list to edit
- Use the **Delete** button at the bottom of the edit page to remove a course
- Bulk actions: Select multiple courses → choose action from dropdown

### List View Features

| Feature | How |
|---------|-----|
| **Filter by category** | Use the right sidebar filter |
| **Filter by hero status** | Filter by "Is hero featured" |
| **Search** | Search by title, description, subtitle, or tagline |
| **Inline editing** | Toggle `is_hero_featured` and `display_order` directly in the list |

---

## 4. Managing the Hero Slider

The homepage hero slider is controlled directly from the admin panel.

### Adding a Hero Slide

1. Go to **Core → Hero Slider Items → Add**
2. Fill in the slide content:

| Field | Description |
|-------|-------------|
| **Title** | Main headline on the slide |
| **Badge** | Small label (e.g., "New", "Popular") |
| **Subtitle** | Supporting text below the title |
| **Image / Image URL** | Background image (upload or external URL) |
| **Description** | Additional text content |
| **Color Gradient** | Tailwind CSS gradient classes (e.g., `from-blue-500 to-cyan-400`) |
| **Display Order** | Number to control slide order (lower = first) |
| **Tagline** | Short tagline text |
| **Highlights** | JSON list of feature highlights |
| **CTA Buttons** | Primary and secondary button text + URLs |

3. Click **Save** — the slide is automatically marked as hero-featured

### Reordering Slides

- Edit the **Display Order** number directly in the list view (inline editing is enabled)
- Lower numbers appear first

### Removing a Slide from the Slider

- Edit the parent **Course** and uncheck `is_hero_featured`, or delete the Hero Slider Item entry

---

## 5. Managing Topics & Content

### Adding Topics to a Course

1. Go to **Core → Topics → Add Topic**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Course** | Select the parent course |
| **Title** | Topic name (e.g., "Variables & Data Types") |
| **Description** | Topic summary |
| **Order** | Display order within the course (0, 1, 2...) |
| **Video URL** | Link to a video lecture |
| **Resources** | Links to materials (comma-separated or JSON) |

3. Click **Save**

### Viewing Topic Progress

Go to **Core → Topic Progress** to see which students have completed which topics.

| Column | Description |
|--------|-------------|
| Student | Student name |
| Topic | Topic title |
| Is Completed | ✅ / ❌ |
| Last Accessed | Timestamp |

Filter by completion status using the sidebar filter.

---

## 6. Managing Quizzes

### Creating a Quiz

1. Go to **Core → Quizzes → Add Quiz**
2. Fill in quiz details:

| Field | Description |
|-------|-------------|
| **Course** | Linked course |
| **Topic** | Linked topic (optional) |
| **Title** | Quiz name |
| **Description** | Instructions or summary |
| **Time Limit** | Minutes allowed (default: 15) |
| **Passing Score** | Minimum passing percentage (default: 50) |

3. **Add Questions** inline on the same page:

| Field | Description |
|-------|-------------|
| **Text** | Question text |
| **Choices** | JSON format: `{"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"}` |
| **Correct Answer** | Single letter key (e.g., `A`) |
| **Explanation** | Explanation shown after answering |

4. Click **Save**

### Viewing Quiz Submissions

Go to **Core → Quiz Submissions** to review student scores.

| Column | Description |
|--------|-------------|
| Student | Who submitted |
| Quiz | Which quiz |
| Score | Percentage achieved |
| Submitted At | When |

Filter by quiz name or date range.

---

## 7. Managing Users

### User Accounts

Go to **Auth → Users** to manage all accounts. The admin shows an extended user list with:

| Column | Description |
|--------|-------------|
| Username | Login username |
| Email | Email address |
| First / Last Name | Full name |
| Is Staff | Admin access |
| Is Parent | Has a parent profile linked |

### Creating a Parent Account

1. Go to **Auth → Users → Add User**
2. Set username and password
3. After saving, scroll down to the **Parent Profile** section
4. Fill in phone number, address, emergency contact
5. Save

Or go to **Parents → Parents → Add Parent** and link to an existing user.

### Parent Management

Go to **Parents → Parents** to see all parent accounts:

| Column | Description |
|--------|-------------|
| Parent Name | Full name from the linked user |
| Email | User email |
| Phone Number | Contact number |
| Students | Number of children registered |
| Created At | Registration date |

---

## 8. Managing Students

### Adding a Student

1. Go to **Parents → Students → Add Student**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Parent** | Select the parent account |
| **User** | Link to a user account (optional — for student login) |
| **Full Name** | Student's full name |
| **Date of Birth** | Date picker |
| **Grade Level** | Current grade/class |
| **Enrollment Date** | When they joined |
| **XP** | Experience points (default: 0) |
| **Is Active** | Active/inactive toggle |

3. Click **Save**

### Student List View

| Column | Description |
|--------|-------------|
| Full Name | Student name |
| Parent | Linked parent |
| Grade Level | Grade |
| Enrollment Date | Join date |
| User Linked | ✅ if a user account exists |
| Is Active | Active status |
| Active Courses | Number of active enrollments |

Filter by active status, grade level, or enrollment date.

---

## 9. Managing Enrollments

### Enrolling a Student in a Course

1. Go to **Parents → Course Enrollments → Add**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Student** | Select student |
| **Course** | Select course |
| **Enrollment Date** | Date picker |
| **Status** | Pending Payment / Active / Completed / Paused / Cancelled |
| **Completion %** | 0–100 |
| **Current Level** | Student's current level in the course |

3. For paid enrollments, expand **Payment Details**:

| Field | Description |
|-------|-------------|
| **Amount Paid** | Payment amount |
| **Payment Reference** | Transaction ID |
| **Payment Date** | When payment was received |

4. Click **Save**

### Bulk Action: Activate Enrollments

Select multiple enrollments → choose **"Activate selected enrollments (Mark Paid)"** from the actions dropdown → click **Go**. This marks selected enrollments as Active.

---

## 10. Tracking Attendance

### Recording Attendance

1. Go to **Parents → Attendance Records → Add**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Student** | Select student |
| **Course** | Select course |
| **Date** | Date picker |
| **Status** | Present / Absent / Late / Excused |
| **Notes** | Optional notes |

3. Click **Save**

### Viewing Attendance

- Filter by status, course, or date range
- The list shows a **Notes** column (✅ if notes exist)
- Search by student name or course name

---

## 11. Progress Tracking

### Adding Progress Records

1. Go to **Parents → Progress Trackers → Add**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Student** | Select student |
| **Course** | Select course |
| **Skill Name** | Specific skill being tracked |
| **Proficiency Level** | Beginner / Intermediate / Advanced / Expert |
| **Score** | 0–100 |
| **Notes** | Additional comments |

3. Click **Save** — `last_updated` is set automatically

---

## 12. Trainer Feedback

### Adding Feedback

1. Go to **Parents → Trainer Feedback → Add**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Student** | Select student |
| **Course** | Select course |
| **Trainer Name** | Name of the trainer |
| **Feedback Date** | Date picker |
| **Category** | Behavior / Technical Skills / Creativity / Teamwork |
| **Rating** | 1–5 stars |
| **Feedback Text** | Detailed feedback comments |

3. Click **Save**

Filter feedback by category, rating, course, or date.

---

## 13. Certificates & Certifications

### Certification Courses

Go to **Certifications → Certification Courses** to manage courses eligible for certification.

| Field | Description |
|-------|-------------|
| **Name** | Course name |
| **Description** | About the certification |
| **Duration** | e.g., "8 Weeks" |
| **Level** | e.g., "Beginner to Advanced" |
| **Price** | Certification fee |
| **Image** | Course image |
| **Core Course** | Link to a core course (for progress tracking) |
| **WhatsApp Group Link** | Invite link for the class group |

### Issuing a Certificate

1. Go to **Certifications → Certificates → Add Certificate**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Certificate ID** | Unique ID (e.g., `INV-2026-001`) |
| **Student Name** | Recipient's full name |
| **Course** | Select the certification course |
| **Issue Date** | Date picker |
| **Issued By** | Issuing authority (default: "Inventobots Academy") |
| **Status** | Valid / Revoked |
| **Certificate Image** | Upload the certificate image |

3. Click **Save**

### Revoking a Certificate

- Open the certificate → change **Status** to **Revoked** → Save
- The public verification page will show the certificate as revoked

### Public Verification

Students and employers can verify certificates at:
```
https://yourdomain.com/certifications/
```
They enter the **Certificate ID** and the system displays the certificate details and status.

### Student Certificates (Linking)

Go to **Parents → Student Certificates** to link certificates to student profiles:

| Field | Description |
|-------|-------------|
| **Student** | Select student |
| **Certificate** | Select certificate |
| **Awarded Date** | Date picker |
| **Status** | Pending / Issued / Revoked |

---

## 14. Badges & Achievements

### Creating a Badge

1. Go to **Core → Badges → Add Badge**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Name** | Badge name (e.g., "5-Day Streak") |
| **Description** | What the badge represents |
| **Image** | Badge icon/image |
| **Criteria** | Internal code (e.g., `STREAK_5`, `FIRST_QUIZ`) |

3. Click **Save**

### Awarding a Badge to a Student

1. Go to **Core → Student Badges → Add**
2. Select the **Student** and **Badge**
3. The `earned_at` timestamp is set automatically
4. Click **Save**

---

## 15. Reports

### Generating a Report

1. Go to **Parents → Reports → Add Report**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Student** | Select student |
| **Report Type** | Type of report |
| **Period Start** | Report start date |
| **Period End** | Report end date |
| **Summary** | Text summary of the report |
| **File** | Upload a PDF or document |

3. Click **Save** — parents can view reports from their portal

---

## 16. Alerts

### Creating an Alert

1. Go to **Parents → Alerts → Add Alert**
2. Fill in:

| Field | Description |
|-------|-------------|
| **Student** | Select student |
| **Alert Type** | Type of alert |
| **Severity** | Severity level |
| **Message** | Alert message text |

3. Click **Save**

### Bulk Actions

| Action | Description |
|--------|-------------|
| **Mark as read** | Select alerts → "Mark selected alerts as read" → Go |
| **Mark as unread** | Select alerts → "Mark selected alerts as unread" → Go |

---

## 17. Quick Reference — Common Tasks

| Task | Where to Go |
|------|-------------|
| Add a new course | Core → Courses → Add |
| Feature a course on homepage slider | Core → Hero Slider Items → Add |
| Add a topic/lesson to a course | Core → Topics → Add |
| Create a quiz with questions | Core → Quizzes → Add (questions are inline) |
| Register a new parent | Auth → Users → Add User + Parent Profile |
| Add a student under a parent | Parents → Students → Add |
| Enroll a student in a course | Parents → Course Enrollments → Add |
| Record attendance | Parents → Attendance Records → Add |
| Track student progress | Parents → Progress Trackers → Add |
| Add trainer feedback | Parents → Trainer Feedback → Add |
| Issue a certificate | Certifications → Certificates → Add |
| Link certificate to student profile | Parents → Student Certificates → Add |
| Award a badge | Core → Student Badges → Add |
| Generate a report | Parents → Reports → Add |
| Send an alert to a parent | Parents → Alerts → Add |
| Activate pending enrollments | Parents → Course Enrollments → Select → Action: Activate |
| Revoke a certificate | Certifications → Certificates → Edit → Status: Revoked |
| Change admin panel URL | Edit `SECURE_ADMIN_URL` in `.env` |

---

*Document prepared by Nithil Suganthan — February 2026*
