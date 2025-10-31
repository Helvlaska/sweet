# 💙 SWEET — PART 4: MVP DEVELOPMENT & EXECUTION

**Developer:** Claire Castan
**Project Period:** September 29 – October 31, 2025
**Duration:** 4 Weeks (Sprints 1 → 4)
**Holberton School – Foundations, Stage 4**

---

## 📘 PROJECT SCOPE

The **SWEET MVP** is a full-stack health-tracking web application designed to help users monitor and visualize their well-being data (glycemia, weight, mood, activity, meals, etc.).
It features secure authentication, modular Flask APIs, and a responsive React dashboard, focusing on accessibility, clarity, and data privacy.

The goal of this MVP stage was to **turn the technical documentation from Stage 3** into a working, testable prototype that demonstrates the full architecture in real conditions.

---

## ⚙️ TASK 0 – SPRINT PLANNING

| Sprint | Focus | Main Deliverables |
|--------|--------|------------------|
| **Sprint 1** | Backend Core | Flask setup, BaseModel, User model, Authentication routes |
| **Sprint 2** | Backend Data & Forum | Health-related entities (Glycemia, Weight, etc.), CRUD routes, testing |
| **Sprint 3** | Frontend Core | React setup, Authentication, Dashboard connection |
| **Sprint 4** | Frontend Features & QA | UI polish, Community section, testing, documentation |

**Methodology**
- Agile micro-sprints with daily retros (“What went well / To improve”).
- Git branching per feature (`feature/<entity>`), merged with `--no-ff`.
- Continuous QA using **Postman**, **Pytest**, and **Flask logs**.
- Daily documentation in `logbook.md`.

---

## 🧱 TASK 1 – DEVELOPMENT EXECUTION

### 🔹 Sprint 1 – Backend Foundation
- Set up Flask environment, config classes, and `.env` secrets.
- Built `BaseModel` (CRUD, timestamps, `to_dict`, logging).
- Implemented `User` model with full attribute validation via regex.
- Added authentication routes (`register`, `login`, `logout`, `reset`, `profile`).
- Configured JWT tokens in secure cookies (no localStorage).
- Migration setup with Flask-Migrate successfully tested.

### 🔹 Sprint 2 – Backend Completion
- Added health and social entities:
  `Glycemia`, `Weight`, `Activity`, `Meal`, `Medication`, `Mood`, `HealthProfessional`, `Note`, `ForumPost`, `Comment`, `Article`.
- Implemented CRUD services + routes for each entity using Flask Blueprints.
- Introduced refactoring to separate logic by domain (`*_routes.py`, `*_service.py`).
- Unified validation and error handling through centralized `validators.py` and `logging.py`.
- Fully validated backend via Postman (API routes, CRUD operations).
- Backend finalized and stable by **October 16th**.

### 🔹 Sprint 3 – Frontend Setup
- Initialized **React app** with structured folders:
  `/pages`, `/components`, `/services`, `/utils`.
- Installed and configured **SASS** (mixins, variables, mobile-first).
- Implemented **AuthContext**, **ProtectedRoute**, and **AppRouter**.
- Linked backend via Axios and secure cookies.
- Completed **multi-step Register** and **Login** forms with live user creation and redirect to dashboard.

### 🔹 Sprint 4 – Frontend Progress & Integration
- Implemented **Dashboard** featuring:
  - Cards for **Glycemia**, **Weight**, **Activity** using Chart.js.
  - Responsive design and date-based filters (week/month).
  - Navbar with logout and profile picture.
  - Dynamic Header with user greeting and current date.
- Data services: `glycemiaService.js`, `weightService.js`, `activityService.js`.
- Live CRUD operations tested successfully.
- Secondary cards (Mood, Meal, Medication) under development — planned for **V2**.

---

## 📊 TASK 2 – PROJECT TRACKING & ADJUSTMENTS

**Tracking Tools**

- Logbook (`logbook.md`) updated daily
- Commit convention: `:emoji: (scope): description`
- Branches merged with `--no-ff` and detailed messages

**Metrics**
- +300 commits total
- 95% feature completion vs. original plan
- Backend done mid-sprint 3 → enabled frontend focus
- QA, refactoring, and documentation included in parallel

**Adjustments**
- Extended work sessions during weekends to offset JWT/cookie learning time.
- Simplified QA strategy to focus on manual validation and stability.
- Prioritized maintainability and clarity over rapid feature expansion.

---

## 🔁 TASK 3 – SPRINT REVIEWS & RETROSPECTIVES

| Week | Focus | Achievements | Improvements |
|------|--------|--------------|---------------|
| **Week 1** | Backend Core | ✅ Clean architecture, BaseModel success | ⚠️ JWT/cookie complexity |
| **Week 2** | Entities & CRUD | ✅ Strong inheritance, reusable validators | ⚠️ Repetitive code pre-refactor |
| **Week 3** | Frontend Setup | ✅ React + AuthContext operational | ⚠️ Cookie/session persistence learning curve |
| **Week 4** | Integration & Testing | ✅ Dashboard functional, stable base | ⚠️ Missing secondary features (V2) |

Each sprint ended with a retrospective focused on autonomy, problem-solving, and planning accuracy.

---

## 🧩 TASK 4 – FINAL INTEGRATION & TESTING

### ✅ Backend Validation
- Implemented Pytest unit files for all models and routes.
- Some AI-generated tests were structurally inconsistent with the final architecture,
  leading to false negatives and excessive debugging time.
- Decision: prioritize **Postman testing** for realistic end-to-end validation.

### 🧪 Testing Strategy
- **Postman collection:** validated all endpoints (Auth, Data, Forum).
- **Logs:** used Flask `app.logger` for detailed tracking of CRUD actions and token generation.
- **Integration:** React ↔ Flask fully connected via secure JWT cookies.
- **Charts:** display dynamic data from API in real time (weight, glycemia, activity).

> 🔹 Although automated Pytests returned structural errors,
> the **Postman validation confirmed the functional reliability of the entire MVP**.
> This pragmatic decision allowed focusing on core stability instead of debugging non-conforming test files.

---

## 🧱 MVP STATUS

While the **core MVP** is functionally complete (authentication, data tracking, dashboard visualization),
a few secondary components — notably the cards for **Mood**, **Meal**, and **Medication** —
are still in progress and planned for **Version 2**.

All backend features are stable, tested, and integrated with the frontend.
The foundation is ready for expansion and UI polish during the next iteration.

---

## 📦 TASK 5 – FINAL DELIVERABLES

| Type | Description | Status | Location |
|------|--------------|--------|-----------|
| 🗂️ Repository | Complete SWEET project | ✅ | [helvlaska/sweet](https://github.com/Helvlaska/sweet) |
| 📋 Logbook | Daily progress documentation | ✅ | branch `logbook` `/docs/logbook.md` |
| 🧱 Planning | Sprint breakdown & objectives | ✅ | `/docs/stage3_report.pdf` |
| ⚙️ Backend | Flask REST API with SQLAlchemy + JWT cookies | ✅ | `/backend/` |
| 💻 Frontend | React + SASS + Chart.js | ✅ | `/frontend/` |
| 🧪 Testing | Postman + logs (Pytest under revision) | ✅ | `/tests/` |
| 📘 Technical Docs | UML, API routes, architecture diagrams | ✅ | `/docs/` |
| 🚀 MVP | Fully functional core version | ✅ | Local server (`http://127.0.0.1:5000`) |

---

## 💬 CONCLUSION

The MVP successfully demonstrates:
- A secure and modular **Flask backend** with clean inheritance.
- A **React frontend** connected through secure JWT cookies.
- Full CRUD functionality validated through **Postman** and **manual testing**.
- Solid integration and logging pipelines ensuring maintainability.

Although automated testing (Pytest) will be rewritten for **Version 2**,
the project already meets all pedagogical objectives of Stage 4:
**planning, building, integrating, testing, and documenting** a complete full-stack application.

Remaining features are clearly identified and scheduled for improvement in the next iteration.
This deliverable proves professional-level organization, foresight, and problem-solving under real project conditions.

---

**End of Stage 4 — MVP functionally complete.**
_“A well-prepared project is already halfway to success.”_
