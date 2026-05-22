# Core Snippets

Curated **FastAPI / Python** highlights from MindTrack backend development. These files are **self-contained**, use **mocked configuration**, and contain **no API keys or production secrets**.

| File | Topic |
|------|--------|
| `01_request_logging_middleware.py` | ASGI middleware, request IDs, global exception handlers |
| `02_tasks_api_route.py` | REST tasks API with Pydantic + SQLAlchemy-style PostgreSQL access |
| `03_ai_task_breakdown_service.py` | AI chunking prompts, JSON parsing, timeouts, mock LLM client |

They are illustrative for portfolio review and may be run only after installing dependencies (`fastapi`, `sqlalchemy`, etc.) and pointing `DATABASE_URL` at a local dev database.
