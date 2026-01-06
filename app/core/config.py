from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import ValidationError
import sys

class Settings(BaseSettings):
    QDRANT_URL: str 
    QDRANT_COLLECTION: str
    APP_ENV: str = "development"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
try:
    settings = Settings()
except ValidationError as e:
    print("The following environment variables are missing or invalid:")
    for error in e.errors():
        missing_field = error['loc'][0] 
        print(f" - {missing_field}")
    print("\nPlease define them in your .env file and restart the application.")
    sys.exit(1)