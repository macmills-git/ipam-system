from sqlalchemy.orm import Session
from sqlalchemy import func
import ipaddress
from typing import Dict
from app.models.subnet import Subnet
from app.models.ip_address import IPAddress, IPStatus

class SubnetService:
    def __init__(self, db: Session):
        self.db = db
    
    def check_overlap(self, cidr: str) -> bool:
        """Check if subnet overlaps with existing subnets"""
        new_network = ipaddress.ip_network(cidr, strict=False)
        subnets = self.db.query(Subnet).all()
        
        for subnet in subnets:
            existing_network = ipaddress.ip_network(str(subnet.cidr), strict=False)
            if new_network.overlaps(existing_network):
                return True
        return False
    
    def get_subnet_stats(self, subnet_id: int) -> Dict:
        """Calculate subnet utilization statistics"""
        subnet = self.db.query(Subnet).filter(Subnet.id == subnet_id).first()
        if not subnet:
            return {}
        
        network = ipaddress.ip_network(str(subnet.cidr), strict=False)
        total_ips = network.num_addresses
        
        # Count used IPs
        used_ips = self.db.query(func.count(IPAddress.id)).filter(
            IPAddress.subnet_id == subnet_id,
            IPAddress.status.in_([IPStatus.ASSIGNED, IPStatus.RESERVED])
        ).scalar() or 0
        
        free_ips = total_ips - used_ips
        utilization = (used_ips / total_ips * 100) if total_ips > 0 else 0
        
        # Count children
        children_count = self.db.query(func.count(Subnet.id)).filter(
            Subnet.parent_subnet_id == subnet_id
        ).scalar() or 0
        
        return {
            "total_ips": total_ips,
            "used_ips": used_ips,
            "free_ips": free_ips,
            "utilization_percent": round(utilization, 2),
            "children_count": children_count
        }
