from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DeviceBase(BaseModel):
    hostname: str = Field(..., min_length=1, max_length=255)
    owner: Optional[str] = None
    device_type: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = []

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    hostname: Optional[str] = Field(None, min_length=1, max_length=255)
    owner: Optional[str] = None
    device_type: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

class DeviceResponse(DeviceBase):
    id: int
    last_seen: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
