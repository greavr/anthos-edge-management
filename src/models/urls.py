from pydantic import BaseModel
from typing import List

class abm_url_list(BaseModel):
    """ABM Cluster Urls"""
    pages: List[str] = [""]
    dashboard: str = ""
    endpoint: str = ""

    def __repr__(self):
        return f"""
            pages: {self.pages},
            dashboard: {self.dashboard},
            metrics: {self.endpoint}"""
