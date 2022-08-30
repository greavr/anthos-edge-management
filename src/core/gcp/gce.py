from google.cloud import compute_v1
import logging

import core.settings as settings
settings = settings.Settings()

## Disable Instance
def stop_instance(instance_name: str, instance_zone: str) -> bool:
    """ This function toggles firewall tag on instance"""
    compute_client = compute_v1.InstancesClient()

    try:
        # Stop Instance
        current_machine = compute_client.stop(
            project = settings.gcp_project,
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
            project = settings.gcp_project,
            instance = instance_name,
            zone = instance_zone
        )
        return True
    except Exception as e:
        logging.error(e)
        print(e)

    return False
