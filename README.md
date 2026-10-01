# SidiWeb

Intelligent website-builder platform. Monorepo with three services:

| Folder | Service | Stack | Default port |
|---|---|---|---|
| [`backend/`](backend/) | REST API (auth, sites, templates, media, recommendations) | Python / FastAPI + MongoDB | 8000 |
| [`ai/`](ai/) | Template / color / font recommendation engine | Python / LangChain | 5001 |
| [`frontend/`](frontend/) | Web client | React 19 + Vite + Tailwind | 5173 |

> Note on stacks: the backend is implemented in **FastAPI** (not Node/Express) and the AI
> service uses **LangChain** (not scikit-learn). The spec's data model, JWT (HS256, 24h) and
> bcrypt hashing are honored.

## Run with Docker (recommended)

The whole stack — MongoDB, backend, AI service, frontend — runs with one command:

```bash
cp .env.example .env     # optional: set JWT_SECRET_KEY, GOOGLE_API_KEY, and host ports
docker compose up --build
```

Then open:
- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs
- AI service: http://localhost:5001

If a default port is already in use on your machine, override it in `.env`
(`BACKEND_PORT`, `FRONTEND_PORT`, `MONGO_PORT`). Stop everything with `docker compose down`
(add `-v` to also drop the Mongo data volume).

The 12 templates seed into MongoDB on first backend startup. The AI service needs a
`GOOGLE_API_KEY` (Gemini) to return live recommendations; without it the backend falls back
to catalogue-based suggestions, so the app still works.

---

## Run without Docker

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+
- MongoDB (local or Atlas)
- `libmagic` for backend image validation (`brew install libmagic` on macOS)

## Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in JWT_SECRET_KEY, MONGODB_URI, etc.
uvicorn main:app --reload --port 8000
# API docs: http://localhost:8000/docs
```
The 12 templates are seeded into MongoDB automatically on first startup.

## AI service
```bash
cd ai
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in OPENAI_API_KEY
python api/app.py             # serves on http://localhost:5001
```

## Frontend
```bash
cd frontend
npm install
cp .env.example .env          # VITE_API_BASE_URL -> backend URL
npm run dev                   # http://localhost:5173
```

## Development workflow
GitFlow-style: `main` is the stable branch; feature work happens on `feat/*` branches and is
reviewed before merging. Merges to `main` require review by the lead/co-lead.
