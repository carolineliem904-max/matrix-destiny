# Matrix Destiny

Bilingual Destiny Matrix MVP for educational self-reflection. The current calculation methodology is intentionally marked `unverified-v0` until definitive formulas are supplied.

## Structure

- `frontend/` - Next.js App Router, TypeScript, Tailwind CSS, SVG chart UI
- `backend/` - FastAPI calculation and interpretation API
- `docs/` - methodology checklist and product notes
- `product_plan.md` - milestone plan and guardrails

## Safety Guardrails

- Calculations are deterministic and separate from interpretations.
- Placeholder values are never labeled as verified.
- AI is not used in the first MVP and must never calculate matrix values.
- Readings are presented for reflection and entertainment, not scientific or predictive claims.

## Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

## Frontend

```bash
cd frontend
npm install
npm run dev
```

By default the frontend calls `http://localhost:8000`. Set `NEXT_PUBLIC_API_BASE_URL` to change that.

## Calculator Navigation

- `/` remains the public calculator and continues to use the intentionally
  unverified `unverified-v0` methodology.
- `/lab/mahesa-gantari` is the feature-flagged experimental calculator for the
  course-transcribed `mahesa-gantari-rws-v0.1` methodology. It is not public by
  default and remains `verified: false`.

## Local Teacher Teaser Preview

The experimental `teacher-teaser-v0.1` endpoints are disabled by default. For
local visual inspection, create `backend/.env` from `backend/.env.example` and
set:

```bash
ENABLE_EXPERIMENTAL_METHODOLOGIES=true
```

Do not commit `backend/.env`. Start the backend and frontend normally, then open:

```text
http://localhost:3000/lab/teacher-teaser
```

The preview remains unverified, displays only explicitly supported positions,
and does not change the public calculator methodology.
