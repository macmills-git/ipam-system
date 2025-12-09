# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All endpoints (except `/auth/login`) require JWT authentication.

### Login

```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@ipam.local",
  "password": "Admin123!"
}

Response:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Use Token

```http
GET /subnets
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

## Endpoints

### Subnets

#### List Subnets

```http
GET /subnets?skip=0&limit=100&parent_id=1&vlan_id=2
```

#### Get Subnet

```http
GET /subnets/{id}
```

#### Create Subnet

```http
POST /subnets
Content-Type: application/json

{
  "cidr": "10.0.0.0/24",
  "description": "Production Network",
  "location": "Datacenter A",
  "vlan_id": 1,
  "reserved_ranges": [
    {"start": "10.0.0.1", "end": "10.0.0.10"}
  ],
  "tags": ["production", "critical"]
}
```

#### Update Subnet

```http
PUT /subnets/{id}
Content-Type: application/json

{
  "description": "Updated description",
  "location": "New location"
}
```

#### Delete Subnet

```http
DELETE /subnets/{id}
```

#### Get Subnet Children

```http
GET /subnets/{id}/children
```

### IP Addresses

#### List IPs

```http
GET /ips?subnet_id=1&status=free&hostname=server
```

#### Get IP

```http
GET /ips/{id}
```

#### Allocate IPs

```http
POST /ips/allocate
Content-Type: application/json

{
  "subnet_id": 1,
  "count": 5,
  "hostname": "server-"
}
```

#### Assign IP to Device

```http
PUT /ips/{id}/assign
Content-Type: application/json

{
  "device_id": 1,
  "hostname": "web-server-01",
  "mac_address": "00:11:22:33:44:55",
  "interface": "eth0"
}
```

#### Update IP

```http
PUT /ips/{id}
Content-Type: application/json

{
  "status": "reserved",
  "hostname": "backup-server"
}
```

#### Delete IP

```http
DELETE /ips/{id}
```

#### Scan IP

```http
POST /ips/{id}/scan
```

#### Resolve Conflict

```http
POST /ips/{id}/conflict-resolve
Content-Type: application/json

{
  "action": "reassign",
  "new_device_id": 2
}
```

### Devices

#### List Devices

```http
GET /devices?skip=0&limit=100
```

#### Get Device

```http
GET /devices/{id}
```

#### Create Device

```http
POST /devices
Content-Type: application/json

{
  "hostname": "server-01",
  "owner": "IT Team",
  "device_type": "Server",
  "notes": "Production web server",
  "tags": ["production", "web"]
}
```

#### Update Device

```http
PUT /devices/{id}
Content-Type: application/json

{
  "owner": "DevOps Team",
  "notes": "Migrated to new team"
}
```

#### Delete Device

```http
DELETE /devices/{id}
```

### VLANs

#### List VLANs

```http
GET /vlans
```

#### Create VLAN

```http
POST /vlans
Content-Type: application/json

{
  "name": "Production",
  "number": 100,
  "description": "Production VLAN"
}
```

#### Update VLAN

```http
PUT /vlans/{id}
Content-Type: application/json

{
  "description": "Updated description"
}
```

#### Delete VLAN

```http
DELETE /vlans/{id}
```

### Users (Admin Only)

#### List Users

```http
GET /users
```

#### Create User

```http
POST /users
Content-Type: application/json

{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "role": "network_engineer"
}
```

#### Update User

```http
PUT /users/{id}
Content-Type: application/json

{
  "role": "admin",
  "active": true
}
```

#### Delete User

```http
DELETE /users/{id}
```

### Audit Logs (Admin/Auditor Only)

#### List Audit Logs

```http
GET /audit-logs?user_id=1&action=create&target_type=subnet&start_date=2024-01-01&end_date=2024-12-31
```

### Bulk Operations

#### Export CSV

```http
GET /export/csv?entity_type=subnets
```

#### Import CSV

```http
POST /import/csv
Content-Type: multipart/form-data

file: <csv-file>
entity_type: subnets
```

## Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict (e.g., duplicate)
- `500 Internal Server Error` - Server error

## Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Rate Limiting

- 100 requests per minute per IP address
- Headers included in response:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Requests remaining
  - `X-RateLimit-Reset`: Time when limit resets

## Pagination

List endpoints support pagination:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum records to return (default: 100, max: 1000)

## Filtering

Most list endpoints support filtering via query parameters.

## Interactive Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI JSON: http://localhost:8000/api/v1/openapi.json
