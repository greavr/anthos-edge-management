from pydantic import BaseModel
from typing import List, Optional

class Policy(BaseModel):
    """Anthos Baremetal Cluster Model"""
    name: str
    version: str
    details: str
    content: dict

    def __repr__(self):
        return f"""name: {self.name},
                version: {self.version}, 
                details: {self.details}, 
                content: {self.content}"""