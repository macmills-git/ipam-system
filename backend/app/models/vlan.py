from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class VLAN(Base, TimestampMixin):
    __tablename__ = "vlans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    number = Column(Integer, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    
    # Relationships
    subnets = relationship("Subnet", back_populates="vlan")
