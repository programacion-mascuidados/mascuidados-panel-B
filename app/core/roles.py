from enum import StrEnum

PANEL_AUTOMATION_1 = "automation-1"
PANEL_AUTOMATION_2 = "automation-2"


class UserRole(StrEnum):
    ADMIN = "admin"
    ACCOUNTS = "accounts"


def allowed_panels_for_role(role: UserRole) -> list[str]:
    if role == UserRole.ADMIN:
        return [PANEL_AUTOMATION_1, PANEL_AUTOMATION_2]
    return [PANEL_AUTOMATION_1]
