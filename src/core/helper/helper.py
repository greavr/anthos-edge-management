from typing import Dict, List
import logging
import csv
import json
import cachetools.func
import os
import yaml
from pathlib import Path

import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging

from core.settings import app_settings
from models.vm import vm_parameter_set, vm_image
from models.acm import Policy


def Configure_Logging():
    """ Function to build logging"""
    logging.basicConfig(level=logging.INFO)
    # client = google.cloud.logging.Client()
    # handler = CloudLoggingHandler(client)
    # logging.getLogger().setLevel(logging.DEBUG)
    # setup_logging(handler)

@cachetools.func.ttl_cache(maxsize=128, ttl=60)
def lookup_location(gcp_region: str) -> Dict[str,str]:
    """ This function returns x,y co-ordinates or returns random land location if not found"""
    result = {"latitude" : "0 0 N", "longitude" : "0 0 W"}

    # Build results
    with open(app_settings.region_file) as f:
        reader = csv.DictReader(f)

        # Check if value exists
        for aItem in reader:
            if aItem["location"] == gcp_region:
                result["latitude"] = aItem["latitude"]
                result["longitude"] = aItem["longitude"]
                   
    return result


def build_vm_info():
    """ This function builds a list of avaiable VM's and Parameter Sets"""

    with open(app_settings.vm_file_file) as f:
        data = json.load(f)

        # Build VM List
        vm_list = []
        for i in data["vms"]:
            this_vm = vm_image(
                name = i["name"],
                image_path=app_settings.vm_image_bucket + "/" + i["file_name"]
            )
            vm_list.append(this_vm)

        # Add to settings
        app_settings.vm_machine_list = vm_list

        # Build Parameter List
        vm_parameter_list = []
        for i in data["parameters"]:
            this_set = vm_parameter_set(
                name = i["name"],
                vm_machine= i["vm_machine"],
                values=i["values"]
            )
            vm_parameter_list.append(this_set)

        # Add to settings
        app_settings.vm_parameters = vm_parameter_list

@cachetools.func.ttl_cache(maxsize=128, ttl=60)
def build_policy_list():
    """ Return list of ACM Policy objects"""
    results = []
    policy_folder  = (Path(__file__).parent / "policys").resolve()

    # Itterate over policy files locally
    for afile in os.scandir(policy_folder):
        # Validate if object is a file
        if afile.is_file():
            print(afile.path)

            # Read File
            with open(afile) as policy_doc:
                read_data = yaml.load(policy_doc, Loader=yaml.FullLoader)
                this_policy = Policy(
                    name=str(read_data["metadata"]["name"]),
                    version="1.0",
                    details=str(read_data["metadata"]["description"]),
                    content=str(read_data)
                )

            results.append(this_policy)


    # Results
    app_settings.acm_policy_list = results