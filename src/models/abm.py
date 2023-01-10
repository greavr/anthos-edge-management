from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class Abm(BaseModel):
    """Anthos Baremetal Cluster Model"""
    name: str
    location: str
    version: str
    node_count: int
    vcpu_count: int
    memory_mb: int
    cluster_state: str
    update_time: datetime
    lat_long: dict
    labels: Optional[dict]
    acm_status: Optional[str]
    acm_update_time: Optional[datetime]
    sync_latency_setting: Optional[int]

    def __repr__(self):
        return f"""name: {self.name}, 
                location: {self.location}, 
                version: {self.version}, 
                node_count: {self.node_count}, 
                vcpu_count: {self.vcpu_count}, 
                memory_mb: {self.memory_mb}, 
                cluster_state: {self.cluster_state},
                update_time: {self.update_time}, 
                lat_long: {self.lat_long},
                labels: {self.labels},
                acm_status: {self.acm_status},
                acm_update_time: {self.acm_update_time},
                sync_latency_setting: {self.sync_latency_setting}"""