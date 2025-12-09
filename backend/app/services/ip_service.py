from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import ipaddress
from app.models.subnet import Subnet
from app.models.ip_address import IPAddress, IPStatus

class IPService:
    def __init__(self, db: Session):
        self.db = db
    
    def allocate_ips(
        self,
        subnet_id: int,
        count: int = 1,
        hostname: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> List[IPAddress]:
        """Allocate first available IPs in subnet"""
        subnet = self.db.query(Subnet).filter(Subnet.id == subnet_id).first()
        if not subnet:
            return []
        
        network = ipaddress.ip_network(str(subnet.cidr), strict=False)
        allocated = []
        
        # Get existing IPs
        existing_ips = {
            str(ip.address) for ip in 
            self.db.query(IPAddress).filter(IPAddress.subnet_id == subnet_id).all()
        }
        
        # Find available IPs
        for ip in network.hosts():
            ip_str = str(ip)
            if ip_str not in existing_ips:
                # Check reserved ranges
                if self._is_reserved(ip_str, subnet.reserved_ranges or []):
                    continue
                
                new_ip = IPAddress(
                    address=ip_str,
                    subnet_id=subnet_id,
                    status=IPStatus.FREE,
                    hostname=hostname,
                    created_by_id=user_id
                )
                self.db.add(new_ip)
                allocated.append(new_ip)
                
                if len(allocated) >= count:
                    break
        
        self.db.commit()
        for ip in allocated:
            self.db.refresh(ip)
        
        return allocated
    
    def _is_reserved(self, ip: str, reserved_ranges: List[dict]) -> bool:
        """Check if IP is in reserved range"""
        ip_obj = ipaddress.ip_address(ip)
        for range_def in reserved_ranges:
            start = ipaddress.ip_address(range_def.get('start', '0.0.0.0'))
            end = ipaddress.ip_address(range_def.get('end', '0.0.0.0'))
            if start <= ip_obj <= end:
                return True
        return False
    
    def scan_ip(self, ip_id: int) -> dict:
        """Scan IP address (mock implementation)"""
        ip = self.db.query(IPAddress).filter(IPAddress.id == ip_id).first()
        if not ip:
            return {"error": "IP not found"}
        
        # Mock scan result
        ip.last_seen = datetime.utcnow()
        self.db.commit()
        
        return {
            "ip": str(ip.address),
            "status": "reachable",
            "last_seen": ip.last_seen,
            "scan_type": "mock"
        }
    
    def resolve_conflict(self, ip_id: int, action: str, new_device_id: Optional[int] = None) -> dict:
        """Resolve IP conflict"""
        ip = self.db.query(IPAddress).filter(IPAddress.id == ip_id).first()
        if not ip:
            return {"error": "IP not found"}
        
        if action == "release":
            ip.status = IPStatus.FREE
            ip.assigned_to_id = None
        elif action == "reassign" and new_device_id:
            ip.assigned_to_id = new_device_id
            ip.status = IPStatus.ASSIGNED
        elif action == "quarantine":
            ip.status = IPStatus.QUARANTINED
        
        self.db.commit()
        return {"status": "resolved", "action": action}
