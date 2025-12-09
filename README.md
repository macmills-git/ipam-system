# Enterprise IPAM System

Production-ready IP Address Management system with IPv4/IPv6 support, RBAC, conflict detection, and cloud deployment.

## 🚀 Quick Start (Local Development)

```bash
# Clone and start everything
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# API: http://localhost:8000
# Swagger: http://localhost:8000/docs
# Grafana: http://localhost:3001 (admin/admin)
```

Default credentials: `admin@ipam.local` / `Admin123!`

## 📋 Features

✅ IPv4 & IPv6 support with CIDR notation
✅ Full CRUD for subnets, IPs, devices, VLANs, DNS
✅ Automatic IP allocation (first-available, best-fit)
✅ IP conflict detection & quarantine workflow
✅ Subnet tree explorer & searchable IP table
✅ Role-Based Access Control (Admin, Engineer, Auditor, Read-only)
✅ JWT authentication + bcrypt password hashing
✅ Dashboard with utilization charts
✅ Complete audit logging
✅ CSV export/import for bulk operations
✅ REST API with OpenAPI/Swagger docs
✅ Comprehensive test suite (>70% coverage)
✅ Docker containerized
✅ Kubernetes Helm charts
✅ Terraform IaC for AWS
✅ CI/CD with GitHub Actions
✅ Prometheus metrics + Grafana dashboards
✅ IP scanner service (mock + real agent)

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│   FastAPI    │─────▶│ PostgreSQL  │
│  Frontend   │      │   Backend    │      │  Database   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ├─────▶ Redis (Cache/Queue)
                            │
                            └─────▶ Scanner Agent
```

## 🧪 Run Tests

```bash
# Backend tests with coverage
cd backend
python -m pytest --cov=app --cov-report=html --cov-report=term
# Coverage report: backend/htmlcov/index.html

# Frontend tests
cd frontend
npm test -- --coverage
```

## 📦 Production Deployment

### Prerequisites

- AWS CLI configured
- kubectl installed
- Terraform >= 1.0
- Helm >= 3.0

### Deploy to AWS

```bash
# 1. Provision infrastructure
cd infra/terraform
terraform init
terraform plan -out=tfplan
terraform apply tfplan

# 2. Configure kubectl
aws eks update-kubeconfig --name ipam-cluster --region us-east-1

# 3. Deploy application
cd ../helm
helm install ipam ./ipam-chart \
  --set database.host=$(terraform output -raw db_endpoint) \
  --set database.password=$(aws secretsmanager get-secret-value --secret-id ipam-db-password --query SecretString --output text)

# 4. Get load balancer URL
kubectl get ingress ipam-ingress
```

## 📊 Monitoring

- **Metrics**: Prometheus scrapes `/metrics` endpoint
- **Dashboards**: Grafana pre-configured with IPAM dashboard
- **Alerts**: Configured for high conflict rate, low IP availability
- **Logs**: Structured JSON logs to stdout (CloudWatch/ELK compatible)

## 🔒 Security

- Passwords hashed with bcrypt (12 rounds)
- JWT tokens with 15min access + 7day refresh
- RBAC enforced on all endpoints
- Rate limiting (100 req/min per IP)
- CORS configured for production domains
- SQL injection protection via SQLAlchemy ORM
- Input validation with Pydantic
- Security headers (HSTS, CSP, X-Frame-Options)

## 📖 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Postman Collection**: `docs/postman_collection.json`

### Key Endpoints

```bash
# Authentication
POST /api/v1/auth/login
POST /api/v1/auth/refresh

# Subnets
GET    /api/v1/subnets
POST   /api/v1/subnets
GET    /api/v1/subnets/{id}/children
DELETE /api/v1/subnets/{id}

# IP Addresses
GET    /api/v1/ips?subnet_id=1&status=free
POST   /api/v1/ips/allocate
PUT    /api/v1/ips/{id}/assign
POST   /api/v1/ips/{id}/scan

# Devices, VLANs, Users
GET/POST /api/v1/devices
GET/POST /api/v1/vlans
GET/POST /api/v1/users

# Bulk Operations
POST /api/v1/export/csv
POST /api/v1/import/csv

# Audit
GET /api/v1/audit-logs
```

## 🗂️ Project Structure

```
.
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── core/        # Config, security, database
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── services/    # Business logic
│   │   └── tests/       # Test suite
│   ├── alembic/         # Database migrations
│   └── requirements.txt
├── frontend/            # React TypeScript app
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API client
│   │   └── types/       # TypeScript types
│   └── package.json
├── infra/
│   ├── terraform/       # AWS infrastructure
│   └── helm/           # Kubernetes charts
├── docker/
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── scanner.Dockerfile
├── scanner-agent/       # Standalone IP scanner
├── scripts/            # Utility scripts
├── sample-data/        # Demo data & seed script
├── docs/              # Documentation
└── docker-compose.yml
```

## 🔧 Configuration

Copy `.env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://ipam:password@localhost:5432/ipam

# Security
SECRET_KEY=your-secret-key-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15

# Redis
REDIS_URL=redis://localhost:6379/0

# Scanner
SCANNER_ENABLED=true
SCANNER_INTERVAL_SECONDS=300
```

## 📥 Sample Data

```bash
# Load demo dataset (subnets, IPs, devices)
cd backend
python scripts/seed_data.py

# Import from CSV
curl -X POST http://localhost:8000/api/v1/import/csv \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample-data/subnets.csv"
```

## 🔍 Scanner Agent

The scanner agent can run on-premises to discover IPs:

```bash
# Run scanner agent (requires network access)
cd scanner-agent
python scanner.py --api-url http://ipam.example.com --api-key $KEY

# Or use Docker
docker run -d --network host ipam-scanner:latest
```

## 🚨 Troubleshooting

**Database connection failed**

```bash
# Check PostgreSQL is running
docker-compose ps postgres
# View logs
docker-compose logs postgres
```

**Frontend can't reach API**

```bash
# Check CORS settings in backend/.env
CORS_ORIGINS=http://localhost:3000
```

**Tests failing**

```bash
# Ensure test database is clean
docker-compose down -v
docker-compose up -d postgres
cd backend && alembic upgrade head
```

## 📝 User Roles

| Role                 | Permissions                                          |
| -------------------- | ---------------------------------------------------- |
| **Admin**            | Full access, user management, system config          |
| **Network Engineer** | Create/modify subnets, assign IPs, resolve conflicts |
| **Auditor**          | Read-only + audit log access                         |
| **Read-only**        | View subnets, IPs, devices (no modifications)        |

## 🔄 Backup & Restore

```bash
# Backup database
docker-compose exec postgres pg_dump -U ipam ipam > backup.sql

# Restore
docker-compose exec -T postgres psql -U ipam ipam < backup.sql

# Automated backups (production)
# Configured in Terraform: RDS automated backups (7 day retention)
```



