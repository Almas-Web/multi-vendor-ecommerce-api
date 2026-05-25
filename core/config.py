from pydantic import Extra
from pydantic_settings import BaseSettings


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

    @property
    def DATABASE_URL(self) -> str:

        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"
        extra = Extra.forbid


settings = Settings()