from google.cloud import compute_v1
from datetime import datetime
import cachetools.func
from typing import List
import logging

from core.settings import app_settings
from models.abm_node import AbmNode

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
        print(e)

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
        print(e)

    return False

# Get Instance List
@cachetools.func.ttl_cache(maxsize=128, ttl=5)
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

@cachetools.func.ttl_cache(maxsize=128, ttl=15)
def build_instance_ip_list():
    """ This function looks up instance public ip for named instance"""
    compute_client = compute_v1.InstancesClient()
    
    # Build Zone List
    try:
        zone_client = compute_v1.ZonesClient()
        zone_results = zone_client.list(project=app_settings.gcp_project)
        zone_list = []
        for a_zone in zone_results:
            zone_list.append(a_zone.name)
        
        print(zone_list)
    except Exception as e:
        logging.error(e)

    for a_zone in zone_list:
        try:
            instance_list = compute_client.list(project=app_settings.gcp_project, zone=a_zone)
            for instance in instance_list:
                instance_ip = instance.network_interfaces[0].access_configs[0].nat_i_p
                app_settings.node_list[instance.name] = instance_ip
        except Exception as e:
            logging.info(e)

    return app_settings.node_list
