from typing import List
from datetime import datetime
import logging
import cachetools.func

from google.cloud import gkehub_v1

from core.settings import app_settings
from models.abm import Abm
from core.gcp import gcp

@cachetools.func.ttl_cache(maxsize=128, ttl=5)
def get_source_repo() -> List[str]:
    """ This Function Returns the URL of the source repo in the project """
    return app_settings.source_repo

@cachetools.func.ttl_cache(maxsize=128, ttl=1)
def acm_status(cluser_name: str = "*") -> List[Abm]:
    """ This function returns a list of clusters, with current ACM status """
    cluster_list = []

    try:

        # Get ABM list
        cluster_list = gcp.get_abm_list()

        # No Nodes Found
        if not cluster_list:
            return cluster_list

        # Create a client
        client = gkehub_v1.GkeHubClient()

        # Initialize request argument(s)
        request = gkehub_v1.GetFeatureRequest(
            name=f"projects/{app_settings.gcp_project}/locations/global/features/configmanagement",
        )

        # Make the request
        page_result = client.get_feature(request=request)

        # Handle the response
        for key in page_result.membership_states:
            cluster_name = key.split("/")[-1]
            data = page_result.membership_states[key]

            status_code = data.configmanagement.config_sync_state.sync_state.code

            # TODO: Fix this mapping, hate that its manual
            ## https://cloud.google.com/python/docs/reference/gkehub/latest/google.cloud.gkehub_v1.types.FeatureState
            if status_code == 5:
                status = "NOT_INSTALLED"
            elif status_code == 1:
                status = "SYNCED"
            else:
                status = str(status_code)

            if data.configmanagement.config_sync_state.sync_state.last_sync:
                last_update = datetime.strptime(data.configmanagement.config_sync_state.sync_state.last_sync, '%Y-%m-%d %H:%M:%S %z %Z')
            else:
                last_update = ""
            
            # Append Value to cluster list
            for aCluster in cluster_list:
                if aCluster.name == cluster_name:
                    aCluster.acm_status = status
                    # Validate Last Sync was
                    if last_update:
                        aCluster.acm_update_time = last_update

    except Exception as e:
        logging.error(e)
        print(e)

    return cluster_list