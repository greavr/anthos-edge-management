from typing import Dict,List
from core.settings import app_settings
from core.gcp import git
from models.abm import Abm

import yaml
import os
import shutil
import logging

def create_selector(selector_name: str, match_labels: Dict[str, str]):
    """ This function creates a cluster config selector and add its to the git repo"""
    "Format for the selector can be found here: https://cloud.google.com/anthos-config-management/docs/how-to/clusterselectors#cluster-configs"

    # Dont creator selector for mesh_id
    if "mesh_id" in selector_name:
        return ""

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
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        save_file = f"{folder_path}/{selector_name}.yaml"

        # Check if selector already exists
        if os.path.exists(save_file):
            logging.debug(f"Existing file found: {save_file}")
            return save_file

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
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        save_file = f"{folder_path}/{cluster_name}.yaml"

        # Check if cluster already exists
        if os.path.exists(save_file):
            logging.debug(f"Existing file found: {save_file}")
            return save_file

        # Write file locally
        with open(save_file, 'w') as yaml_file:
            yaml.dump(outputFile, yaml_file)


        logging.debug(yaml.dump(outputFile))
    except Exception as e:
        logging.error(e)
        print(e)

    # Return path to file
    return save_file

def create_repo_file(file_name: str, file_contents: str, basefolder: str = "default") -> str:
    """ This function creates local file"""

    save_file = ""

    try:
        save_file = f"{app_settings.save_file_directory}{basefolder}/{file_name}"
        # Check if selector already exists
        if os.path.exists(save_file):
            logging.debug(f"Existing file found: {save_file}")
            return ""

        folder_path = os.path.dirname(save_file)

        # Check if file already exists
        if os.path.exists(save_file):
            logging.debug(f"Existing file found: {save_file}")
            return save_file

        # Build folder if not present
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        # Write file locally
        out_file = open(save_file, 'w')
        out_file.write(file_contents)
        out_file.close()

    except Exception as e:
        logging.error(e)
        print(e)

    return save_file    

def rebuild_clusters(cluster_list: List[Abm]) -> List[str]:
    """ This function builder creates objects per cluster"""

    # Source File list
    file_list=[]
    # Return list
    git_added_files = []

    try: 
        # Create Default apps
        git_file_to_create = git.get_file_contents()
        for key,value in git_file_to_create.items():
            file_list.append(create_repo_file(file_name=key, file_contents=value))

        # Add cluster specific features
        for aCluster in cluster_list:

            # Cluster Object
            file_list.append(create_cluster(cluster_name=aCluster.name, labels=aCluster.labels))

            # location selector
            file_list.append(create_selector(selector_name=f"{aCluster.name}-sel", match_labels={"loc":aCluster.labels["loc"]}))
            
            # per-label selector
            for key, value in aCluster.labels.items():
                if key != "loc":
                    file_list.append(create_selector(selector_name=f"{key}-{value}-sel", match_labels={key:value}))

            # Cleanup file list
            while("" in file_list):
                file_list.remove("")
        
        # Finally sync to git
        git_added_files = git.add_file_to_branch(file_list=file_list)
        cleanup_local_folder()

    except Exception as e:
        logging.error(e)
        print(e)
     

    return git_added_files

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

def create_data_volume(image_path: str, selector: str, disk_size: str = "10G") -> str:
    """ Create DataVolume file contents """

    outputFile = {
        "apiVersion": "vm.cluster.gke.io/v1",
        "kind": "VirtualMachineDisk",
        "metadata": {
            "annotations": {
                "configmanagement.gke.io/cluster-selector": selector
                },
            "name": "vm-disk"
        },
        "spec": {
            "size": disk_size ,
            "storageClassName": "local-disks",
            "source": {
                "https": {
                    "url": image_path
                }
            }
        }
    }

    return outputFile

def create_vm(vm_name: str, selector: str, parameters:str = "") -> str:
    """ This function returns vm yaml"""

    # Establish OS type
    if "windows" in vm_name.lower():
        os_type = "Windows"
    else:
        os_type = "linux"

    outputfile = {
        "apiVersion": "vm.cluster.gke.io/v1",
        "kind": "VirtualMachine",
        "metadata": {
            "annotations": {
                "configmanagement.gke.io/cluster-selector": selector
                },
            "name": vm_name,
        },
        "spec": {
            "osType": os_type,
            "compute": {
                "cpu": {
                    "vcpus": "2"
                    },
                "memory": {
                    "capacity": "2GiB"
                    }
                },
            "disks": [{
                "boot": "true",
                "virtualMachineDiskName": "vm-disk"
        }]
        }
    }

    return outputfile

def creat_vm_file(vm_name: str, target_cluster: str, parameter_set: str = "") -> bool:
    """ This function creates VM Manifest file and adds to repo"""
    vm_image_path = vm_name
    vm_parameters = parameter_set

    result = False

    try:
        # Create Deployment variables
        vm_file_name = f"{target_cluster}-{vm_name}".lower().replace("_", "-") #Cleaner file name

        # Get vm image name
        for a_vm in app_settings.vm_machine_list:
            if vm_name == a_vm.name:
                vm_image_path = a_vm.image_path

        # Get Parameter set
        for a_parameter_set in app_settings.vm_parameters:
            if parameter_set == a_parameter_set.name:
                vm_parameters = a_parameter_set.values

        # Selector
        vm_selector = f"{target_cluster}-sel"

        # Create YAML
        data_volume = yaml.dump(create_data_volume(image_path=vm_image_path,selector=vm_selector))
        vm_file = yaml.dump(create_vm(vm_name=vm_name,selector=vm_selector,parameters=vm_parameters))
        combined_file = data_volume + "\n---\n" + vm_file
        print(combined_file)

        add_to_git_file = [create_repo_file(file_name=f"{vm_file_name}.yaml",file_contents=combined_file, basefolder="vms")]
        git_added_files = git.add_file_to_branch(file_list=add_to_git_file)
        print(git_added_files)
        cleanup_local_folder()

        # Return result
        result = True
    except Exception as e:
        logging.error(e)
        print(e)

    return result
