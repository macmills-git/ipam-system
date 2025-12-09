from fastapi import APIRouter
from app.api.v1 import auth, subnets, ips, devices, vlans, users, audit_logs, bulk_ops

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(subnets.router, prefix="/subnets", tags=["Subnets"])
api_router.include_router(ips.router, prefix="/ips", tags=["IP Addresses"])
api_router.include_router(devices.router, prefix="/devices", tags=["Devices"])
api_router.include_router(vlans.router, prefix="/vlans", tags=["VLANs"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(audit_logs.router, prefix="/audit-logs", tags=["Audit Logs"])
api_router.include_router(bulk_ops.router, prefix="", tags=["Bulk Operations"])
