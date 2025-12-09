from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class Device(Base, TimestampMixin):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(255), unique=True, index=True, nullable=False)
    owner = Column(String(255), nullable=True)
    device_type = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    tags = Column(JSON, default=list, nullable=True)
    
    # Relationships
    ip_addresses = relationship("IPAddress", back_populates="device")
