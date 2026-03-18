from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "Agent Trust Control Plane")
    app_env: str = os.getenv("APP_ENV", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))


settings = Settings()
