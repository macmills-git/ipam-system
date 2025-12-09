from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: int
    user_id: Optional[int]
    action: str
    target_type: str
    target_id: Optional[int]
    before_data: Optional[Dict]
    after_data: Optional[Dict]
    ip_address: Optional[str]
    timestamp: datetime
    details: Optional[str]
    
    class Config:
        from_attributes = True
