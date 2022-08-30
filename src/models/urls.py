from pydantic import BaseModel
from typing import List

class abm_url_list(BaseModel):
    """ABM Cluster Urls"""
    store_pages: List[str]
    monitoring_dashboar: str