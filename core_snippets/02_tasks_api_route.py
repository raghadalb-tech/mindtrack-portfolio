"""
MindTrack — Structured tasks API route (portfolio snippet).

Demonstrates: APIRouter, Pydantic v2 models, dependency-injected DB session,
parameterized SQL, and auth-gated endpoints.

Uses a mocked PostgreSQL URL — no real credentials.
"""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Annotated, Generator, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Connection, Engine

# Mock configuration for documentation only
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://mindtrack_app:changeme@localhost:5432/mindtrack_dev",
)

engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)
router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_db() -> Generator[Connection, None, None]:
    with engine.connect() as conn:
        yield conn


# --- Auth stub (portfolio: replace with real JWT dependency) ---

def get_current_user_id() -> int:
    """Stand-in for Depends(get_current_user) → user id."""
    return 1


# --- Schemas ---

class SubtaskOut(BaseModel):
    id: int
    title: str
    done: bool


class TaskOut(BaseModel):
    id: int
    title: str
    category: str = "assignment"
    deadline: Optional[str] = None
    is_completed: bool
    subtasks: List[SubtaskOut] = Field(default_factory=list)


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(default="assignment", max_length=50)
    deadline: Optional[str] = Field(default=None, description="ISO date YYYY-MM-DD")


# --- Routes ---

@router.get("", response_model=List[TaskOut])
def list_tasks(
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Connection, Depends(get_db)],
) -> List[TaskOut]:
    rows = db.execute(
        text(
            """
            SELECT t.id, t.title, t.category, t.deadline, t.is_completed
            FROM tasks t
            WHERE t.user_id = :uid
            ORDER BY t.deadline NULLS LAST, t.id DESC
            """
        ),
        {"uid": user_id},
    ).mappings().all()

    result: List[TaskOut] = []
    for row in rows:
        sub_rows = db.execute(
            text(
                """
                SELECT id, title, done
                FROM subtasks
                WHERE task_id = :tid
                ORDER BY id ASC
                """
            ),
            {"tid": row["id"]},
        ).mappings().all()
        result.append(
            TaskOut(
                id=row["id"],
                title=row["title"],
                category=row["category"],
                deadline=row["deadline"],
                is_completed=bool(row["is_completed"]),
                subtasks=[
                    SubtaskOut(id=s["id"], title=s["title"], done=bool(s["done"]))
                    for s in sub_rows
                ],
            )
        )
    return result


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    body: TaskCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Connection, Depends(get_db)],
) -> TaskOut:
    now = datetime.now(timezone.utc).isoformat()
    inserted = db.execute(
        text(
            """
            INSERT INTO tasks (user_id, title, category, deadline, is_completed, created_at)
            VALUES (:uid, :title, :category, :deadline, false, :created_at)
            RETURNING id, title, category, deadline, is_completed
            """
        ),
        {
            "uid": user_id,
            "title": body.title.strip(),
            "category": body.category.strip(),
            "deadline": body.deadline,
            "created_at": now,
        },
    ).mappings().one()
    db.commit()

    return TaskOut(
        id=inserted["id"],
        title=inserted["title"],
        category=inserted["category"],
        deadline=inserted["deadline"],
        is_completed=bool(inserted["is_completed"]),
        subtasks=[],
    )


@router.patch("/{task_id}/complete", response_model=dict)
def complete_task(
    task_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
    db: Annotated[Connection, Depends(get_db)],
) -> dict:
    row = db.execute(
        text(
            """
            UPDATE tasks
            SET is_completed = true, updated_at = :now
            WHERE id = :tid AND user_id = :uid
            RETURNING id
            """
        ),
        {"tid": task_id, "uid": user_id, "now": datetime.now(timezone.utc).isoformat()},
    ).mappings().first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.commit()
    return {"message": "ok", "task_id": task_id}
