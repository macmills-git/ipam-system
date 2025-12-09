from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from datetime import datetime
import ipaddress

class SubnetBase(BaseModel):
    cidr: str = Field(..., description="CIDR notation (e.g., 10.0.0.0/24)")
    description: Optional[str] = None
    parent_subnet_id: Optional[int] = None
    vlan_id: Optional[int] = None
    location: Optional[str] = None
    reserved_ranges: Optional[List[Dict[str, str]]] = []
    tags: Optional[List[str]] = []
    
    @validator('cidr')
    def validate_cidr(cls, v):
        try:
            ipaddress.ip_network(v, strict=False)
        except ValueError:
            raise ValueError('Invalid CIDR notation')
        return v

class SubnetCreate(SubnetBase):
    pass

class SubnetUpdate(BaseModel):
    description: Optional[str] = None
    vlan_id: Optional[int] = None
    location: Optional[str] = None
    reserved_ranges: Optional[List[Dict[str, str]]] = None
    tags: Optional[List[str]] = None

class SubnetResponse(SubnetBase):
    id: int
    created_by_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SubnetWithStats(SubnetResponse):
    total_ips: int
    used_ips: int
    free_ips: int
    utilization_percent: float
    children_count: int
