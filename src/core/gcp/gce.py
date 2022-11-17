from google.cloud import compute_v1
from datetime import datetime
import cachetools.func
from typing import List
import logging
import threading

from core.settings import app_settings
from models.abm_node import AbmNode

from core.gcp import gcp

## Disable Instance
def stop_instance(instance_name: str, instance_zone: str) -> bool:
    """ This function toggles firewall tag on instance"""
    compute_client = compute_v1.InstancesClient()

    try:
        # Stop Instance
        current_machine = compute_client.stop(
            project = app_settings.gcp_project,
            instance = instance_name,
            zone = instance_zone
        )
        return True
    except Exception as e:
        logging.error(e)
        logging.error(e)

    return False

## Enable Instance
def start_instance(instance_name: str, instance_zone: str) -> bool:
    """ This function toggles firewall tag on instance"""
    compute_client = compute_v1.InstancesClient()

    try:
        # Stop Instance
        current_machine = compute_client.start(
            project = app_settings.gcp_project,
            instance = instance_name,
            zone = instance_zone
        )
        return True
    except Exception as e:
        logging.error(e)
        logging.error(e)

    return False

# Get Instance List
@cachetools.func.ttl_cache(maxsize=1024, ttl=60)
def get_instance_list(location: str, cluster_name: str = "") -> List[AbmNode]:
    """ Function returns a filtered list of instance per-cluster """
    compute_client = compute_v1.InstancesClient()

    request = {
        "project" : app_settings.gcp_project,
    }

    agg_list = compute_client.aggregated_list(request=request)

    all_instances = []
    ## TODO: OPTIMIZE THIS MESS
    for zone, response in agg_list:
        if response.instances:
            if location in zone:
                for instance in response.instances:
                    if "workstation" not in instance.name:
                        aNode = AbmNode(
                            name = instance.name,
                            zone = zone.rsplit('/', 1)[-1],
                            ip = instance.network_interfaces[0].network_i_p,
                            instance_type = instance.machine_type.rsplit('/', 1)[-1],
                            disk_size_gb = instance.disks[0].disk_size_gb,
                            update_time = datetime.now(),
                            status = instance.status
                        )

                        all_instances.append(aNode)

    return all_instances

def build_instance_ip_list():
    """ This function looks up instance public ip for named instance"""
    compute_client = compute_v1.InstancesClient()
    logging.debug("Building Instance list")

    # Build Instance List
    for a_zone in app_settings.zone_list:
        try:
            instance_list = compute_client.list(project=app_settings.gcp_project, zone=a_zone)
            for instance in instance_list:
                instance_ip = instance.network_interfaces[0].access_configs[0].nat_i_p
                app_settings.node_list[instance.name] = instance_ip
        except Exception as e:
            logging.info(e)

@cachetools.func.ttl_cache(maxsize=1024, ttl=60)
def return_instance_ip_list():
    """" This function returns list of GCE instances"""

    # If first time
    if not app_settings.node_list:
        logging.debug("First time building instance list")
        build_instance_ip_list()
    else:
        logging.debug("Building instance list as Background Thread")
        x = threading.Thread( target=build_instance_ip_list, args=())
        x.start

    return app_settings.node_list