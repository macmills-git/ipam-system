# IPAM System - Documentation Index

Welcome to the IPAM System documentation. This index will help you find the information you need.

## 🚀 Getting Started

**New to IPAM?** Start here:

1. **[QUICKSTART_GUIDE.md](../QUICKSTART_GUIDE.md)** - Get running in 5 minutes
2. **[README.md](../README.md)** - Project overview and features
3. **[PROJECT_SUMMARY.md](../PROJECT_SUMMARY.md)** - Complete project summary

## 📚 Core Documentation

### For Users

- **[QUICKSTART_GUIDE.md](../QUICKSTART_GUIDE.md)**

  - One-command setup
  - First steps
  - Common tasks
  - Troubleshooting basics

- **[README.md](../README.md)**
  - Feature overview
  - Architecture diagram
  - Quick start commands
  - Configuration basics

### For Developers

- **[ARCHITECTURE.md](ARCHITECTURE.md)**

  - System architecture
  - Component details
  - Data flow diagrams
  - Technology choices
  - Scalability design

- **[API.md](API.md)**

  - Complete API reference
  - Authentication guide
  - Endpoint documentation
  - Request/response examples
  - Error codes

- **[TESTING.md](TESTING.md)**
  - Test setup
  - Running tests
  - Writing tests
  - Coverage reports
  - CI/CD integration

### For DevOps/SRE

- **[DEPLOYMENT.md](DEPLOYMENT.md)**

  - Local deployment
  - AWS deployment (Terraform)
  - Kubernetes deployment (Helm)
  - Database setup
  - Monitoring setup
  - Backup/restore procedures
  - Troubleshooting

- **[DEPLOYMENT_CHECKLIST.md](../DEPLOYMENT_CHECKLIST.md)**
  - Pre-deployment checklist
  - Infrastructure setup
  - Application deployment
  - Post-deployment verification
  - Security hardening
  - Go-live checklist

## 🔧 Technical Resources

### API & Integration

- **[postman_collection.json](postman_collection.json)**

  - Ready-to-use Postman collection
  - All API endpoints
  - Example requests
  - Environment variables

- **Swagger UI**
  - Interactive API documentation
  - Try endpoints live
  - Access at: http://localhost:8000/docs

### Code Examples

- **Sample Data**

  - [sample-data/subnets.csv](../sample-data/subnets.csv) - Example subnet data
  - [sample-data/ips.csv](../sample-data/ips.csv) - Example IP data

- **Scripts**
  - [scripts/backup.sh](../scripts/backup.sh) - Database backup
  - [scripts/restore.sh](../scripts/restore.sh) - Database restore
  - [quickstart.sh](../quickstart.sh) - One-command setup

## 📖 By Topic

### Authentication & Security

- **Authentication**: [API.md#authentication](API.md#authentication)
- **Security Features**: [README.md#security](../README.md#security)
- **RBAC**: [ARCHITECTURE.md#security-architecture](ARCHITECTURE.md#security-architecture)
- **Security Checklist**: [DEPLOYMENT_CHECKLIST.md#security-hardening](../DEPLOYMENT_CHECKLIST.md#security-hardening)

### Subnet Management

- **Creating Subnets**: [API.md#subnets](API.md#subnets)
- **Subnet Hierarchy**: [ARCHITECTURE.md#data-flow](ARCHITECTURE.md#data-flow)
- **Subnet Service**: `backend/app/services/subnet_service.py`

### IP Address Management

- **IP Allocation**: [API.md#ip-addresses](API.md#ip-addresses)
- **Allocation Algorithms**: [ARCHITECTURE.md#ip-allocation-flow](ARCHITECTURE.md#ip-allocation-flow)
- **IP Service**: `backend/app/services/ip_service.py`

### Conflict Detection

- **Scanner Agent**: `scanner-agent/scanner.py`
- **Conflict Resolution**: [API.md#resolve-conflict](API.md#resolve-conflict)
- **Conflict Flow**: [ARCHITECTURE.md#conflict-detection-flow](ARCHITECTURE.md#conflict-detection-flow)

### Bulk Operations

- **CSV Import**: [API.md#import-csv](API.md#import-csv)
- **CSV Export**: [API.md#export-csv](API.md#export-csv)
- **Sample Data**: [sample-data/](../sample-data/)

### Monitoring & Observability

- **Prometheus Setup**: [DEPLOYMENT.md#monitoring](DEPLOYMENT.md#monitoring)
- **Grafana Dashboards**: `infra/monitoring/grafana/`
- **Metrics**: [ARCHITECTURE.md#monitoring--observability](ARCHITECTURE.md#monitoring--observability)

### Testing

- **Backend Tests**: [TESTING.md#backend-testing](TESTING.md#backend-testing)
- **Frontend Tests**: [TESTING.md#frontend-testing](TESTING.md#frontend-testing)
- **Integration Tests**: [TESTING.md#integration-testing](TESTING.md#integration-testing)
- **Test Files**: `backend/tests/`

### Deployment

- **Local (Docker Compose)**: [DEPLOYMENT.md#local-development-deployment](DEPLOYMENT.md#local-development-deployment)
- **AWS (Terraform)**: [DEPLOYMENT.md#aws-production-deployment](DEPLOYMENT.md#aws-production-deployment)
- **Kubernetes (Helm)**: [DEPLOYMENT.md#step-3-deploy-to-kubernetes](DEPLOYMENT.md#step-3-deploy-to-kubernetes)

## 🎯 By Role

### Network Engineer

**I want to:**

- **Get started quickly** → [QUICKSTART_GUIDE.md](../QUICKSTART_GUIDE.md)
- **Create subnets** → [API.md#create-subnet](API.md#create-subnet)
- **Allocate IPs** → [API.md#allocate-ips](API.md#allocate-ips)
- **Resolve conflicts** → [API.md#resolve-conflict](API.md#resolve-conflict)
- **Import bulk data** → [API.md#import-csv](API.md#import-csv)
- **Export reports** → [API.md#export-csv](API.md#export-csv)

### System Administrator

**I want to:**

- **Deploy locally** → [DEPLOYMENT.md#local-development-deployment](DEPLOYMENT.md#local-development-deployment)
- **Deploy to AWS** → [DEPLOYMENT.md#aws-production-deployment](DEPLOYMENT.md#aws-production-deployment)
- **Manage users** → [API.md#users](API.md#users)
- **Configure monitoring** → [DEPLOYMENT.md#monitoring](DEPLOYMENT.md#monitoring)
- **Set up backups** → [DEPLOYMENT.md#backup-and-restore](DEPLOYMENT.md#backup-and-restore)
- **Troubleshoot issues** → [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)

### Developer

**I want to:**

- **Understand architecture** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **Use the API** → [API.md](API.md)
- **Run tests** → [TESTING.md](TESTING.md)
- **Contribute code** → [ARCHITECTURE.md#technology-choices-justification](ARCHITECTURE.md#technology-choices-justification)
- **Extend functionality** → `backend/app/` and `frontend/src/`

### DevOps Engineer

**I want to:**

- **Set up CI/CD** → `.github/workflows/ci-cd.yml`
- **Deploy infrastructure** → `infra/terraform/`
- **Configure Kubernetes** → `infra/helm/`
- **Set up monitoring** → `infra/monitoring/`
- **Automate deployments** → [DEPLOYMENT.md](DEPLOYMENT.md)
- **Scale the system** → [ARCHITECTURE.md#scalability](ARCHITECTURE.md#scalability)

### Security Auditor

**I want to:**

- **Review security** → [ARCHITECTURE.md#security-architecture](ARCHITECTURE.md#security-architecture)
- **Check audit logs** → [API.md#audit-logs](API.md#audit-logs)
- **Verify compliance** → [DEPLOYMENT_CHECKLIST.md#compliance](../DEPLOYMENT_CHECKLIST.md#compliance)
- **Test security** → [TESTING.md#security-testing](TESTING.md#security-testing)

## 🔍 Quick Reference

### Common Commands

```bash
# Start locally
./quickstart.sh

# Run tests
cd backend && pytest --cov=app
cd frontend && npm test

# Deploy to AWS
cd infra/terraform && terraform apply
helm install ipam ./infra/helm/ipam-chart

# Backup database
./scripts/backup.sh

# View logs
docker-compose logs -f backend
kubectl logs -f deployment/ipam-backend
```

### Important URLs

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **Swagger**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001
- **Prometheus**: http://localhost:9090

### Default Credentials

- **Email**: admin@ipam.local
- **Password**: Admin123!
- **Grafana**: admin / admin

⚠️ **Change these in production!**

## 📁 File Structure Reference

```
ipam-system/
├── README.md                    # Main documentation
├── QUICKSTART_GUIDE.md         # 5-minute setup
├── PROJECT_SUMMARY.md          # Complete summary
├── DEPLOYMENT_CHECKLIST.md     # Deployment checklist
├── quickstart.sh               # Setup script
├── docker-compose.yml          # Local development
├── .env.example               # Configuration template
│
├── backend/                    # FastAPI application
│   ├── app/                   # Application code
│   ├── alembic/              # Database migrations
│   ├── scripts/              # Utility scripts
│   ├── tests/                # Test suite
│   └── requirements.txt      # Python dependencies
│
├── frontend/                   # React application
│   ├── src/                  # Source code
│   ├── public/               # Static files
│   └── package.json          # Node dependencies
│
├── scanner-agent/             # IP scanner service
│   ├── scanner.py            # Scanner implementation
│   └── requirements.txt      # Dependencies
│
├── infra/                     # Infrastructure as Code
│   ├── terraform/            # AWS infrastructure
│   ├── helm/                 # Kubernetes charts
│   └── monitoring/           # Prometheus + Grafana
│
├── docker/                    # Dockerfiles
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── scanner.Dockerfile
│
├── docs/                      # Documentation
│   ├── INDEX.md              # This file
│   ├── API.md                # API reference
│   ├── ARCHITECTURE.md       # System design
│   ├── DEPLOYMENT.md         # Deployment guide
│   ├── TESTING.md            # Testing guide
│   └── postman_collection.json
│
├── sample-data/               # Sample CSV files
├── scripts/                   # Helper scripts
└── .github/workflows/         # CI/CD pipelines
```

## 🆘 Getting Help

### Documentation Issues

If you can't find what you're looking for:

1. Check this index
2. Use search in your editor (Ctrl+F / Cmd+F)
3. Check the [README.md](../README.md)
4. Review [ARCHITECTURE.md](ARCHITECTURE.md)

### Technical Issues

1. Check [DEPLOYMENT.md#troubleshooting](DEPLOYMENT.md#troubleshooting)
2. Review logs: `docker-compose logs`
3. Check GitHub Issues
4. Contact support

### Feature Requests

1. Review [ARCHITECTURE.md#future-enhancements](ARCHITECTURE.md#future-enhancements)
2. Open GitHub Issue
3. Submit Pull Request

## 📝 Documentation Updates

This documentation is maintained alongside the code. When updating:

1. Update relevant documentation files
2. Update this index if adding new docs
3. Keep examples up to date
4. Test all commands and examples
5. Update version numbers

## 🎓 Learning Path

**Recommended order for new users:**

1. [QUICKSTART_GUIDE.md](../QUICKSTART_GUIDE.md) - Get it running
2. [README.md](../README.md) - Understand features
3. [API.md](API.md) - Learn the API
4. [ARCHITECTURE.md](ARCHITECTURE.md) - Understand design
5. [DEPLOYMENT.md](DEPLOYMENT.md) - Deploy to production
6. [TESTING.md](TESTING.md) - Contribute code

## 📊 Documentation Statistics

- **Total Documentation Files**: 10+
- **Total Pages**: 100+
- **Code Examples**: 50+
- **API Endpoints Documented**: 30+
- **Deployment Guides**: 3 (Local, AWS, K8s)

## 🔄 Version History

- **v1.0.0** - Initial release
  - Complete IPAM system
  - Full documentation
  - Production-ready

---

**Last Updated**: 2024-01-01
**Maintained By**: IPAM Development Team
**License**: MIT
