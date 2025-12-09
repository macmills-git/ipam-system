from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.vlan import VLAN
from app.schemas.vlan import VLANCreate, VLANUpdate, VLANResponse
from app.services.audit_service import log_audit

router = APIRouter()

@router.get("", response_model=List[VLANResponse])
async def list_vlans(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vlans = db.query(VLAN).offset(skip).limit(limit).all()
    return vlans

@router.post("", response_model=VLANResponse, status_code=status.HTTP_201_CREATED)
async def create_vlan(
    vlan_data: VLANCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    vlan = VLAN(**vlan_data.dict())
    db.add(vlan)
    db.commit()
    db.refresh(vlan)
    log_audit(db, current_user.id, "create", "vlan", vlan.id, after_data=vlan_data.dict())
    return vlan

@router.put("/{vlan_id}", response_model=VLANResponse)
async def update_vlan(
    vlan_id: int,
    vlan_data: VLANUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    vlan = db.query(VLAN).filter(VLAN.id == vlan_id).first()
    if not vlan:
        raise HTTPException(status_code=404, detail="VLAN not found")
    
    for key, value in vlan_data.dict(exclude_unset=True).items():
        setattr(vlan, key, value)
    
    db.commit()
    db.refresh(vlan)
    log_audit(db, current_user.id, "update", "vlan", vlan.id)
    return vlan

@router.delete("/{vlan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vlan(
    vlan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    vlan = db.query(VLAN).filter(VLAN.id == vlan_id).first()
    if not vlan:
        raise HTTPException(status_code=404, detail="VLAN not found")
    
    log_audit(db, current_user.id, "delete", "vlan", vlan.id)
    db.delete(vlan)
    db.commit()
