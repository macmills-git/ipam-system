#!/usr/bin/env python3
"""Seed database with sample data"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.vlan import VLAN
from app.models.device import Device
from app.models.subnet import Subnet
from app.models.ip_address import IPAddress, IPStatus

def seed_database():
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(User).first():
            print("Database already seeded")
            return
        
        print("Seeding database...")
        
        # Create users
        admin = User(
            username="admin",
            email="admin@ipam.local",
            hashed_password=get_password_hash("Admin123!"),
            role=UserRole.ADMIN,
            active=True
        )
        engineer = User(
            username="engineer",
            email="engineer@ipam.local",
            hashed_password=get_password_hash("Engineer123!"),
            role=UserRole.NETWORK_ENGINEER,
            active=True
        )
        auditor = User(
            username="auditor",
            email="auditor@ipam.local",
            hashed_password=get_password_hash("Auditor123!"),
            role=UserRole.AUDITOR,
            active=True
        )
        readonly = User(
            username="readonly",
            email="readonly@ipam.local",
            hashed_password=get_password_hash("Readonly123!"),
            role=UserRole.READ_ONLY,
            active=True
        )
        
        db.add_all([admin, engineer, auditor, readonly])
        db.commit()
        print("✓ Created users")
        
        # Create VLANs
        vlan10 = VLAN(name="Management", number=10, description="Management VLAN")
        vlan20 = VLAN(name="Servers", number=20, description="Server VLAN")
        vlan30 = VLAN(name="Workstations", number=30, description="Workstation VLAN")
        
        db.add_all([vlan10, vlan20, vlan30])
        db.commit()
        print("✓ Created VLANs")
        
        # Create devices
        devices = [
            Device(hostname="router-01", device_type="Router", owner="Network Team"),
            Device(hostname="switch-01", device_type="Switch", owner="Network Team"),
            Device(hostname="server-01", device_type="Server", owner="IT Team"),
            Device(hostname="server-02", device_type="Server", owner="IT Team"),
            Device(hostname="workstation-01", device_type="Workstation", owner="John Doe"),
        ]
        
        db.add_all(devices)
        db.commit()
        print("✓ Created devices")
        
        # Create subnets
        subnet1 = Subnet(
            cidr="10.0.0.0/24",
            description="Management Network",
            vlan_id=vlan10.id,
            location="Datacenter A",
            reserved_ranges=[{"start": "10.0.0.1", "end": "10.0.0.10"}],
            tags=["production", "management"],
            created_by_id=admin.id
        )
        subnet2 = Subnet(
            cidr="10.0.1.0/24",
            description="Server Network",
            vlan_id=vlan20.id,
            location="Datacenter A",
            reserved_ranges=[{"start": "10.0.1.1", "end": "10.0.1.10"}],
            tags=["production", "servers"],
            created_by_id=admin.id
        )
        subnet3 = Subnet(
            cidr="10.0.2.0/24",
            description="Workstation Network",
            vlan_id=vlan30.id,
            location="Office Building",
            tags=["production", "workstations"],
            created_by_id=admin.id
        )
        subnet4 = Subnet(
            cidr="2001:db8::/64",
            description="IPv6 Test Network",
            location="Datacenter A",
            tags=["ipv6", "test"],
            created_by_id=admin.id
        )
        
        db.add_all([subnet1, subnet2, subnet3, subnet4])
        db.commit()
        print("✓ Created subnets")
        
        # Create IP addresses
        ips = [
            IPAddress(address="10.0.0.1", subnet_id=subnet1.id, status=IPStatus.RESERVED, hostname="gateway", created_by_id=admin.id),
            IPAddress(address="10.0.0.11", subnet_id=subnet1.id, status=IPStatus.ASSIGNED, hostname="router-01", assigned_to_id=devices[0].id, created_by_id=admin.id),
            IPAddress(address="10.0.0.12", subnet_id=subnet1.id, status=IPStatus.ASSIGNED, hostname="switch-01", assigned_to_id=devices[1].id, created_by_id=admin.id),
            IPAddress(address="10.0.1.20", subnet_id=subnet2.id, status=IPStatus.ASSIGNED, hostname="server-01", assigned_to_id=devices[2].id, created_by_id=admin.id),
            IPAddress(address="10.0.1.21", subnet_id=subnet2.id, status=IPStatus.ASSIGNED, hostname="server-02", assigned_to_id=devices[3].id, created_by_id=admin.id),
            IPAddress(address="10.0.2.100", subnet_id=subnet3.id, status=IPStatus.ASSIGNED, hostname="workstation-01", assigned_to_id=devices[4].id, created_by_id=admin.id),
            IPAddress(address="10.0.2.101", subnet_id=subnet3.id, status=IPStatus.FREE, created_by_id=admin.id),
            IPAddress(address="2001:db8::1", subnet_id=subnet4.id, status=IPStatus.RESERVED, hostname="ipv6-gateway", created_by_id=admin.id),
        ]
        
        db.add_all(ips)
        db.commit()
        print("✓ Created IP addresses")
        
        print("\n✅ Database seeded successfully!")
        print("\nDefault credentials:")
        print("  Admin:    admin@ipam.local / Admin123!")
        print("  Engineer: engineer@ipam.local / Engineer123!")
        print("  Auditor:  auditor@ipam.local / Auditor123!")
        print("  ReadOnly: readonly@ipam.local / Readonly123!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
