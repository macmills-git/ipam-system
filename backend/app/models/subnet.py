from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class Subnet(Base, TimestampMixin):
    __tablename__ = "subnets"
    
    id = Column(Integer, primary_key=True, index=True)
    cidr = Column(INET, unique=True, index=True, nullable=False)
    parent_subnet_id = Column(Integer, ForeignKey("subnets.id"), nullable=True)
    description = Column(Text, nullable=True)
    vlan_id = Column(Integer, ForeignKey("vlans.id"), nullable=True)
    location = Column(String(255), nullable=True)
    reserved_ranges = Column(JSON, default=list, nullable=True)  # [{"start": "10.0.0.1", "end": "10.0.0.10"}]
    tags = Column(JSON, default=list, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    parent_subnet = relationship("Subnet", remote_side=[id], backref="children")
    vlan = relationship("VLAN", back_populates="subnets")
    ip_addresses = relationship("IPAddress", back_populates="subnet", cascade="all, delete-orphan")
    created_by_user = relationship("User", foreign_keys=[created_by_id], back_populates="created_subnets")
