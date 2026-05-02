from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    # Database configuration
    DATABASE_URL: str = (
        "postgresql://ecommerce_user:ecommerce_password@localhost:5432/ecommerce_db"
    )

    # Security configurations
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Strip configuration
    STRIPE_API_KEY: str = "sk_test_your_stripe_test_key_here"
    STRIPE_WEBHOOK_SECRET: str = "whsec_your_webhook_secret_here"

    # Environment
    ENVIRONMENT: str = "developement"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    # returns the same instance againa and again
    return Settings()
