from pydantic import BaseSettings
from pathlib import Path
import os

base_path = Path(__file__).parent

save_path = 'src/core/gcp/files/'

class Settings(BaseSettings):
    app_name: str = "Anthos Edge API"
    region_file: str = str((base_path / "helper/locations.csv").resolve())
    gcp_project: str = os.getenv('GCP_PROJECT')
    source_repo: str = os.environ.get('SOURCE_REPO', '')
    save_file_directory: str = os.environ.get('SAVE_PATH',save_path)
    git_token: str = os.environ.get('GIT_TOKEN','')
    copy_from_repo: str = os.environ.get('COPY_FROM_REPO','greavr/anthos-edge-workloads')

    def lookup_values(self):

        """Function to lookup git values"""
        if self.git_token == "":
            from core.gcp import gcp
            self.git_token = gcp.get_secret_value(secret_name="git_token")
        
        if self.source_repo == "":
            from core.gcp import gcp
            self.source_repo = gcp.get_secret_value(secret_name="source_repo")



app_settings = Settings()
app_settings.lookup_values()