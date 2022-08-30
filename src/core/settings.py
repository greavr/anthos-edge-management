from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Anthos Edge API"
    gcp_project: str