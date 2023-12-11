import secrets
from os import getenv
from pathlib import Path

from pydantic import BaseSettings

PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent


def get_dotenv_paths() -> list[Path]:
    dotenv_path = PACKAGE_ROOT / "dotenvs"
    env = getenv("DEPLOYMENT_ENVIRONMENT", "local")
    return [dotenv_path / f".env.{env}", dotenv_path / ".env"]


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 3
    SECRET_KEY: str = secrets.token_urlsafe(32)

    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_DB_NAME: str
    TEST_DATABASE_URL: str

    class Config:
        env_file = get_dotenv_paths()
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
