from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.authenticate import verify_credentials
from app.core.config import Settings, get_settings
from app.core.roles import UserRole, allowed_panels_for_role
from app.schemas.auth import AuthStatusResponse, LoginRequest, LoginResponse

router = APIRouter()


def _session_role(request: Request) -> UserRole | None:
    raw = request.session.get("role")
    if not raw:
        return None

    try:
        return UserRole(raw)
    except ValueError:
        return None


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    request: Request,
    settings: Settings = Depends(get_settings),
) -> LoginResponse:
    verified = verify_credentials(
        credentials.username, credentials.password, settings
    )

    if verified is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    username, role = verified
    panels = allowed_panels_for_role(role)

    request.session["authenticated"] = True
    request.session["username"] = username
    request.session["role"] = role.value

    return LoginResponse(
        message="Sesión iniciada",
        username=username,
        role=role.value,
        allowed_panels=panels,
    )


@router.post("/logout")
def logout(request: Request) -> dict[str, str]:
    request.session.clear()
    return {"message": "Sesión cerrada"}


@router.get("/me", response_model=AuthStatusResponse)
def auth_status(request: Request) -> AuthStatusResponse:
    if not request.session.get("authenticated"):
        return AuthStatusResponse(authenticated=False)

    role = _session_role(request)
    if role is None:
        request.session.clear()
        return AuthStatusResponse(authenticated=False)

    return AuthStatusResponse(
        authenticated=True,
        username=request.session.get("username"),
        role=role.value,
        allowed_panels=allowed_panels_for_role(role),
    )
