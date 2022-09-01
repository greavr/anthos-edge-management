from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "Anthos Edge API"
    gcp_project: str = os.getenv('GCP_PROJECT')

app_settings = Settings()