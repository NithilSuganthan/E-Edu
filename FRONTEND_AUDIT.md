# FRONTEND AUDIT — Inventobots Academy
Date: 26 Aug 2026. Based on actually running the site and inspecting rendered HTML
(all public pages + authenticated parent/student portals + admin), plus template/JS review.

## Scores

| Dimension | Score /10 | Notes |
|---|---|---|
| Overall frontend | **6.5** | Solid visual identity, but had several dead links, a missing page, and mocked features |
| Visual design | 7.5 | Consistent Tailwind design language in portals; polished login/register screens |
| UX | 6 | Clear CTAs mostly; broken "Continue Learning", dead lab CTAs, no password reset |
| Mobile responsiveness | 6.5 | Responsive Tailwind classes everywhere (verified by markup review); real-device testing NOT performed — see limitations |
| Accessibility | 6 | Good aria usage on dashboard; 12 imgs lacked alt text (fixed); contrast generally good |
| Performance | 5.5 | Tailwind CDN (~300KB JS) + lucide CDN on every page; N+1 queries in dashboards |
| Consistency | 6 | Public site is light-themed; portals force dark mode; two font families (Outfit vs Poppins); admin is a third look |

## CRITICAL ISSUES (fixed unless noted)

1. **Parent → Student details page: HTTP 500**
   - Page: `/parents/student/<id>/` — `student_detail.html` did not exist.
   - Why it matters: any click-through to a child's detailed report crashed the app.
   - Fix: created `parents/templates/parents/student_detail.html` matching dashboard design (enrollments, attendance table, feedback, skills, certificates, reports, alerts) and added a "View Details →" link on each student card.

2. **Student dashboard: "Continue Learning" was `href="#"`**
   - Why it matters: primary action of the student LMS did nothing.
   - Fix: links to the course player when enrolled+active; renders disabled state otherwise.

3. **Student dashboard pending-payment cards had NO online payment path**
   - Only a hardcoded WhatsApp link existed although the Razorpay checkout flow exists.
   - Fix: added "Pay Now (Online)" button → existing payment route; kept WhatsApp as secondary.

## HIGH PRIORITY

4. **Public Lab page: all 4 locked-feature CTAs were `href="#"`** (Code Studio, Circuit, Abacus, Memory).
   - Fix: now point to student login.
5. **Parent dashboard rendered empty course names** (`enrollment.course.name` — field doesn't exist, it's `.title`).
   - Fix: corrected field reference.
6. **Parent dashboard rendered empty certificate titles** (`cert.certificate.title` doesn't exist).
   - Fix: now shows course title + certificate ID.
7. **Parent login "Forgot password?" was a dead `#` link.**
   - Fix: replaced with static hint ("Contact the academy office") until a reset flow is built.

## MEDIUM PRIORITY (documented, not all fixed)

8. **Dark mode toggle is fake**: `theme.js` hardcodes `darkMode: true` for everyone. Light theme unreachable. (Left as-is — intentional current product decision.)
9. **Code Studio output is simulated** (`lab.js runCode()` fakes compile after 800ms). Must be disclosed to reviewers as MOCKED.
10. **Tailwind via CDN** (`cdn.tailwindcss.com`) prints a console warning and is not for production builds; ~300KB render-blocking JS per page.
11. **Two font families** across portals (Poppins vs Outfit) — minor brand inconsistency.
12. Student recommendations link to `#` (backend provides no target page yet).

## LOW PRIORITY

13. `unpkg.com/lucide@latest` unpinned version — supply-chain/update risk.
14. Admin panel uses Django default styling beyond jazzmin skin — acceptable.

## COSMETIC

15. Mixed icon animation styles between hero slider and portals.
16. Empty states exist and are good (dashboard cards) — keep this pattern elsewhere.

## Fixed accessibility issues
- Added `alt` attributes to 12 `<img>` elements (browse courses ×8, sidebar avatars ×2, my-courses, settings).
- Added `loading="lazy"` to below-fold images.
- Kept existing `aria-*`, `sr-only`, progressbar roles (already decent).

## What I verified but did NOT test
- Real browser console errors / pixel rendering on physical devices (no browser automation available). Markup-level checks only.
