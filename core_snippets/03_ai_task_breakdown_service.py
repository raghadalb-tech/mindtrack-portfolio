"""
MindTrack — AI task breakdown service wrapper (portfolio snippet).

Demonstrates: prompt templates, structured JSON parsing, timeouts,
graceful ADHD-friendly fallbacks, and mocked LLM configuration.

NO real API keys — LLM calls are simulated for documentation.
"""

from __future__ import annotations

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import dataclass
from typing import Any, Callable, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

logger = logging.getLogger("mindtrack.ai")

# Mocked provider settings
LLM_SETTINGS = {
    "API_KEY": os.getenv("LLM_API_KEY", "mock-key-replace-in-env"),
    "MODEL": "gemini-1.5-flash",
    "TIMEOUT_SECONDS": 15,
}

router = APIRouter(prefix="/ai", tags=["AI Features"])


def get_current_user_id() -> int:
    return 1


# --- Request / response models ---

class ChunkTaskRequest(BaseModel):
    task_title: str = Field(..., min_length=1, max_length=300)
    task_description: Optional[str] = Field(default=None, max_length=2000)
    task_id: Optional[int] = None


class SubtaskSuggestion(BaseModel):
    title: str
    order: int = 0


class ChunkTaskResponse(BaseModel):
    subtasks: List[SubtaskSuggestion]
    count: int


# --- Prompt engineering ---

CHUNK_SYSTEM_PROMPT = """You are Maya, an ADHD-friendly academic coach.
Break the student's task into 3–7 very small, concrete steps.
Rules:
- Respond with JSON only: {"subtasks": [{"title": "...", "order": 0}, ...]}
- Each step must be doable in under 25 minutes
- Use simple, encouraging language
- No markdown, no extra keys
"""


def build_chunk_user_prompt(title: str, description: Optional[str]) -> str:
    parts = [f"Task title: {title}"]
    if description:
        parts.append(f"Details: {description}")
    return "\n".join(parts)


def _clean_json_text(raw: str) -> str:
    s = (raw or "").strip()
    if s.startswith("```"):
        s = s.replace("```json", "").replace("```", "").strip()
    return s


def parse_subtasks_payload(raw: str) -> List[SubtaskSuggestion]:
    data = json.loads(_clean_json_text(raw))
    items = data.get("subtasks") or []
    out: List[SubtaskSuggestion] = []
    for i, item in enumerate(items):
        title = (item.get("title") or "").strip()
        if not title:
            continue
        out.append(SubtaskSuggestion(title=title, order=int(item.get("order", i))))
    if not out:
        raise ValueError("Model returned no valid subtasks")
    return out


# --- Mock LLM client (portfolio: swap for real SDK) ---

@dataclass
class MockLLMClient:
    api_key: str

    def generate(self, system: str, user: str) -> str:
        if not self.api_key or self.api_key == "mock-key-replace-in-env":
            raise RuntimeError("LLM API key not configured")
        # Simulated model output for documentation
        return json.dumps(
            {
                "subtasks": [
                    {"title": "Open the assignment brief and highlight due dates", "order": 0},
                    {"title": "List three resources you already have (slides, notes)", "order": 1},
                    {"title": "Draft a 5-bullet outline in 15 minutes", "order": 2},
                ]
            },
            ensure_ascii=False,
        )


def _get_llm_client() -> MockLLMClient:
    return MockLLMClient(api_key=LLM_SETTINGS["API_KEY"].strip())


def _run_with_timeout(fn: Callable[[], Any], *, timeout_s: int) -> Any:
    with ThreadPoolExecutor(max_workers=1) as pool:
        fut = pool.submit(fn)
        try:
            return fut.result(timeout=timeout_s)
        except FuturesTimeout:
            raise HTTPException(
                status_code=503,
                detail="AI is busy. Please try again in a minute.",
            )


def chunk_task_sync(body: ChunkTaskRequest) -> ChunkTaskResponse:
    client = _get_llm_client()

    def _call() -> str:
        # Real integration: client.models.generate_content(...)
        return client.generate(
            CHUNK_SYSTEM_PROMPT,
            build_chunk_user_prompt(body.task_title, body.task_description),
        )

    try:
        raw = _run_with_timeout(_call, timeout_s=LLM_SETTINGS["TIMEOUT_SECONDS"])
        subtasks = parse_subtasks_payload(raw)
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("chunk-task failed: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="AI is temporarily unavailable. Try a smaller task description.",
        )

    return ChunkTaskResponse(subtasks=subtasks, count=len(subtasks))


@router.post("/chunk-task", response_model=ChunkTaskResponse)
def chunk_task(
    body: ChunkTaskRequest,
    user_id: int = Depends(get_current_user_id),
) -> ChunkTaskResponse:
    _ = user_id  # Persist subtasks & ai_interactions in full implementation
    return chunk_task_sync(body)
