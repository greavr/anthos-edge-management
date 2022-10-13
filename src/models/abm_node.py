from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class AbmNode(BaseModel):
    """Anthos Baremetal Node Model"""
    name: str
    zone: str
    ip: str
    instance_type: str
    disk_size_gb: int
    status: str = ""
    update_time: datetime

    def __repr__(self):
        return f"""name: {self.name}, 
                zone: {self.zone}, 
                ip: {self.ip}, 
                instance_type: {self.instance_type},
                status: {self.status},
                disk_size_gb: {self.disk_size_gb}, 
                update_time: {self.update_time}"""