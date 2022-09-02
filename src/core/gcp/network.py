from google.cloud import compute_v1
import logging

from core.settings import app_settings

def disable_network(cluster: str, location: str) -> bool:
    """ This Function adds a firewall rule blocking all external traffic """
    result = False
    try:
        network = f"global/networks/{location}"

        firewall_rule = compute_v1.Firewall()
        firewall_rule.name = f"no-internet-{cluster}"
        firewall_rule.direction = "EGRESS"

        blocked_ports = compute_v1.Denied()
        blocked_ports.I_p_protocol = "TCP"
        blocked_ports.ports = ["1-12349"]

        firewall_rule.denied = [blocked_ports]
        firewall_rule.destination_ranges = ["0.0.0.0/0"]
        firewall_rule.network = network
        firewall_rule.description = "Block All Egress Traffic"
        firewall_rule.priority = 1001

        firewall_client = compute_v1.FirewallsClient()
        firewall_client.insert(
            project=app_settings.gcp_project, firewall_resource=firewall_rule
        )
        # Rule Added
        result = True

    except Exception as e:
        logging.error(e)
        print(e)

    return result

def enable_network(cluster: str) -> bool:
    """ This Function removes a firewall rule blocking all external traffic """
    result = False
    try:
        # Standard pattern rule creation
        firewall_rule_name = f"no-internet-{cluster}"
        firewall_client = compute_v1.FirewallsClient()

        firewall_client.delete(
            project=app_settings.gcp_project, firewall=firewall_rule_name
        )

        # Rule Removed
        result = True
    except Exception as e:
        logging.error(e)
        print(e)

    return result

