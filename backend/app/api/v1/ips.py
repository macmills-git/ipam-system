from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.ip_address import IPAddress, IPStatus
from app.schemas.ip_address import (
    IPAddressCreate, IPAddressUpdate, IPAddressResponse,
    IPAddressAllocate, IPAddressAssign, IPConflictResolve
)
from app.services.ip_service import IPService
from app.services.audit_service import log_audit

router = APIRouter()

@router.get("", response_model=List[IPAddressResponse])
async def list_ips(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    subnet_id: Optional[int] = None,
    status: Optional[IPStatus] = None,
    hostname: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(IPAddress)
    
    if subnet_id:
        query = query.filter(IPAddress.subnet_id == subnet_id)
    if status:
        query = query.filter(IPAddress.status == status)
    if hostname:
        query = query.filter(IPAddress.hostname.ilike(f"%{hostname}%"))
    
    ips = query.offset(skip).limit(limit).all()
    return ips

@router.get("/{ip_id}", response_model=IPAddressResponse)
async def get_ip(
    ip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
    if not ip:
        raise HTTPException(status_code=404, detail="IP address not found")
    return ip

@router.post("/allocate", response_model=List[IPAddressResponse])
async def allocate_ips(
    allocation: IPAddressAllocate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    service = IPService(db)
    ips = service.allocate_ips(
        subnet_id=allocation.subnet_id,
        count=allocation.count,
        hostname=allocation.hostname,
        user_id=current_user.id
    )
    
    if not ips:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No available IPs in subnet"
        )
    
    for ip in ips:
        log_audit(db, current_user.id, "allocate", "ip_address", ip.id, after_data={"address": str(ip.address)})
    
    return ips

@router.put("/{ip_id}/assign", response_model=IPAddressResponse)
async def assign_ip(
    ip_id: int,
    assignment: IPAddressAssign,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
    if not ip:
        raise HTTPException(status_code=404, detail="IP address not found")
    
    before_data = {"status": ip.status, "assigned_to_id": ip.assigned_to_id}
    
    ip.status = IPStatus.ASSIGNED
    ip.assigned_to_id = assignment.device_id
    if assignment.hostname:
        ip.hostname = assignment.hostname
    if assignment.mac_address:
        ip.mac_address = assignment.mac_address
    if assignment.interface:
        ip.interface = assignment.interface
    
    db.commit()
    db.refresh(ip)
    
    log_audit(db, current_user.id, "assign", "ip_address", ip.id, before_data=before_data, after_data=assignment.dict())
    
    return ip

@router.put("/{ip_id}", response_model=IPAddressResponse)
async def update_ip(
    ip_id: int,
    ip_data: IPAddressUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
    if not ip:
        raise HTTPException(status_code=404, detail="IP address not found")
    
    before_data = {k: v for k, v in ip.__dict__.items() if not k.startswith('_')}
    
    for key, value in ip_data.dict(exclude_unset=True).items():
        setattr(ip, key, value)
    
    db.commit()
    db.refresh(ip)
    
    log_audit(db, current_user.id, "update", "ip_address", ip.id, before_data=before_data, after_data=ip_data.dict(exclude_unset=True))
    
    return ip

@router.delete("/{ip_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ip(
    ip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    ip = db.query(IPAddress).filter(IPAddress.id == ip_id).first()
    if not ip:
        raise HTTPException(status_code=404, detail="IP address not found")
    
    log_audit(db, current_user.id, "delete", "ip_address", ip.id, before_data={"address": str(ip.address)})
    
    db.delete(ip)
    db.commit()

@router.post("/{ip_id}/scan")
async def scan_ip(
    ip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    service = IPService(db)
    result = service.scan_ip(ip_id)
    
    log_audit(db, current_user.id, "scan", "ip_address", ip_id, details="IP scan initiated")
    
    return result

@router.post("/{ip_id}/conflict-resolve")
async def resolve_conflict(
    ip_id: int,
    resolution: IPConflictResolve,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    service = IPService(db)
    result = service.resolve_conflict(ip_id, resolution.action, resolution.new_device_id)
    
    log_audit(db, current_user.id, "resolve_conflict", "ip_address", ip_id, after_data=resolution.dict())
    
    return result
