# SWEET - Stage 5 Final Report

## 1. Results Summary

Sweet is an application designed to support people with diabetes by centralizing their daily health data (glycemia, weight, activity, meals, medication, and mood) into a clear and intuitive dashboard.
The goal for the MVP was to deliver a functional, easy-to-use, secure, and genuinely helpful tool for patients.

The delivered MVP fully meets these objectives.
Users can record their data, track their evolution over time, visualize trends through charts, manage their medication, health professionals and notes, access an article section, and update their personal profile.
The responsive design is fully implemented on the landing page, login page, and register page, and the application remains usable on mobile for all features. A complete mobile-first approach is planned for the next iteration.

### Architecture

The chosen stack — React (frontend), Flask (backend), and MySQL (database) — enabled the creation of a modern, structured, and maintainable application.
The backend handles all business logic, the frontend focuses on the user interface, and the database ensures reliable and consistent data storage.

### Key Technical Metrics

- 13 database entities (12 main entities + BaseModel)
- 43,881 lines of code
- 226 commits
- 72 backend services
- 32 API routes

### Delivered Features

- Full authentication system (register, login, logout)
- User profile management
- Recording and consultation of all health data (glycemia, weight, activity, meals, mood)
- Medication management (dose, stock, tracking)
- Health professionals + notes
- Data aggregation (daily averages) and Chart.js visualization
- Articles section (admin only)
- Responsive interface (main pages fully responsive)
- The MVP covers nearly all objectives defined in earlier stages.

---

## 2. Lessons Learned

Developing Sweet has been an extremely rich experience, both technically and personally.
Working alone on a project of this scale required strong organization, consistency, and continuous skill-building.

### Organization and Work Method

Very early in the project, it became clear that traditional project management tools did not perfectly match the workflow needed.
A personal logbook quickly became the most efficient solution.

Every morning: write down the goals.
Every evening: review progress and analyze difficulties.

This simple but powerful system kept the project structured, focused, and moving forward consistently.

### Architecture and Code Structure

With 13 entities, multiple relationships, and significant business logic, the architecture needed to be robust:

- a shared BaseModel (generic CRUD + timestamps),
- a clean separation into models / services / routes,
- strict division of responsibilities between the frontend, backend, and database.

This architecture proved to be reliable, maintainable, and scalable.

### Managing the Project’s Volume

The large number of services, routes, forms, and validations required constant technical discipline.
This repetition allowed for deeper understanding of:

- API design,
- data modelling,
- error handling,
- consistency across features,
- and backend architecture.

Despite the complexity, the project remained coherent thanks to a strong structure.

### Security and Data Protection

Security was a central concern throughout the entire project, since Sweet handles sensitive medical and personal data.

Several strategies were implemented:

- Authentication
  - JWT stored in httpOnly cookies
  - Access/refresh token system (including a “remember me” option)

- Data Protection
  - Password hashing with bcrypt
  - Strict validation for all fields using regex
  - Whitelist-style validation to prevent malicious input

- Form Security
  Sweet includes a very large number of forms (glycemia, activity, meals, mood, weight, medication, notes, pros, profile…).
  Each form required:

  - type validation
  - format validation
  - boundary checks
  - input cleaning
  - detailed error logging

- Logging as a Testing Tool
  A very advanced logging system was implemented.
  Every service call, every route, every validation, and every error is fully traceable.

  This system acted as an internal audit tool, enabling:
  - fast debugging,
  - precise tracking of backend behavior,
  - confidence in the correctness of the application.

For an MVP, this method proved extremely effective and adapted to the project timeline.

### Data Visualization and Aggregation

To keep charts readable, a custom aggregation system was designed:

- grouping values by date,
- computing daily averages,
- generating labels dynamically.

This produced clean, informative visuals that are relevant for both patients and healthcare professionals.

### Responsive Design and UI

Only the landing, login, and register pages are fully responsive, but this led to valuable insights:

- the importance of a mobile-first strategy,
- the need for a consistent breakpoint system,
- the impact of UI/UX decisions on scalability.

A complete responsive refactor is planned for the next iteration and for the future mobile version of Sweet.

### Autonomy and Confidence

Handling all aspects of the project — backend, frontend, database, security, architecture, UI/UX, QA, and project management — significantly increased autonomy, confidence, and full-stack understanding.

## 3. Retrospective

As the sole developer, you fulfilled every role: backend engineer, frontend engineer, database designer, UI/UX designer, QA, SCM, and project manager.

### What Worked Well

- The logbook as a powerful daily management tool
- A clean and modular backend architecture
- Strong validation and security practices
- A highly effective logging system used as a testing method
- Maintaining overall coherence despite the project’s size

### Challenges

- Managing all roles alone
- The high volume of entities and business logic
- Completing full responsive design within the timeline
- Maintaining consistency and motivation during the most intensive development phases

### Improvements for Future Iterations

- Adopting a mobile-first responsive approach
- Increasing modularity for future scalability
- Preparing deployment and a cloud-ready architecture
- Adding automated tests in later versions (not needed for the MVP)

## 4. Conclusion

Sweet is a project born from a personal story and driven by a genuine intention to help diabetic patients better understand their daily health and feel supported.

- The delivered MVP is:
  - functional,
  - stable,
  - structured,
  - secure,
  - and technically solid.

- The next steps are already planned:
  - deploying the application online,
  - completing a full responsive refactor,
  - building a mobile version,
  - adding intelligent statistics and alert systems.

Sweet demonstrates the ability to deliver a complete full-stack project — from concept to architecture, from backend to frontend — while maintaining clarity, structure, and a human-centered approach.

It is a project to be proud of: useful, real, structured, and deeply meaningful.
