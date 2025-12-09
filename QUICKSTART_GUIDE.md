# IPAM System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites

- Docker & Docker Compose installed
- 8GB RAM available
- Ports 3000, 8000, 5432, 6379 available

### One-Command Start

```bash
# Make script executable (Linux/macOS)
chmod +x quickstart.sh

# Run quick start
./quickstart.sh
```

**Windows users:**

```powershell
docker-compose up --build -d
```

### Access the Application

After 1-2 minutes, open your browser:

- **Frontend**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001

**Login with:**

- Email: `admin@ipam.local`
- Password: `Admin123!`

## 📋 What You Get

✅ Full IPv4 & IPv6 support
✅ Subnet management with tree view
✅ Automatic IP allocation
✅ Device inventory
✅ VLAN management
✅ Role-based access control
✅ Complete audit logging
✅ CSV import/export
✅ Real-time monitoring dashboards
✅ REST API with Swagger docs

## 🎯 Quick Tasks

### 1. Create Your First Subnet

```bash
curl -X POST http://localhost:8000/api/v1/subnets \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cidr": "10.0.0.0/24",
    "description": "My First Network",
    "location": "Office"
  }'
```

Or use the UI:

1. Click "Subnets" in navigation
2. Click "Add Subnet"
3. Enter CIDR: `10.0.0.0/24`
4. Click "Create"

### 2. Allocate IP Addresses

```bash
curl -X POST http://localhost:8000/api/v1/ips/allocate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "subnet_id": 1,
    "count": 10
  }'
```

Or use the UI:

1. Go to "IP Addresses"
2. Click "Allocate IP"
3. Select subnet and quantity

### 3. Import Bulk Data

```bash
# Use sample data
curl -X POST http://localhost:8000/api/v1/import/csv \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@sample-data/subnets.csv" \
  -F "entity_type=subnets"
```

## 🧪 Run Tests

```bash
# Backend tests
cd backend
pytest --cov=app --cov-report=term

# Frontend tests
cd frontend
npm test -- --coverage
```

## 📊 View Monitoring

1. Open Grafana: http://localhost:3001
2. Login: admin / admin
3. Navigate to Dashboards
4. View IPAM metrics

## 🛠️ Common Commands

```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart services
docker-compose restart

# Stop everything
docker-compose down

# Stop and remove data
docker-compose down -v

# Backup database
./scripts/backup.sh

# Restore database
./scripts/restore.sh backups/ipam_backup_20240101.sql.gz
```

## 📚 Next Steps

1. **Read the docs**:

   - [Full README](README.md)
   - [API Documentation](docs/API.md)
   - [Architecture](docs/ARCHITECTURE.md)
   - [Deployment Guide](docs/DEPLOYMENT.md)

2. **Explore the API**:

   - Open http://localhost:8000/docs
   - Try the interactive Swagger UI
   - Import [Postman collection](docs/postman_collection.json)

3. **Customize**:

   - Edit `.env` for configuration
   - Modify `docker-compose.yml` for services
   - Update frontend in `frontend/src/`

4. **Deploy to Production**:
   - Follow [Deployment Guide](docs/DEPLOYMENT.md)
   - Use Terraform for AWS infrastructure
   - Deploy with Helm to Kubernetes

## 🔒 Security Notes

⚠️ **Before Production:**

1. Change default passwords in `.env`
2. Generate new SECRET_KEY (32+ characters)
3. Configure CORS_ORIGINS for your domain
4. Enable HTTPS with valid certificates
5. Review security settings in `backend/app/core/security.py`
6. Set up firewall rules
7. Enable database encryption
8. Configure backup retention

## 🐛 Troubleshooting

### Services won't start

```bash
# Check if ports are in use
docker-compose ps
lsof -i :8000  # Check port 8000

# View detailed logs
docker-compose logs backend
```

### Database connection failed

```bash
# Restart database
docker-compose restart postgres

# Check database is ready
docker-compose exec postgres pg_isready -U ipam
```

### Frontend can't reach API

```bash
# Check CORS settings in .env
CORS_ORIGINS=http://localhost:3000

# Restart backend
docker-compose restart backend
```

### Tests failing

```bash
# Clean test database
docker-compose down -v
docker-compose up -d postgres
cd backend && alembic upgrade head
pytest
```

## 💡 Tips

- **Performance**: Increase Docker memory to 4GB+ for better performance
- **Development**: Use `docker-compose logs -f` to watch logs in real-time
- **Database**: Access PostgreSQL directly: `docker-compose exec postgres psql -U ipam`
- **Redis**: Check cache: `docker-compose exec redis redis-cli`
- **Scanner**: Enable real scanning by setting `MOCK_MODE=false` in scanner service

## 📞 Support

- **Documentation**: Check `/docs` folder
- **Issues**: GitHub Issues
- **API Questions**: See Swagger docs at `/docs`
- **Community**: [Link to community forum]

## 🎓 Learning Resources

### Video Tutorials (Suggested)

1. Quick Start (5 min)
2. Creating Subnets (10 min)
3. IP Allocation Strategies (15 min)
4. User Management & RBAC (10 min)
5. Production Deployment (30 min)

### Example Workflows

**Network Engineer Daily Tasks:**

1. Check dashboard for IP utilization
2. Allocate IPs for new devices
3. Resolve any conflicts
4. Export reports for management

**Admin Tasks:**

1. Create user accounts
2. Assign roles
3. Review audit logs
4. Monitor system health

**Auditor Tasks:**

1. Review audit logs
2. Generate compliance reports
3. Track changes over time

## 🚢 Production Deployment Checklist

- [ ] Change all default passwords
- [ ] Configure production database (RDS)
- [ ] Set up Redis cluster
- [ ] Configure HTTPS/TLS
- [ ] Set up monitoring alerts
- [ ] Configure automated backups
- [ ] Test disaster recovery
- [ ] Set up CI/CD pipeline
- [ ] Configure logging aggregation
- [ ] Review security settings
- [ ] Load test the system
- [ ] Document custom configurations
- [ ] Train users
- [ ] Set up support process

## 📈 Scaling Guide

**Small (< 1000 IPs):**

- Single backend instance
- db.t3.micro RDS
- Basic monitoring

**Medium (1000-10000 IPs):**

- 2-3 backend instances
- db.t3.small RDS
- Redis cache
- Enhanced monitoring

**Large (10000+ IPs):**

- 5+ backend instances with auto-scaling
- db.t3.medium+ RDS with read replicas
- Redis cluster
- Full monitoring stack
- CDN for frontend

## 🎉 Success!

You now have a fully functional IPAM system running locally. Explore the features, import your network data, and when ready, deploy to production following the deployment guide.

**Happy IP Management! 🌐**
