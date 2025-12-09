from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class VLANBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    number: int = Field(..., ge=1, le=4094)
    description: Optional[str] = None

class VLANCreate(VLANBase):
    pass

class VLANUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    number: Optional[int] = Field(None, ge=1, le=4094)
    description: Optional[str] = None

class VLANResponse(VLANBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
