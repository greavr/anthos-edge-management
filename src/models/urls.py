from pydantic import BaseModel
from typing import List

class abm_url_list(BaseModel):
    """ABM Cluster Urls"""
    pos: str = ""
    dashboard: str = ""
    grafana: str = ""

    def __repr__(self):
        return f"""
            pos: {self.pos},
            dashboard: {self.dashboard},
            metrics: {self.grafana}"""
