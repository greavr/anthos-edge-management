from datetime import datetime
from pydantic import BaseModel
from typing import List

class abm_log_item(BaseModel):
    """Log Format"""
    severity: str
    timestamp: datetime
    data: str

    def __repr__(self):
        return f"""
            severity: {self.severity},
            timestamp: {self.timestamp},
            data: {self.data}"""