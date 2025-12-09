from sqlalchemy import Column, Integer, String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
from app.models.base import TimestampMixin

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    NETWORK_ENGINEER = "network_engineer"
    AUDITOR = "auditor"
    READ_ONLY = "read_only"

class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.READ_ONLY, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")
    created_subnets = relationship("Subnet", foreign_keys="Subnet.created_by_id", back_populates="created_by_user")
    created_ips = relationship("IPAddress", foreign_keys="IPAddress.created_by_id", back_populates="created_by_user")
