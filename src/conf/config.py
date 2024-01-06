from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = (
        "postgresql+psycopg2://postgres:111111@localhost:5432/rest_app"
    )
    secret_key: str = "1234567890"
    algorithm: str = "HS256"
    mail_username: str = "postgres@meail.com"
    mail_password: str = "postgres"
    mail_from: str = "postgres@meail.com"
    mail_port: int = 567234
    mail_server: str = "postgres"
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str = "sadf2234f43rf3443"
    cloudinary_name: str = "cloud_name"
    cloudinary_api_key: str = "aaaaaa111111111111"
    cloudinary_api_secret: str = "secret"

    model_config = ConfigDict(
        extra="ignore", env_file=".env", env_file_encoding="utf-8"
    )  # noqa


settings = Settings()
