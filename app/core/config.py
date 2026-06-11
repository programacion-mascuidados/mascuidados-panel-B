from functools import lru_cache

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _strip_env_string(value: object) -> object:
    if isinstance(value, str):
        return value.strip()
    return value


def _normalize_credential(value: str) -> str:
    stripped = value.strip()
    if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in "\"'":
        return stripped[1:-1]
    return stripped


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    app_name: str = "Mas Cuidados Panel API"
    app_version: str = "0.2.0"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql://user:password@localhost:5432/mascuidados"

    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    secret_key: str = "cambiar-esta-clave-en-produccion"
    admin_username: str = "admin"
    admin_password: str = "admin"
    cc_username: str = Field(
        default="",
        validation_alias=AliasChoices("CC_USERNAME", "ACCOUNTS_USERNAME"),
    )
    cc_password: str = Field(
        default="",
        validation_alias=AliasChoices("CC_PASSWORD", "ACCOUNTS_PASSWORD"),
    )
    session_max_age: int = 60 * 60 * 8  # 8 horas

    @field_validator(
        "admin_username",
        "cc_username",
        mode="before",
    )
    @classmethod
    def strip_usernames(cls, value: object) -> object:
        return _strip_env_string(value)

    @field_validator(
        "admin_password",
        "cc_password",
        mode="before",
    )
    @classmethod
    def strip_passwords(cls, value: object) -> object:
        return _strip_env_string(value)

    @field_validator("admin_password", "cc_password", mode="after")
    @classmethod
    def normalize_passwords(cls, value: str) -> str:
        return _normalize_credential(value)

    @property
    def control_cuentas_login_enabled(self) -> bool:
        return bool(self.cc_username and self.cc_password)

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
