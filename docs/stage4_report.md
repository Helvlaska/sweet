🩵 SWEET — PART 4: MVP DEVELOPMENT AND EXECUTION
--------------------------------------------------

👩‍💻 Developer: Claire Castan
📅 Delivery Date: [to be completed]
🎯 Objective: Delivery of the complete MVP (backend + frontend + QA) based on the technical documentation from Part 3.

# 🔗 GitHub Links
--------------------------------------------------
- Main branch (full code):
  [https://github.com/Helvlaska/sweet] – Main branch

- Logbook branch (daily progress):
  [https://github.com/Helvlaska/sweet] – Logbook branch


# 🧱 Project Structure
--------------------------------------------------
**Backend (Flask)** – Completed
- `/app/`: models, routes, services, utils
- `requirements.txt`: dependencies
- `migrations/`: database management
- Tests: Pytest / Postman (see `/tests`) – under review and corrections

**Frontend (React)** – In progress
- `/src/`: pages, components, API services
- `package.json`: dependencies
- Styling: SASS (mobile-first)
- Tests: Jest / React Testing Library


# 🗓️ Completed Sprints
--------------------------------------------------
| Sprint | Period | Main Objective | Status |
|--------|----------|----------------|--------|
| 1 | Weeks 1–2 | Authentication + Backend Core | ✅ |
| 2 | Weeks 3–4 | CRUD Data Health + Professionals + Notes | ✅ |
| 3 | Weeks 5–6 | Frontend Auth + Dashboard | 🔁 |
| 4 | Weeks 7–8 | Forum, Articles, Final UI + QA | 🔁 |



# 🧪 Testing and Quality
--------------------------------------------------
- ✅ Postman tests on all main routes (auth, data, pros, notes, forum, articles)
- ✅ Centralized logs in `/app/logs/`
- ✅ Role management (user/admin)
- ✅ JWT tokens with httpOnly cookies
- 🔁 Responsive and consistent UI (SASS, mobile-first)
- 🔁 Final QA validation (manual tests and bug fixes)


# 🚀 How to Run the Project
--------------------------------------------------
**Backend:**
```bash
cd backend
python3 run.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

---

**Local Access:**
- Frontend → http://127.0.0.1:5173
- Backend → http://127.0.0.1:5000


# 📚 Included Documentation
- logbook.md: complete development journal (logbook branch)
- README.md: installation and overview guide

**✅ Deliverables Summary**
Flask Backend (complete)	✅	/app
React Frontend (complete)	✅	/src
Technical Documentation	✅	/docs
Logbook	✅	logbook branch
Postman / QA Tests	✅	/tests
Executable MVP	🔁	Local or demo video

🗂️ Annexes (Upcoming)
- Demo screenshots
- Test results (logs / screenshots)
- Final sprint retrospective notes
