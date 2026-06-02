from collections.abc import Generator

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def require_auth(request: Request) -> str:
    if not request.session.get("authenticated"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
        )

    return request.session.get("username", "")
