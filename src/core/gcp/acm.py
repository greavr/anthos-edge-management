from typing import List
from datetime import datetime
import logging
import cachetools.func

from google.cloud import gkehub_v1

from core.settings import app_settings
from models import abm
from models.abm import Abm
from core.gcp import file_manager, gcp

@cachetools.func.ttl_cache(maxsize=128, ttl=5)
def get_source_repo() -> List[str]:
    """ This Function Returns the URL of the source repo in the project """
    return app_settings.source_repo

@cachetools.func.ttl_cache(maxsize=128, ttl=10)
def call_acm():
    """" This function calls up Google Cloud to get list of ACM clusters"""

    try:
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
            elif status_code == 2:
                status = "ERROR"
            elif status_code == 3:
                status = "APPLY ERROR"
            elif status_code == 1:
                status = "SYNCED"
            else:
                status = str(status_code)

            if data.configmanagement.config_sync_state.sync_state.last_sync:
                last_update = datetime.strptime(data.configmanagement.config_sync_state.sync_state.last_sync, '%Y-%m-%d %H:%M:%S %z %Z')
            else:
                last_update = ""

            # Save results to set
            this_server = {"cluster": cluster_name, "status": status, "last_update": last_update}
            app_settings.acm_status.append(this_server)


    except Exception as e:
        logging.error(e)
        print(e)

@cachetools.func.ttl_cache(maxsize=128, ttl=1)
def acm_status(which_cluser_name: str) -> List[str]:
    """ This function returns a list of clusters, with current ACM status """
    cluster_list = ["NOT_INSTALLED",""]

    # Itterate through values
    for aCluster in app_settings.acm_status:
        if aCluster["cluster"] == which_cluser_name:
            # Matching cluster
            cluster_list = [aCluster["status"],aCluster["last_update"]]

    
    return cluster_list

def build_repo() -> bool:
    """ This function creates a set of cluster registrys for entrys found in the ACM list"""

    result = False
    #try:
    abm_list = gcp.get_abm_list()

    # For each cluster create cluster registry file
    this_cluster_file = file_manager.rebuild_clusters(cluster_list=abm_list)
    logging.debug(this_cluster_file)
    print(this_cluster_file)
    
    # Done Adding files
    result = True
    # except Exception as e:
    #     logging.error(e)
    #     print(e)

    return result

