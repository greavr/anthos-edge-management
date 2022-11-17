from typing import Dict, List
from pydantic import BaseSettings
from pathlib import Path
import os
import json

from models.vm import vm_parameter_set, vm_image
from models.acm import Policy

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
    vm_image_bucket: str = os.environ.get('VM_IMAGE_BUCKET','')
    vm_machine_list: List[vm_image] = []
    vm_file_file: str = str((base_path / "helper/vms.json").resolve())
    vm_parameters: List[vm_parameter_set] = []
    acm_policy_list: List[Policy] = []
    fleet_monitoring_urls: List[str] = []
    acm_status = []
    node_list = {}
    zone_list = {}
    abm_list = {}

    def lookup_values(self):
        """Function to lookup git values"""
        if self.git_token == "":
            from core.gcp import gcp
            self.git_token = gcp.get_secret_value(secret_name="git_token")

            # COnfigure fleet URLS
            url_list = json.loads(gcp.get_secret_value(secret_name="fleet_urls"))
            if url_list:
                self.fleet_monitoring_urls = url_list
            else:
                self.fleet_monitoring_urls = []
        
        if self.source_repo == "":
            from core.gcp import gcp
            self.source_repo = gcp.get_secret_value(secret_name="source_repo")

app_settings = Settings()
app_settings.lookup_values()