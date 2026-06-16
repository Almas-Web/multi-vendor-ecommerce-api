from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    PROJECT_NAME: str = "Multi Vendor Ecommerce API"
    PROJECT_VERSION: str = "1.0.0"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"

    POSTGRES_DB: str = "multi_vendor_ecommerce_db"

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 300

    JWT_ALGORITHM: str = "HS256"

    # =========================
    # EMAIL SETTINGS (IMPORTANT)
    # =========================
    EMAIL_HOST: str = "smtp.gmail.com"
    EMAIL_PORT: int = 587
    EMAIL_USERNAME: str | None = None
    EMAIL_PASSWORD: str | None = None
    EMAIL_FROM: str | None = None
    EMAIL_PROVIDER: str = "gmail"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_SERVER}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ✅ Pydantic v2 config
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="forbid"
    )


settings = Settings()