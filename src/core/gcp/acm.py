from typing import List
from datetime import datetime
import logging
import cachetools.func
import yaml

from google.cloud import gkehub_v1

from core.settings import app_settings
from core.gcp import file_manager, gcp, gcp, git, file_manager

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
                last_update = str(data.configmanagement.config_sync_state.sync_state.last_sync)
            else:
                last_update = ""

            # Save results to set
            this_server = {"cluster": cluster_name, "status": status, "last_update": last_update}
            app_settings.acm_status.append(this_server)


    except Exception as e:
        logging.error(e)

@cachetools.func.ttl_cache(maxsize=128, ttl=1)
def acm_status(which_cluser_name: str) -> List[str]:
    """ This function returns a list of clusters, with current ACM status """
    cluster_list = ["NOT_INSTALLED",""]

    call_acm()

    # Itterate through values
    for aCluster in app_settings.acm_status:
        if aCluster["cluster"] == which_cluser_name:
            # Matching cluster
            cluster_list = [aCluster["status"],aCluster["last_update"]]

    return cluster_list

def build_repo() -> bool:
    """ This function creates a set of cluster registrys for entrys found in the ACM list"""

    result = False
    try:
        abm_list = gcp.get_abm_list()

        # For each cluster create cluster registry file
        this_cluster_file = file_manager.rebuild_clusters(cluster_list=abm_list)
        logging.info(f"Creating file: {this_cluster_file}")
        
        # Done Adding files
        result = True
    except Exception as e:
        logging.error(e)

    return result

def update_application(labels: dict, app_name: str) -> bool:
    """ This function updates post application to targeted clusters"""

    # First get cluster list
    abm_list = gcp.get_abm_list()

    #Build list of applicable clusters
    selected_clusters = []
    unselected_clusters = []
    
    # Check for matching labels in list
    for label in labels:
        label_values = labels[label]
        for value in label_values:
             for cluster in abm_list: # For each cluster
                curr_cluster_labels = cluster.labels # Look at the cluster labels
                if(curr_cluster_labels[label] == value):  
                    if(cluster not in selected_clusters): # Add the cluster name if it has the desired label:value 
                        selected_clusters.append(cluster.name) # Remove duplicates
    
    # Build unselected clusters
    for cluster in abm_list:
        if(cluster.name not in selected_clusters):
            unselected_clusters.append(cluster.name)

    v2_file = "pos/pos_v2.yaml"
    v1_file = "pos/pos_v1.yaml"
    file_list = []
    # Update app_yaml
    if app_name == "pos_v2":
        # Add tagged instances to pos_v2 and untagged to pos_v1
        selected_yaml = yaml.safe_load(git.get_contents(file_path="default/" + v2_file))
        selected_yaml['metadata']['annotations']['configsync.gke.io/cluster-name-selector'] = ",".join(selected_clusters)
        # Remove old selector if there:
        if 'configmanagement.gke.io/cluster-selector' in selected_yaml['metadata']['annotations']:
            del selected_yaml['metadata']['annotations']['configmanagement.gke.io/cluster-selector']
        file_list.append(file_manager.create_repo_file(file_name=v2_file,file_contents=yaml.dump(selected_yaml), basefolder="default"))

        # Updated pos_v1
        unselected_yaml = yaml.safe_load(git.get_contents(file_path="default/" + v1_file))
        unselected_yaml['metadata']['annotations']['configsync.gke.io/cluster-name-selector'] = ",".join(unselected_clusters)
        file_list.append(file_manager.create_repo_file(file_name=v1_file,file_contents=yaml.dump(unselected_yaml), basefolder="default"))
    else:
        # Add tagged instances to pos_v1 and untagged to pos_v2
        selected_yaml = yaml.safe_load(git.get_contents(file_path="default/" + v1_file))
        selected_yaml['metadata']['annotations']['configsync.gke.io/cluster-name-selector'] = ",".join(selected_clusters)
        # Remove old selector if there:
        if "configmanagement.gke.io/cluster-selector" in selected_yaml['metadata']['annotations']:
            del selected_yaml['metadata']['annotations']['configmanagement.gke.io/cluster-selector']
        file_list.append(file_manager.create_repo_file(file_name=v1_file,file_contents=yaml.dump(selected_yaml), basefolder="default"))

        # Updated pos_v2
        unselected_yaml = yaml.safe_load(git.get_contents(file_path="default/" + v2_file))
        # Check not null
        if unselected_clusters:
            unselected_yaml['metadata']['annotations']['configsync.gke.io/cluster-name-selector'] = ",".join(unselected_clusters)
        else:
            unselected_yaml['metadata']['annotations']['configmanagement.gke.io/cluster-selector'] = "blank-sel"
            # Remove no longer needed value
            if 'configsync.gke.io/cluster-name-selector' in unselected_yaml['metadata']['annotations']:
                del unselected_yaml['metadata']['annotations']['configsync.gke.io/cluster-name-selector']
        file_list.append(file_manager.create_repo_file(file_name=v2_file,file_contents=yaml.dump(unselected_yaml), basefolder="default"))

    # Push Files to Git
    git_added_files = git.add_file_to_branch(file_list=file_list)
    file_manager.cleanup_local_folder()       
        

    logging.debug(f"Selected clusters: {selected_clusters}")
    logging.debug(f"Un-Selected clusters: {unselected_clusters}")