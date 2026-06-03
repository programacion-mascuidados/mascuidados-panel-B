from collections.abc import Generator

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.roles import UserRole


def get_db_session() -> Generator[Session, None, None]:
    yield from get_db()


def require_auth(request: Request) -> str:
    if not request.session.get("authenticated"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado",
        )

    return request.session.get("username", "")


def require_session_role(request: Request) -> UserRole:
    require_auth(request)

    raw = request.session.get("role")
    if not raw:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida",
        )

    try:
        return UserRole(raw)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida",
        ) from exc


def require_leads_access(request: Request) -> str:
    role = require_session_role(request)

    if role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tenés permiso para acceder a esta sección",
        )

    return request.session.get("username", "")
