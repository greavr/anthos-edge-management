from typing import Dict, List
from pydantic import BaseSettings
from pathlib import Path
import os
import json
import logging

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
    grafana_url: str = os.environ.get('GRAFANA_URL','')
    vm_machine_list: List[vm_image] = []
    vm_file_file: str = str((base_path / "helper/vms.json").resolve())
    vm_parameters: List[vm_parameter_set] = []
    acm_policy_list: List[Policy] = []
    fleet_monitoring_urls: List[str] = []
    acm_status = []
    node_list = {}
    zone_list = {}
    abm_list = {}
    latency_graph_url: str = os.environ.get('LATENCY_GRAPH_URL','')
    syncronicity_looker_url: str = os.environ.get('SYNC_LOOKER_URL','')

    def lookup_values(self):
        """Function to lookup settings values from secret manager"""
        if self.git_token == "":
            # Check for secret value
            try:
                from core.gcp import gcp
                self.git_token = gcp.get_secret_value(secret_name="git_token")
            except Exception as e:
                logging.error(e)


        # Configure fleet URLS
        if self.grafana_url:
            # Env Var set, pre-populate
            self.fleet_monitoring_urls = [
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=6",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=2",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=4",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=8",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=10",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=16",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=18",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=20",
                f"{self.grafana_url}/d-solo/c7hM3KSVz/fleet-metrics?orgId=1&panelId=22"
            ]
        else:
            # Lookup values from secret manager
            try:
                from core.gcp import gcp
                url_list = json.loads(gcp.get_secret_value(secret_name="fleet_urls"))
            except Exception as e:
                logging.error(e)

            # Process what we got
            if url_list:
                self.fleet_monitoring_urls = url_list
            else:
                self.fleet_monitoring_urls = []
        # END fleet URL config
        
        if self.source_repo == "":
            try:
                from core.gcp import gcp
                self.source_repo = gcp.get_secret_value(secret_name="source_repo")
            except Exception as e:
                logging.error(e)

        if self.latency_graph_url == "":
            try:
                from core.gcp import gcp
                self.latency_graph_url = gcp.get_secret_value(secret_name="latency_graph_url")
            except Exception as e:
                logging.error(e)

        if self.syncronicity_looker_url == "":
            try:
                from core.gcp import gcp
                self.syncronicity_looker_url = gcp.get_secret_value(secret_name="syncronicity_looker_url")
            except Exception as e:
                logging.error(e)

app_settings = Settings()
app_settings.lookup_values()