from typing import Dict,List
from core.settings import app_settings
from core.gcp import git
import yaml
import os
import shutil
import logging

def create_selector(selector_name: str, match_labels: Dict[str, str]):
    """ This function creates a cluster config selector and add its to the git repo"""
    "Format for the selector can be found here: https://cloud.google.com/anthos-config-management/docs/how-to/clusterselectors#cluster-configs"

    label_set = {}

    for key, val in match_labels.items():
            label_set[key] = val

    outputFile = {
        "kind": "ClusterSelector",
        "apiVersion": "configmanagement.gke.io/v1",
        "metadata" : {
            "name" : selector_name
        },
        "spec": {
            "selector": {
                "matchLabels" : label_set
            }
        }
    }

    save_file = ""
    try:
        folder_path = f"{app_settings.save_file_directory}selectors"

        # Build folder if not present
        if not os.path.exists (folder_path):
            os.makedirs(folder_path)

        save_file = f"{folder_path}/{selector_name}.yaml"

        # Check if selector already exists
        if os.path.exists(save_file):
            return ""

        # Write file locally
        with open(save_file, 'w') as yaml_file:
            yaml.dump(outputFile, yaml_file)

        logging.debug(yaml.dump(outputFile))

    except Exception as e:
        logging.error(e)
        print(e)

    # Return path to file
    return save_file

def create_cluster(cluster_name: str, labels: Dict[str,str]):
    """ This function creates a cluster and label registry entry in git"""
    "Format for the cluster registry can be found here: https://cloud.google.com/anthos-config-management/docs/how-to/clusterselectors#cluster-configs"

    label_set = {}
    for key, val in labels.items():
        label_set[key] = val

    outputFile = {
        "kind": "Cluster",
        "apiVersion": "clusterregistry.k8s.io/v1alpha1",
        "metadata" : {
            "name" : cluster_name,
            "labels" : label_set
        }
    }

    save_file = ""
    try:
        folder_path = f"{app_settings.save_file_directory}setup"

        # Build folder if not present
        if not os.path.exists (folder_path):
            os.makedirs(folder_path)

        save_file = f"{folder_path}/{cluster_name}.yaml"

        # Write file locally
        with open(save_file, 'w') as yaml_file:
            yaml.dump(outputFile, yaml_file)


        logging.debug(yaml.dump(outputFile))
    except Exception as e:
        logging.error(e)
        print(e)

    # Return path to file
    return save_file

def create_repo_sync(cluster_name: str, selector_name: str ):
    """ This function creates repo sync config and rbac roles"""
    " More details here: https://cloud.google.com/anthos-config-management/docs/how-to/unstructured-repo#configure_an_unstructured_repository"

    outputFile = {
        "apiVersion": "configsync.gke.io/v1alpha1",
        "kind": "RepoSync",
        "metadata": {
            "name": "repo-sync",
            "annotations": {
                "configmanagement.gke.io/cluster-selector": selector_name
            }
        },
        "spec": {
            "git": {
                "repo": f"{app_settings.source_repo}.git",
                "branch": "main",
                "dir": "/{cluster_name}",
                "auth": "none"
            }
        }
    }
    
    save_file = ""
    try:
        folder_path = f"{app_settings.save_file_directory}{cluster_name}"

        # Build folder if not present
        if not os.path.exists (folder_path):
            os.makedirs(folder_path)

        save_file = f"{folder_path}/repo-sync.yaml"

        # Write file locally
        with open(save_file, 'w') as yaml_file:
            yaml.dump(outputFile, yaml_file)


        logging.debug(yaml.dump(outputFile))
    except Exception as e:
        logging.error(e)
        print(e)

    # Return path to file
    return save_file

def create_role_binding(cluster_name: str, selector_name: str):
    """ This function created RBAC for syncing"""
    " More Details Here: https://cloud.google.com/anthos-config-management/docs/how-to/unstructured-repo#configure_an_unstructured_repository"


    outputFile = {
        "kind": "RoleBinding",
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "metadata": {
            "name": "syncs-repo-crb",
            "annotations": {
                "configmanagement.gke.io/cluster-selector": selector_name
            }
        },
        "subjects": {
            "kind": "ServiceAccount",
            "name": f"ns-reconciler-{cluster_name}",
            "namespace": "config-management-system",
        },
        "roleRef": {
            "kind": "ClusterRole",
            "name": "cluster-admin",
            "apiGroup": "rbac.authorization.k8s.io"
        }
    }
    

    save_file = ""
    try:
        folder_path = f"{app_settings.save_file_directory}{cluster_name}"

        # Build folder if not present
        if not os.path.exists (folder_path):
            os.makedirs(folder_path)

        save_file = f"{folder_path}/repo-rbac.yaml"

        # Write file locally
        with open(save_file, 'w') as yaml_file:
            yaml.dump(outputFile, yaml_file)


        logging.debug(yaml.dump(outputFile))
    except Exception as e:
        logging.error(e)
        print(e)

    # Return path to file
    return save_file

def rebuild_clusters(cluster_name: str, cluster_labels: Dict[str,str], git_push: bool = True) -> list[str]:
    """ This function builder creates objects per cluster"""

    file_list=[]

    try: 
        # First create cluster object
        file_list.append(create_cluster(cluster_name=cluster_name, labels=cluster_labels))
        # Create Repo Sync File
        file_list.append(create_repo_sync(cluster_name=cluster_name,selector_name=f"{cluster_name}-sel"))
        # Create RBAC roles
        file_list.append(create_role_binding(cluster_name=cluster_name, selector_name=f"{cluster_name}-sel"))

        # Then create selectors
        ## Default selector
        file_list.append(create_selector(selector_name=f"{cluster_name}-sel", match_labels={"loc":cluster_labels["loc"]}))
        ## One for each label
        for key, value in cluster_labels.items():
            if key != "loc":
                file_list.append(create_selector(selector_name=f"{key}-{value}-sel", match_labels={key:value}))

        # Cleanup file list
        while("" in file_list):
            file_list.remove("")
        # If sync to git, sync to git
        if git_push:
            print(file_list)
            git.add_file_to_branch(file_list=file_list)
            cleanup_local_folder()
    except Exception as e:
        logging.error(e)
        print(e)
     

    return file_list

def cleanup_local_folder() -> bool:
    """ This function removes local folder"""
    result = False
    try:
        # Remove the root
        shutil.rmtree(app_settings.save_file_directory)
    except OSError as e:
        logging.error(e)
        print ("Error: %s - %s." % (e.filename, e.strerror))

    return result

