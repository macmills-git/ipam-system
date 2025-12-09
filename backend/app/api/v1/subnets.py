from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.subnet import Subnet
from app.schemas.subnet import SubnetCreate, SubnetUpdate, SubnetResponse, SubnetWithStats
from app.services.subnet_service import SubnetService
from app.services.audit_service import log_audit

router = APIRouter()

@router.get("", response_model=List[SubnetResponse])
async def list_subnets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    parent_id: Optional[int] = None,
    vlan_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Subnet)
    
    if parent_id is not None:
        query = query.filter(Subnet.parent_subnet_id == parent_id)
    if vlan_id is not None:
        query = query.filter(Subnet.vlan_id == vlan_id)
    
    subnets = query.offset(skip).limit(limit).all()
    return subnets

@router.get("/{subnet_id}", response_model=SubnetWithStats)
async def get_subnet(
    subnet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subnet = db.query(Subnet).filter(Subnet.id == subnet_id).first()
    if not subnet:
        raise HTTPException(status_code=404, detail="Subnet not found")
    
    service = SubnetService(db)
    stats = service.get_subnet_stats(subnet_id)
    
    return {**subnet.__dict__, **stats}

@router.post("", response_model=SubnetResponse, status_code=status.HTTP_201_CREATED)
async def create_subnet(
    subnet_data: SubnetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    service = SubnetService(db)
    
    # Check for overlaps
    if service.check_overlap(subnet_data.cidr):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Subnet overlaps with existing subnet"
        )
    
    subnet = Subnet(
        **subnet_data.dict(),
        created_by_id=current_user.id
    )
    db.add(subnet)
    db.commit()
    db.refresh(subnet)
    
    log_audit(db, current_user.id, "create", "subnet", subnet.id, after_data=subnet_data.dict())
    
    return subnet

@router.put("/{subnet_id}", response_model=SubnetResponse)
async def update_subnet(
    subnet_id: int,
    subnet_data: SubnetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    subnet = db.query(Subnet).filter(Subnet.id == subnet_id).first()
    if not subnet:
        raise HTTPException(status_code=404, detail="Subnet not found")
    
    before_data = {k: v for k, v in subnet.__dict__.items() if not k.startswith('_')}
    
    for key, value in subnet_data.dict(exclude_unset=True).items():
        setattr(subnet, key, value)
    
    db.commit()
    db.refresh(subnet)
    
    log_audit(db, current_user.id, "update", "subnet", subnet.id, before_data=before_data, after_data=subnet_data.dict(exclude_unset=True))
    
    return subnet

@router.delete("/{subnet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subnet(
    subnet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    subnet = db.query(Subnet).filter(Subnet.id == subnet_id).first()
    if not subnet:
        raise HTTPException(status_code=404, detail="Subnet not found")
    
    # Check if subnet has IPs
    if subnet.ip_addresses:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete subnet with assigned IPs"
        )
    
    log_audit(db, current_user.id, "delete", "subnet", subnet.id, before_data={"cidr": str(subnet.cidr)})
    
    db.delete(subnet)
    db.commit()

@router.get("/{subnet_id}/children", response_model=List[SubnetResponse])
async def get_subnet_children(
    subnet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    subnet = db.query(Subnet).filter(Subnet.id == subnet_id).first()
    if not subnet:
        raise HTTPException(status_code=404, detail="Subnet not found")
    
    return subnet.children
