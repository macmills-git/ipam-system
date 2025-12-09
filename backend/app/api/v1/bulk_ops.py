from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models.user import User, UserRole
from app.models.subnet import Subnet
from app.models.ip_address import IPAddress
from app.services.bulk_service import BulkService
from app.services.audit_service import log_audit

router = APIRouter()

@router.post("/import/csv")
async def import_csv(
    file: UploadFile = File(...),
    entity_type: str = "subnets",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.ADMIN, UserRole.NETWORK_ENGINEER]))
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be CSV")
    
    content = await file.read()
    service = BulkService(db)
    
    try:
        if entity_type == "subnets":
            result = service.import_subnets_csv(content.decode('utf-8'), current_user.id)
        elif entity_type == "ips":
            result = service.import_ips_csv(content.decode('utf-8'), current_user.id)
        else:
            raise HTTPException(status_code=400, detail="Invalid entity type")
        
        log_audit(db, current_user.id, "import_csv", entity_type, None, details=f"Imported {result['created']} records")
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/export/csv")
async def export_csv(
    entity_type: str = "subnets",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = BulkService(db)
    
    if entity_type == "subnets":
        data = service.export_subnets_csv()
    elif entity_type == "ips":
        data = service.export_ips_csv()
    else:
        raise HTTPException(status_code=400, detail="Invalid entity type")
    
    log_audit(db, current_user.id, "export_csv", entity_type, None)
    
    return Response(
        content=data,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={entity_type}_export.csv"}
    )
