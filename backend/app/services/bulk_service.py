from sqlalchemy.orm import Session
import csv
import io
from typing import Dict
from app.models.subnet import Subnet
from app.models.ip_address import IPAddress, IPStatus

class BulkService:
    def __init__(self, db: Session):
        self.db = db
    
    def import_subnets_csv(self, csv_content: str, user_id: int) -> Dict:
        """Import subnets from CSV"""
        reader = csv.DictReader(io.StringIO(csv_content))
        created = 0
        errors = []
        
        for row in reader:
            try:
                subnet = Subnet(
                    cidr=row['cidr'],
                    description=row.get('description'),
                    location=row.get('location'),
                    created_by_id=user_id
                )
                self.db.add(subnet)
                created += 1
            except Exception as e:
                errors.append(f"Row {created + 1}: {str(e)}")
        
        self.db.commit()
        return {"created": created, "errors": errors}
    
    def import_ips_csv(self, csv_content: str, user_id: int) -> Dict:
        """Import IPs from CSV"""
        reader = csv.DictReader(io.StringIO(csv_content))
        created = 0
        errors = []
        
        for row in reader:
            try:
                ip = IPAddress(
                    address=row['address'],
                    subnet_id=int(row['subnet_id']),
                    status=IPStatus(row.get('status', 'free')),
                    hostname=row.get('hostname'),
                    created_by_id=user_id
                )
                self.db.add(ip)
                created += 1
            except Exception as e:
                errors.append(f"Row {created + 1}: {str(e)}")
        
        self.db.commit()
        return {"created": created, "errors": errors}
    
    def export_subnets_csv(self) -> str:
        """Export subnets to CSV"""
        subnets = self.db.query(Subnet).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'cidr', 'description', 'location', 'vlan_id', 'created_at'])
        
        for subnet in subnets:
            writer.writerow([
                subnet.id,
                str(subnet.cidr),
                subnet.description or '',
                subnet.location or '',
                subnet.vlan_id or '',
                subnet.created_at
            ])
        
        return output.getvalue()
    
    def export_ips_csv(self) -> str:
        """Export IPs to CSV"""
        ips = self.db.query(IPAddress).all()
        
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['id', 'address', 'subnet_id', 'status', 'hostname', 'device_id', 'created_at'])
        
        for ip in ips:
            writer.writerow([
                ip.id,
                str(ip.address),
                ip.subnet_id,
                ip.status.value,
                ip.hostname or '',
                ip.assigned_to_id or '',
                ip.created_at
            ])
        
        return output.getvalue()
