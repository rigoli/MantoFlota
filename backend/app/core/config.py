"""Configuración central (pydantic-settings)."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Variables de entorno para la aplicación."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url_async: str = Field(
        description="SQLAlchemy async URL (asyncmy)",
    )
    database_url_sync: str = Field(
        description="SQLAlchemy sync URL para Alembic (pymysql)",
    )
    test_database_url_async: str | None = Field(
        default=None,
        description="URL async para pytest",
    )

    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Orígenes CORS separados por coma",
    )
    jwt_secret_key: str = Field(
        default="cambiar-en-produccion",
        description="Secreto firmar JWT (definir en producción)",
    )
    jwt_algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(
        default=60 * 24,
        description="Duración del access token en minutos",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Lista de orígenes permitidos."""
        raw = self.cors_origins.strip()
        if not raw:
            return []
        parts: list[str] = []
        for segment in raw.split(","):
            s = segment.strip()
            if s:
                parts.append(s)
        return parts


@lru_cache
def get_settings() -> Settings:
    """Singleton de configuración."""
    return Settings()
