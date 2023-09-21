from typing import Dict, List
from pydantic import BaseSettings
from pathlib import Path
import os
import json
import logging
import random

from models.vm import vm_parameter_set, vm_image, vm_info
from models.acm import Policy

base_path = Path(__file__).parent

save_path = 'src/core/gcp/files/'

class Settings(BaseSettings):
    app_name: str = "Anthos Edge API"
    region_file: str = str((base_path / "helper/locations.csv").resolve())
    gcp_project: str = os.getenv('GCP_PROJECT')
    source_repo: str = os.environ.get('SOURCE_REPO', 'https://github.com/greavr/anthos-edge-acm')
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
    latency_graph_url: str = os.environ.get('LATENCY_GRAPH_URL','')
    workload_url = os.environ.get("POS_URL", ["https://storage.googleapis.com/anthos-edge-live-pos/pos-new/index.html","https://storage.googleapis.com/anthos-edge-live-pos/pos-old/index.html"])
    grafana_url: str = os.environ.get('GRAFANA_URL','')
    running_vm_list = []

    def lookup_values(self):
        """Function to lookup settings values from secret manager"""

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
        # END fleet URL config

    def build_running_vm_list(self):
        """ Must be run after list of VM Machines is built """
        # Build running vm_list
        gcp_regions = ["asia-east1","asia-east2","asia-northeast1","asia-northeast2","asia-northeast3","asia-south1","asia-south2","asia-southeast1","asia-southeast2","australia-southeast1","australia-southeast2","europeentral2","europe-north1","europe-southwest1","europe-west1-d","europe-west2","europe-west3","europe-west4","europe-west6","europe-west8","europe-west9","northamerica-northeast1","northamerica-northeast2","southamerica-east1","southamerica-west1","usentral1","us-east1-d","us-east4","us-east5","us-south1","us-west1","us-west2","us-west3","us-west4"]
        for i in range(random.randint(6, 12)):
            this_vm = vm_info(
                cluster_name= f"abm-{random.choice(gcp_regions)}",
                vm_name="vm-machine-"+str(random.randint(1, 100)),
                vm_ip="192.168.10.1",
                vm_status=random.choice(["Provisioning","Running","Stopped","Removing"]),
                vm_image_name=random.choice(app_settings.vm_machine_list).name,
                vm_parameter_set_name=random.choice(app_settings.vm_parameters).name,
            )
            self.running_vm_list.append(this_vm)


app_settings = Settings()
app_settings.lookup_values()