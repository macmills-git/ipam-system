from pydantic import BaseModel, Field, validator
from typing import Optional, Dict
from datetime import datetime
from app.models.ip_address import IPStatus
import ipaddress

class IPAddressBase(BaseModel):
    address: str = Field(..., description="IP address")
    subnet_id: int
    status: IPStatus = IPStatus.FREE
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    interface: Optional[str] = None
    metadata: Optional[Dict] = {}
    
    @validator('address')
    def validate_ip(cls, v):
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise ValueError('Invalid IP address')
        return v

class IPAddressCreate(IPAddressBase):
    pass

class IPAddressAllocate(BaseModel):
    subnet_id: int
    count: int = Field(1, ge=1, le=100)
    hostname: Optional[str] = None

class IPAddressAssign(BaseModel):
    device_id: int
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    interface: Optional[str] = None

class IPAddressUpdate(BaseModel):
    status: Optional[IPStatus] = None
    assigned_to_id: Optional[int] = None
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    interface: Optional[str] = None
    metadata: Optional[Dict] = None

class IPAddressResponse(IPAddressBase):
    id: int
    assigned_to_id: Optional[int]
    lease_expires: Optional[datetime]
    last_seen: Optional[datetime]
    created_by_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class IPConflictResolve(BaseModel):
    action: str = Field(..., description="release, reassign, or quarantine")
    target_ip_id: Optional[int] = None
    new_device_id: Optional[int] = None
