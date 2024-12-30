import os
from pydantic_settings import BaseSettings
from typing import Optional,Dict,Any
from pydantic import EmailStr, validator

# from pydantic import Base EmailStr,validator


def get_secret(secret_name, default):
    try:
        with open('/run/secrets/{0}'.format(secret_name), 'r') as secret_file:
            return secret_file.read().strip()
    except IOError:
        return os.getenv(secret_name, default)

class ConfigClass(BaseSettings):
    SECRET_KEY: str = get_secret("SECRET_KEY", 'H5zMm7XtCKNsab88JQCLkaY4d8hExSjghGyaJDy12M')
    ALGORITHM: str = get_secret("ALGORITHM", 'HS256')

    ADMIN_KEY: str = get_secret("ADMIN_KEY", "65a613c36558")
    ADMIN_USERNAME: str = get_secret("ADMIN_USERNAME", "admin_b8b57106")
    ADMIN_PASSWORD: str = get_secret("ADMIN_PASSWORD", "86zNT34Ktux8mv2Q")

    # 60 minutes * 24 hours * 355 days = 365 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(get_secret("ACCESS_TOKEN_EXPIRE_MINUTES", 30 * 24 * 365))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(get_secret("REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 365))

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = get_secret("EMAIL_RESET_TOKEN_EXPIRE_HOURS", 8)

    # SQLALCHEMY_DATABASE_URL: str = get_secret("SQLALCHEMY_DATABASE_URL", 'postgresql://base_api_v2:Lcy96xP66EMBbrrr@dbe.comii.de:6020/sanctions_db_dev')
    SQLALCHEMY_DATABASE_URL: str = get_secret("SQLALCHEMY_DATABASE_URL", 'postgresql://postgres:2002@localhost:5432/sanctions_database')

    SQLALCHEMY_POOL_SIZE: int = 100
    SQLALCHEMY_MAX_OVERFLOW: int = 0
    SQLALCHEMY_POOL_TIMEOUT: int = 30
    SQLALCHEMY_POOL_RECYCLE: int = get_secret("SQLALCHEMY_POOL_RECYCLE", 3600)
    SQLALCHEMY_ENGINE_OPTIONS: dict = {
        "pool_pre_ping": True,
        "pool_recycle": SQLALCHEMY_POOL_RECYCLE,
    }

    # MINIO_URL: Optional[str] = get_secret("MINIO_URL", "files.comii.de")
    # MINIO_KEY: Optional[str] = get_secret("MINIO_ACCESS_KEY", "Wl0jshEzbP5+Q7KXpLpLRRqwiOPwcBEskc5s6slfyBo=")
    # MINIO_SECRET: Optional[str] = get_secret("MINIO_SECRET_KEY",
    #                                          "jDe6SMqcANAkflmmfCFyfGXN7r9AE2oKXpD0n0LRRqZfHoskT/4pOht"
    #                                          "+n1jjogmfCFyfGXD0n0N7r9AEDa0kpxfiw==")
    # MINIO_BUCKET: str = get_secret("MINIO_BUCKET", "develop")
    # MINIO_SECURE: bool = True

    PREFERRED_LANGUAGE: str = get_secret("PREFERRED_LANGUAGE", 'fr')

    API_V1_STR: str = get_secret("API_V1_STR", "/api/v1")

    PROJECT_NAME: str = get_secret("PROJECT_NAME", "BASE API")
    PROJECT_VERSION: str = get_secret("PROJECT_VERSION", "0.0.1")

    # Redis config
    REDIS_HOST: str = get_secret("REDIS_HOST", "localhost")  # redis_develop
    REDIS_PORT: int = get_secret("REDIS_PORT", 6379)
    REDIS_DB: int = get_secret("REDIS_DB", 2)
    REDIS_CHARSET: str = get_secret("REDIS_CHARSET", "UTF-8")
    REDIS_DECODE_RESPONSES: bool = get_secret("REDIS_DECODE_RESPONSES", True)

    SMTP_TLS: bool = get_secret("SMTP_TLS", True)
    SMTP_SSL: bool = get_secret("SMTP_SSL", False)
    SMTP_PORT: Optional[int] = int(get_secret("SMTP_PORT", 587))
    SMTP_HOST: Optional[str] = get_secret("SMTP_HOST", " ")
    SMTP_USER: Optional[str] = get_secret("SMTP_USER", " ")
    SMTP_PASSWORD: Optional[str] = get_secret("SMTP_PASSWORD", " ")
    EMAILS_FROM_EMAIL: Optional[EmailStr] = get_secret("EMAILS_FROM_EMAIL", "info@esm.com")
    EMAILS_FROM_NAME: Optional[str] = get_secret("EMAILS_FROM_NAME", "Ems Tool")

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = int(get_secret("EMAIL_RESET_TOKEN_EXPIRE_HOURS", 48))
    EMAILS_ENABLED: bool = get_secret("EMAILS_ENABLED", True) in ["True", True]
    EMAIL_TEMPLATES_DIR: str = "{}/app/main/templates/emails/render".format(os.getcwd())

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = get_secret("EMAIL_TEST_USER", "lawtechnology@gmail.com")
    FIRST_SUPERUSER: EmailStr = get_secret("FIRST_SUPERUSER", "admin@lawtechnology.com")
    FIRST_SUPERUSER_PASSWORD: str = get_secret("FIRST_SUPERUSER_PASSWORD", "SecurePassword123!")
    FIRST_SUPERUSER_FIRST_NAME: str = get_secret("FIRST_SUPERUSER_FIRST_NAME", "Law")
    FIRST_SUPERUSER_LASTNAME: str = get_secret("FIRST_SUPERUSER_LASTNAME", "Technology")
    USERS_OPEN_REGISTRATION: bool = get_secret("USERS_OPEN_REGISTRATION", False) in ["True", True]

    LOCAL: bool = os.getenv("LOCAL", True)

    class Config:
        case_sensitive = True


Config = ConfigClass()
