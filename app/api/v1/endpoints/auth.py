import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.core.config import Settings, get_settings
from app.schemas.auth import AuthStatusResponse, LoginRequest, LoginResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    request: Request,
    settings: Settings = Depends(get_settings),
) -> LoginResponse:
    username_ok = secrets.compare_digest(
        credentials.username, settings.admin_username
    )
    password_ok = secrets.compare_digest(
        credentials.password, settings.admin_password
    )

    if not (username_ok and password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
        )

    request.session["authenticated"] = True
    request.session["username"] = settings.admin_username

    return LoginResponse(message="Sesión iniciada", username=settings.admin_username)


@router.post("/logout")
def logout(request: Request) -> dict[str, str]:
    request.session.clear()
    return {"message": "Sesión cerrada"}


@router.get("/me", response_model=AuthStatusResponse)
def auth_status(request: Request) -> AuthStatusResponse:
    if request.session.get("authenticated"):
        return AuthStatusResponse(
            authenticated=True,
            username=request.session.get("username"),
        )

    return AuthStatusResponse(authenticated=False)
