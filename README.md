<p align="center">
  <img src="assets/logo.png" alt="MindTrack ADHD System Logo" width="300"/>
</p>

<p align="center">
  <img src="assets/banner.svg" alt="MindTrack banner" width="100%"/>
</p>

<h1 align="center">MindTrack · ADHD System</h1>

<p align="center">
  <strong>A Smart Task Organizer for University Students with ADHD — powered by AI</strong>
</p>

<p align="center">
  <a href="https://flutter.dev/"><img src="https://img.shields.io/badge/Flutter-Dart-02569B?style=for-the-badge&logo=flutter&logoColor=white" alt="Flutter"/></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/></a>
  <a href="https://fastapi.tiangolo.com/"><img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/></a>
  <a href="https://www.sqlite.org/"><img src="https://img.shields.io/badge/SQLite-Storage-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/></a>
  <a href="https://ai.google.dev/"><img src="https://img.shields.io/badge/Google-Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Google Gemini"/></a>
  <a href="#"><img src="https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT"/></a>
</p>

<p align="center">
  <a href="https://github.com/raghadalb-tech"><img src="https://img.shields.io/badge/GitHub-raghadalb--tech-181717?style=for-the-badge&logo=github" alt="GitHub"/></a>
  <a href="https://www.linkedin.com/in/raghad-a-53b503395"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Graduation%20Project-64748b?style=for-the-badge" alt="License"/></a>
</p>

<p align="center">
  <em>📂 Portfolio documentation — architecture, features & backend highlights · Full source not published</em>
</p>

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#core-features">Features</a> •
  <a href="#system-architecture">Architecture</a> •
  <a href="#tech-stack">Tech Stack</a> •
  <a href="#my-role">My Role</a> •
  <a href="#code-highlights">Code</a>
</p>

---

## Overview

**MindTrack** is a graduation project (Princess Nourah bint Abdulrahman University, Aug 2025 – May 2026) that helps university students—especially those with **ADHD**—plan, break down, and complete academic work without cognitive overload.

Instead of a flat to-do list, the app turns large assignments into **small, actionable steps**, supports **focus sessions**, and tracks **progress** with encouragement suited to executive-function challenges.

I built the complete app as the **sole developer**: the Flutter mobile client, the FastAPI backend, the data layer and the Google Gemini integration.

<p align="center">
  <img src="assets/app-mockup.svg" alt="MindTrack illustrative app mockup" width="92%"/>
</p>

### Target audience

| | |
|:---:|:---|
| 🎯 **Primary** | University students with ADHD — overwhelm, time blindness, difficulty starting |
| 📚 **Secondary** | Neurotypical students needing structured planning for heavy course loads |

<table>
<tr>
<td width="50%" bgcolor="#ede9fe">

**Design for ADHD**

- Short AI responses  
- One next step at a time  
- Clear deadline priorities  

</td>
<td width="50%" bgcolor="#ccfbf1">

**Built for trust**

- Non-punitive errors when AI is busy  
- Real task context in every AI request  
- Secure JWT-backed API  

</td>
</tr>
</table>

---

## Core features

<p align="center">
  <img src="assets/features-overview.svg" alt="MindTrack core features overview" width="100%"/>
</p>

| Feature | What it does |
|---------|----------------|
| 🧠 **AI task breakdown** | Google Gemini decomposes tasks into ordered subtasks with structured, JSON-validated outputs |
| 💬 **Maya AI assistant** | Arabic-first assistant powered by Gemini, grounded in the user's real tasks & deadlines |
| ⏱️ **Focus mode** | Timed sessions linked to tasks, habit tracking, gamification hooks |
| 📊 **Progress tracking** | Tasks, subtasks, mood check-ins, badges & streaks (gamification engine) |
| 🆘 **Rescue & reminders** | Proactive checks & smart reminder suggestions |
| 🔐 **Security layer** | JWT auth, middleware, structured exception handling, CORS |

---

## System architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'primaryColor': '#ede9fe', 'primaryTextColor': '#4c1d95', 'primaryBorderColor': '#7c3aed', 'lineColor': '#0d9488', 'secondaryColor': '#ccfbf1', 'tertiaryColor': '#f1f5f9'}}}%%
flowchart LR
    subgraph Client["📱 Mobile"]
        APP["Flutter / Dart App"]
    end

    subgraph API["⚡ FastAPI"]
        MW["Middleware"]
        AUTH["JWT Auth"]
        R["Routers"]
        MW --> AUTH --> R
    end

    subgraph Data["🗄️ Data"]
        DB[("SQLite")]
    end

    subgraph AI["🤖 AI"]
        P["Context builder + JSON validation"]
        L["Google Gemini"]
        P --> L
    end

    APP -->|HTTPS| MW
    R --> DB
    R --> P
```

<details>
<summary><strong>📁 Repository layout</strong></summary>

```
mindtrack-portfolio/
├── README.md
├── assets/              # Banners & illustrations (SVG)
├── core_snippets/       # Curated FastAPI highlights
├── docs/architecture.md
└── .env.example
```

</details>

---

## Tech stack

<p align="center">

| Layer | Stack |
|:------:|:------|
| 📱 **Mobile** | Flutter · Dart |
| ⚙️ **Runtime** | Python 3.11+ |
| 🚀 **API** | FastAPI · Pydantic · Uvicorn |
| 🗄️ **Database** | SQLite *(app)* · snippets written for PostgreSQL |
| 🔑 **Auth** | JWT access/refresh · salted password hashing |
| 🤖 **AI** | Google Gemini · structured JSON outputs · timeouts & fallbacks |
| 🛡️ **Ops** | Env config · structured logging · global exception handlers |

</p>

---

## My role

> Sole developer — mobile client, backend, data layer and AI integration.
> Snippets in [`core_snippets/`](core_snippets/) use **mock config** — no API keys or secrets.

### Flutter mobile client

- Complete Flutter/Dart app: tasks, AI breakdown, focus sessions, reminders, progress and gamification screens
- Arabic-first experience for the Maya assistant

### FastAPI backend APIs

- **Modular routers** — `/auth` · `/tasks` · `/ai` · `/focus` · `/gamification` · `/mood` · `/admin`
- **Lifespan hooks** — DB init & health checks at startup
- **REST endpoints** — CRUD, profile, focus sessions, admin (role-based)
- **Error contract** — Global handlers → predictable JSON for clients

### Database design

> The app runs on **SQLite**. Portfolio snippets are written for **PostgreSQL** with the same relational model.

- Users, tasks, subtasks, sessions, reminders, mood, gamification, AI logs
- **Versioned migrations** — non-destructive schema evolution
- **Indexes** on foreign keys & WAL-friendly settings

### AI integration (Google Gemini)

- **Task chunking** — small steps, JSON-only, post-parse validation
- **Context injection** — real deadlines & reminders in Arabic context
- **Reliability** — thread timeouts, `asyncio.wait_for`, friendly 503 UX
- **Audit trail** — `ai_interactions` logging for demos & debugging

---

## Code highlights

| | File | Shows |
|:---:|:-----|:------|
| 🔧 | [`01_request_logging_middleware.py`](core_snippets/01_request_logging_middleware.py) | Request ID, latency logging, safe errors |
| 📋 | [`02_tasks_api_route.py`](core_snippets/02_tasks_api_route.py) | Pydantic models, DB injection, REST tasks |
| 🤖 | [`03_ai_task_breakdown_service.py`](core_snippets/03_ai_task_breakdown_service.py) | Gemini service wrapper, JSON parse, timeouts, mock LLM |

---

## Privacy notice

- No production `.env`, API keys, or database dumps
- Snippets are representative; redacted for public portfolio review

---

## Author

<p align="center">
  <strong>Raghad Al-Bishri</strong> · Full-Stack Engineer<br/>
  <sub>Flutter · FastAPI · Google Gemini · API security</sub>
</p>

<p align="center">
  <a href="https://github.com/raghadalb-tech"><img src="https://img.shields.io/badge/View-GitHub%20Profile-181717?style=flat-square&logo=github" alt="GitHub profile"/></a>
  <a href="https://www.linkedin.com/in/raghad-a-53b503395"><img src="https://img.shields.io/badge/LinkedIn-Raghad%20Al--Bishri-0A66C2?style=flat-square&logo=linkedin" alt="LinkedIn"/></a>
</p>

---

<p align="center">
  <sub>Private graduation project · All rights reserved · <a href="LICENSE">License</a></sub>
</p>
