from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
from app.models.base import TimestampMixin

class IPStatus(str, enum.Enum):
    FREE = "free"
    ASSIGNED = "assigned"
    RESERVED = "reserved"
    QUARANTINED = "quarantined"

class IPAddress(Base, TimestampMixin):
    __tablename__ = "ip_addresses"
    
    id = Column(Integer, primary_key=True, index=True)
    address = Column(INET, unique=True, index=True, nullable=False)
    subnet_id = Column(Integer, ForeignKey("subnets.id"), nullable=False)
    status = Column(SQLEnum(IPStatus), default=IPStatus.FREE, nullable=False, index=True)
    assigned_to_id = Column(Integer, ForeignKey("devices.id"), nullable=True)
    hostname = Column(String(255), nullable=True, index=True)
    mac_address = Column(String(17), nullable=True)
    interface = Column(String(100), nullable=True)
    lease_expires = Column(DateTime(timezone=True), nullable=True)
    metadata = Column(JSON, default=dict, nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    subnet = relationship("Subnet", back_populates="ip_addresses")
    device = relationship("Device", back_populates="ip_addresses")
    created_by_user = relationship("User", foreign_keys=[created_by_id], back_populates="created_ips")
