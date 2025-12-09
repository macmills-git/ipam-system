from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from app.models.audit_log import AuditLog

def log_audit(
    db: Session,
    user_id: Optional[int],
    action: str,
    target_type: str,
    target_id: Optional[int] = None,
    before_data: Optional[Dict[str, Any]] = None,
    after_data: Optional[Dict[str, Any]] = None,
    ip_address: Optional[str] = None,
    details: Optional[str] = None
):
    audit_log = AuditLog(
        user_id=user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        before_data=before_data,
        after_data=after_data,
        ip_address=ip_address,
        details=details
    )
    db.add(audit_log)
    db.commit()
    return audit_log
