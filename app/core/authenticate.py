import secrets

from app.core.config import Settings
from app.core.roles import UserRole


def verify_credentials(
    username: str,
    password: str,
    settings: Settings,
) -> tuple[str, UserRole] | None:
    if secrets.compare_digest(username, settings.admin_username) and secrets.compare_digest(
        password, settings.admin_password
    ):
        return settings.admin_username, UserRole.ADMIN

    if settings.accounts_login_enabled:
        if secrets.compare_digest(
            username, settings.accounts_username
        ) and secrets.compare_digest(password, settings.accounts_password):
            return settings.accounts_username, UserRole.ACCOUNTS

    return None
