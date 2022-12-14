from google.cloud import gkehub_v1
from google.cloud import secretmanager
from google.cloud import compute_v1
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import cachetools.func
import logging
from datetime import datetime
from typing import List
import threading
import logging

from core.gcp import acm    
from core.settings import app_settings
from core.helper import helper
from models.abm import Abm

## List Anthos GKE Clusters
@cachetools.func.ttl_cache(maxsize=128, ttl=15)
def get_abm_list() -> List[Abm]:
    """Return list of kubernetes clusters registered in Anthos. Returns Array of cluster and instances"""

    if app_settings.abm_list:
        logging.info("Using cache")
        x = threading.Thread(target=build_abm_list, args=())
        x.start()
    else:
        build_abm_list()

    # Return values
    return app_settings.abm_list

def build_abm_list():
    """ This creates a fresh list of ABM instances"""

    logging.info("Rebuilding list")

    # Result List
    abm_list = []
    # Update ACM Status
    acm.call_acm()

    # Build Client
    try:
         # Create a client
        client = gkehub_v1.GkeHubClient()

        # Initialize request argument(s)
        request = gkehub_v1.ListMembershipsRequest(
            parent=f"projects/{app_settings.gcp_project}/locations/-",
        )

        # Make the request
        page_result = client.list_memberships(request=request)

        # Handle the response
        for response in page_result:
            # Get Location from label
            try:
                this_location = response.labels["loc"]
            except:
                this_location = response.name.split("/")[-3]

            # Generate Friendly Name
            cluster_name = response.name.split("/")[-1]

            # Lookup Status
            this_acm_status = acm.acm_status(which_cluser_name=cluster_name)
            acm_status_code = this_acm_status[0]
            acm_update_time = this_acm_status[1]
            # Validate date / time
            if acm_update_time == "":
                acm_update_time = datetime.now()
            logging.info(f"ACM STATUS: {this_acm_status}")

            # Create new class
            thisAbm = Abm(
                name = cluster_name,
                location = this_location,
                version = response.endpoint.kubernetes_metadata.kubernetes_api_server_version,
                node_count = response.endpoint.kubernetes_metadata.node_count,
                vcpu_count = response.endpoint.kubernetes_metadata.vcpu_count,
                memory_mb = response.endpoint.kubernetes_metadata.memory_mb,
                cluster_state = str(response.state.code).split(".")[-1],
                update_time = response.endpoint.kubernetes_metadata.update_time,
                lat_long = helper.lookup_location(gcp_region=this_location),
                labels = response.labels,
                acm_status=acm_status_code,
                acm_update_time=acm_update_time,
                sync_latency_setting=0
            )

            abm_list.append(thisAbm)
            app_settings.abm_list = abm_list

            logging.info("List Build Complete")

    except Exception as e:
        logging.error(e)

def set_secret_value(secret_name: str, secret_value: str) -> bool:
    """ This function updates the secret in the vault and updates the app_settings"""

    result = False

    # Try to create the secret
    try:
        # Now update the secret
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the parent project.
        parent = f"projects/{app_settings.gcp_project}"

        # Build a dict of settings for the secret
        secret = {'replication': {'automatic': {}}}
        # Create the secret
        client.create_secret(secret_id=secret_name, parent=parent, secret=secret)
    except Exception as e:
        logging.error(e)
        logging.error(e)

    # Next try to add secret
    try:
        # Now create the value
        parent = f"projects/{app_settings.gcp_project}/secrets/{secret_name}"
        secret_value = secret_value.encode('UTF-8')
        client.add_secret_version(parent=parent, payload={'data': secret_value})
        result = True

    except Exception as e:
        logging.error(e)
        logging.error(e)

    # Return the decoded payload.
    return result

@cachetools.func.ttl_cache(maxsize=128, ttl=5)
def get_secret_value(secret_name: str) -> str:
    """ This function looksup the secret in secret manager (if exists)""" 

    result = ""
    try:
        client = secretmanager.SecretManagerServiceClient()

        # Build the resource name of the secret version.
        name = f"projects/{app_settings.gcp_project}/secrets/{secret_name}/versions/latest"

        # Access the secret version.
        response = client.access_secret_version(name=name)
        result = response.payload.data.decode('UTF-8')
        logging.info(result)
    
    except Exception as e:
        logging.error(e)

    # Return the decoded payload.
    return result

def get_zones():
    """ This function builds a list of Google Cloud Zones"""

    # If popuplate already return current value
    if app_settings.zone_list:
        logging.info("Using existing zone list")
        return app_settings.zone_list

    # Build list
    try:
        logging.debug("Building Zone List")
        zone_client = compute_v1.ZonesClient()
        zone_results = zone_client.list(project=app_settings.gcp_project)
        zone_list = []
        for a_zone in zone_results:
            zone_list.append(a_zone.name)
        
        app_settings.zone_list =zone_list
    except Exception as e:
        logging.error(e)
    
    # Return happy list
    return app_settings.zone_list

def set_firestore_value(value_name: str, value_to_save: dict, collection_name: str) -> bool:
    """ This function saves values in datastore""" 
    try: 
        db = firestore.client()
        logging.debug(f"Writing values to firestore in the project: {app_settings.gcp_project}")

        # Save values
        logging.debug(f"Saving the value: {value_to_save} to in {value_name}")
        doc_ref = db.collection(collection_name).document(value_name)

        # Update value
        doc_ref.set(value_to_save)
        return True
    except Exception as e:
        logging.exception(f"Unable to save to firestore. Value name: {value_name}, Value: {value_to_save}")
        logging.exception(e)
        return False

@cachetools.func.ttl_cache(maxsize=128, ttl=5)
def get_firestore_value(value_name: str, collection_name: str) -> dict:
    """ this function looksup firestore value"""
    db = firestore.client()
    logging.debug(f"Looking up values to firestore in the project: {app_settings.gcp_project}")
    
    # get values
    logging.debug(f"Get the value for: {value_name}")
    doc_ref = db.collection(collection_name).document(value_name)
    doc = doc_ref.get().to_dict()

    logging.debug(f"Found values: {doc}")
    return(doc)


