import cachetools.func
import google.cloud.logging
from typing import List

from models.logs import abm_log_item

from core.settings import app_settings

@cachetools.func.ttl_cache(maxsize=128, ttl=5)
def GetLogs(cluster_name: str, row_count: int = 100) -> List[abm_log_item]:
    """ This function returns list of logs from a specific ABM cluster"""
    client = google.cloud.logging.Client(project=app_settings.gcp_project)

    # List of results
    log_list = []

    # Itterate over items
    for entry in client.list_entries(filter_=f'resource.labels.cluster_name="{cluster_name}"',max_results=row_count):

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
