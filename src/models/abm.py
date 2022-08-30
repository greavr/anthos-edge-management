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
    update_time: datetime
    labels: Optional[dict]

    def __repr__(self):
        return f"""name: {self.name}, 
                location: {self.location}, 
                version: {self.version}, 
                node_count: {self.node_count}, 
                vcpu_count: {self.vcpu_count}, 
                memory_mb: {self.memory_mb}, 
                update_time: {self.update_time}, 
                labels: {self.labels}"""