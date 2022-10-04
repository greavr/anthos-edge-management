from google.cloud import gkehub_v1
from google.cloud import secretmanager
import cachetools.func
import logging
from datetime import datetime
from typing import List

from core.gcp import acm    
from core.settings import app_settings
from core.helper import helper
from models.abm import Abm

## List Anthos GKE Clusters
@cachetools.func.ttl_cache(maxsize=128, ttl=5)
def get_abm_list() -> List[Abm]:
    """Return list of kubernetes clusters registered in Anthos. Returns Array of cluster and instances"""

    # Result List
    abm_list = []

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
            print(response)
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
            print(f"ACM STATUS: {this_acm_status}")

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
                acm_update_time=acm_update_time
            )
            

            logging.info(thisAbm)
            abm_list.append(thisAbm)


    except Exception as e:
        logging.error(e)
        print(e)

    return abm_list

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
        print(e)

    # Next try to add secret
    try:

        # Now create the value
        parent = f"projects/{app_settings.gcp_project}/secrets/{secret_name}"
        secret_value = secret_value.encode('UTF-8')
        client.add_secret_version(parent=parent, payload={'data': secret_value})
        result = True

    except Exception as e:
        logging.error(e)
        print(e)

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
    
    except Exception as e:
        logging.error(e)
        print(e)

    # Return the decoded payload.
    return result


