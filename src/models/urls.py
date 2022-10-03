from pydantic import BaseModel
from typing import List

class abm_url_list(BaseModel):
    """ABM Cluster Urls"""
    store_pages: List[str]
    monitoring_dashboard: str
    metrics_endpoint: str

class fleet_url_list(BaseModel):
    """ Monitoring URLS """
    in_store_iot: str
    fleet_hardware: str
    store_wait: str
    graph_list: List[str]
