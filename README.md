# InsightIQ — AI-Powered Analytics Dashboard

> A B2B internal analytics dashboard that lets teams track KPIs and generate actionable business insights using Claude AI in one click.

**Live Demo** → [https://ai-project-steel-psi.vercel.app](https://ai-project-steel-psi.vercel.app)  
**API Docs** → [https://insightiq-backend-f9q9.onrender.com/docs](https://insightiq-backend-f9q9.onrender.com/docs)

---

## What I Built

InsightIQ solves a real problem for B2B teams: **spending hours manually analyzing KPIs in spreadsheets to write reports that could be generated in seconds.**

The application has four core views:

- **Login / Register** — JWT-based authentication. Each team member has their own secure account.
- **Dashboard** — A real-time overview of KPIs across Sales, Marketing and Support, with trend cards and interactive charts (line, bar, pie) with a date range picker.
- **Metrics** — A full CRUD interface to add, edit, and delete business metrics. Includes form validation, loading states, empty states, and confirmation messages.
- **Insights IA** — The core AI feature. The user selects a category, clicks "Analyser avec Claude", and receives a structured business report in real time via streaming. All analyses are saved and exportable as PDF.

---

## Tech Stack

| Layer      | Technology                                          |
|------------|-----------------------------------------------------|
| Frontend   | Vue 3, Vite, Tailwind CSS, Pinia, Vue Router        |
| Backend    | Python 3.11, FastAPI, SQLAlchemy, Pydantic          |
| Database   | PostgreSQL                                          |
| AI         | Anthropic Claude (`claude-sonnet-4-20250514`)       |
| Auth       | JWT (python-jose + passlib bcrypt)                  |
| Deployment | Vercel (frontend) + Render (API + PostgreSQL)       |

---

## Features

### Core
- JWT authentication — register, login, protected routes, per-user sessions
- Dashboard with KPI cards and trend indicators
- Interactive charts — line, bar, pie with date range filtering
- Full CRUD for business metrics with form validation
- AI-powered analysis via Claude with structured prompt engineering

### Advanced
- Real-time streaming — Claude's response appears word by word via SSE
- PDF export — formatted reports downloadable directly from the browser
- Collapsible sidebar — smooth animation, icon-only mode with tooltips

---

## Project Structure
```
insightiq/
├── backend/
│   ├── main.py                      # FastAPI app entry point + CORS + router registration
│   ├── database.py                  # SQLAlchemy engine, session and Base declaration
│   ├── models.py                    # User, Metric, Insight ORM models with relationships
│   ├── schemas.py                   # Pydantic validation schemas (create, update, response)
│   ├── seed.py                      # Demo account seeder (demo@insightiq.com)
│   ├── routers/
│   │   ├── auth.py                  # Register, login, /me endpoints
│   │   ├── metrics.py               # CRUD endpoints — filtered by authenticated user
│   │   └── insights.py              # Claude generation + SSE streaming + history
│   ├── services/
│   │   ├── auth_service.py          # JWT creation, password hashing, get_current_user
│   │   ├── claude_service.py        # Claude API integration + prompt engineering
│   │   └── seed_service.py          # Auto-seeds 23 demo metrics for every new user
│   └── requirements.txt             # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── views/
│   │   │   ├── LoginView.vue        # Register + sign in with tabs, form validation
│   │   │   ├── DashboardView.vue    # KPI cards, line/bar/pie charts, date range filter
│   │   │   ├── MetricsView.vue      # Metrics table (desktop) + cards (mobile), CRUD
│   │   │   └── InsightsView.vue     # Claude generator with SSE streaming + history
│   │   ├── components/
│   │   │   ├── AppLayout.vue        # Collapsible sidebar + hamburger menu on mobile
│   │   │   ├── KpiCard.vue          # KPI summary card with trend badge
│   │   │   ├── MetricModal.vue      # Create / edit modal with full form validation
│   │   │   └── InsightCard.vue      # Insight display card with PDF export button
│   │   ├── stores/
│   │   │   ├── authStore.js         # Auth state — token, user, login, register, logout
│   │   │   ├── metricsStore.js      # Metrics state — fetch, create, update, delete
│   │   │   └── insightsStore.js     # Insights state — fetch, generate, SSE streaming
│   │   ├── services/
│   │   │   ├── api.js               # Axios instance + JWT interceptor + SSE stream helper
│   │   │   └── pdfExport.js         # Client-side PDF generation with jsPDF
│   │   └── router/
│   │       └── index.js             # Vue Router config + auth guards (redirect to /login)
│   └── package.json                 # Frontend dependencies
│
└── README.md                        # Project documentation 
```

## Key Technical Decisions

**FastAPI** — Auto-generates Swagger docs at `/docs`. Pydantic validation rejects invalid inputs automatically with correct HTTP status codes.

**Vue 3 + Pinia** — Composition API is simpler than React+Redux for this scope. Each resource (metrics, insights, auth) has its own isolated store.

**JWT Authentication** — Tokens stored in `localStorage`, injected via Axios interceptor. A 401 response auto-redirects to `/login`.

**Structured prompt** — Role + formatted data + 3-section output format guarantees consistent, displayable Claude responses every time.

**Streaming SSE** — Instead of waiting 5-10s, chunks arrive via Server-Sent Events and update the UI word by word using the native Fetch API.

---

## How I Used AI

Claude analyzes business metrics and generates a structured report with key trends, alert points, and 3 actionable recommendations. Without InsightIQ, a manager spends 2-3h/week on this — with InsightIQ it takes 10 seconds.

Error handling covers: `AuthenticationError`, `RateLimitError`, `APIConnectionError`, and generic exceptions — each returning a clear message in the UI.

Claude was also used throughout development for generating boilerplate, debugging, and improving prompt design.

---

## API Endpoints

| Method   | Endpoint                     | Auth | Description                        |
|----------|------------------------------|------|------------------------------------|
| `POST`   | `/api/auth/register`         | No   | Create a new account               |
| `POST`   | `/api/auth/login`            | No   | Login and receive JWT token        |
| `GET`    | `/api/auth/me`               | Yes  | Get current user info              |
| `GET`    | `/api/metrics/`              | Yes  | List metrics (filter by category)  |
| `POST`   | `/api/metrics/`              | Yes  | Create a new metric                |
| `PUT`    | `/api/metrics/{id}`          | Yes  | Update an existing metric          |
| `DELETE` | `/api/metrics/{id}`          | Yes  | Delete a metric                    |
| `POST`   | `/api/insights/generate`     | Yes  | Generate insight via Claude        |
| `POST`   | `/api/insights/stream`       | Yes  | Generate insight via SSE streaming |
| `GET`    | `/api/insights/`             | Yes  | List saved insights                |

---

## What I'd Improve With More Time

- Unit tests — pytest for FastAPI endpoints, vitest for Vue components
- Automatic alerts — trigger Claude analysis when a KPI crosses a threshold
- WebSockets — live metric updates without page refresh
- Multi-workspace — data isolation per team or department
- CSV import — bulk import metrics from a spreadsheet

---

## Local Setup

### Prerequisites
Python 3.11+, Node.js 20+, Docker Desktop, Git

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `backend/.env`:
```env
DATABASE_URL=postgresql://admin:secret@localhost:5432/insightiq
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxx
SECRET_KEY=your-secret-jwt-key
```

```bash
docker-compose up -d
python seed.py
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

> Run both terminals simultaneously — backend on :8000, frontend on :5173.

---

