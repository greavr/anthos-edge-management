import cachetools.func
import google.cloud.logging
from typing import List

from models.logs import abm_log_item
import core.settings as settings

settings = settings.Settings()

@cachetools.func.ttl_cache(maxsize=128, ttl=5)
def GetLogs(cluster_name: str) -> List[abm_log_item]:
    """ This function returns list of logs from a specific ABM cluster"""
    client = google.cloud.logging.Client(project=settings.gcp_project)

    # List of results
    log_list = []

    # Itterate over items
    for entry in client.list_entries(filter_=f'resource.labels.cluster_name="{cluster_name}"',max_results=100):

        timestamp = entry.timestamp.isoformat()

        # Not all logs have a severity
        if entry.severity:
            severity = entry.severity
        else:
            severity = "DEFAULT"

        this_log = abm_log_item(
            severity = severity,
            timestamp = timestamp,
            data = str(entry)
        )

        log_list.append(this_log)
    
    return log_list
