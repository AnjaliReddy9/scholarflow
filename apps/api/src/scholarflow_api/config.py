from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="ScholarFlow API", validation_alias="SCHOLARFLOW_APP_NAME")
    log_level: str = Field(default="info", validation_alias="SCHOLARFLOW_LOG_LEVEL")
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:4200"],
        validation_alias="SCHOLARFLOW_CORS_ORIGINS",
    )
    database_url: str = Field(
        default="postgresql://scholarflow:scholarflow@localhost:5432/scholarflow",
        validation_alias="SCHOLARFLOW_DATABASE_URL",
    )
    vector_store_url: str = Field(
        default="http://localhost:6333",
        validation_alias="SCHOLARFLOW_VECTOR_STORE_URL",
    )
    inference_base_url: str | None = Field(
        default=None,
        validation_alias="SCHOLARFLOW_INFERENCE_BASE_URL",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, v: object) -> list[str]:
        if isinstance(v, str):
            return [s.strip() for s in v.split(",") if s.strip()]
        if isinstance(v, list):
            return [str(x).strip() for x in v if str(x).strip()]
        return ["http://localhost:4200"]
