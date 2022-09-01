from google.cloud import gkehub_v1
import cachetools.func
import logging
from typing import List

from core.settings import app_settings
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
            try:
                this_location = response.labels["loc"]
            except:
                this_location = response.name.split("/")[-3]


            # Create new class
            thisAbm = Abm(
                name = response.name.split("/")[-1],
                location = this_location,
                version = response.endpoint.kubernetes_metadata.kubernetes_api_server_version,
                node_count = response.endpoint.kubernetes_metadata.node_count,
                vcpu_count = response.endpoint.kubernetes_metadata.vcpu_count,
                memory_mb = response.endpoint.kubernetes_metadata.memory_mb,
                update_time = response.endpoint.kubernetes_metadata.update_time,
                labels = response.labels
            )

            
            logging.info(thisAbm)
            abm_list.append(thisAbm)


    except Exception as e:
        logging.error(e)
        print(e)

    return abm_list