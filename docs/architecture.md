# MindTrack — Architecture Notes

Extended documentation for the portfolio repository. See the root [README](../README.md) for the executive summary.

## API surface (conceptual)

| Prefix | Responsibility |
|--------|----------------|
| `/auth` | Registration, login, refresh tokens, session management |
| `/tasks` | Tasks, subtasks, categories, deadlines |
| `/ai` | Task chunking, Maya chat, reminder suggestions, rescue checks |
| `/focus` | Focus session start/end, duration stats |
| `/mood` | Mood check-ins for wellness tracking |
| `/gamification` | Points, badges, profile gamification state |
| `/admin` | User administration, audit logs (role-gated) |

## Cross-cutting concerns

1. **Authentication** — Bearer JWT on protected routes; `Depends(get_current_user)` pattern.
2. **Validation** — Pydantic request/response models; HTTP 400 with stable `detail` shapes.
3. **Errors** — HTTP exceptions mapped to JSON; unhandled exceptions logged server-side, generic 500 to clients.
4. **AI safety** — Timeouts, fallback copy, no stack traces in AI error responses.

## Data entities (PostgreSQL-oriented)

- **users** — credentials hash, profile, UI preferences, role
- **tasks** / **subtasks** — hierarchical work breakdown
- **user_sessions** — device/session tokens
- **focus_sessions** — timed work blocks
- **reminders** — user-defined notification config
- **ai_interactions** — audit trail for AI features
- **schema_migrations** — applied migration IDs

## Deployment assumptions (documentation only)

- `DATABASE_URL=postgresql://user:pass@localhost:5432/mindtrack_dev`
- `JWT_SECRET` — long random string, rotated per environment
- `LLM_API_KEY` — provider key loaded from environment, never from source control
