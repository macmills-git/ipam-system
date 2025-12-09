# IPAM System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer / Ingress                  │
│                    (AWS ALB / Kubernetes Ingress)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
        ┌───────▼────────┐       ┌───────▼────────┐
        │   Frontend     │       │    Backend     │
        │  React + TS    │       │    FastAPI     │
        │  (Port 3000)   │       │  (Port 8000)   │
        └────────────────┘       └───────┬────────┘
                                         │
                        ┌────────────────┼────────────────┐
                        │                │                │
                ┌───────▼────────┐  ┌───▼────┐  ┌───────▼────────┐
                │   PostgreSQL   │  │ Redis  │  │  Scanner Agent │
                │   (Port 5432)  │  │ (6379) │  │  (Background)  │
                └────────────────┘  └────────┘  └────────────────┘
                        │
                ┌───────▼────────┐
                │  Prometheus    │
                │  + Grafana     │
                │  (Monitoring)  │
                └────────────────┘
```

## Component Details

### Frontend (React + TypeScript)

- **Technology**: React 18, TypeScript, Tailwind CSS
- **Features**:
  - Dashboard with charts (Chart.js)
  - Subnet tree explorer
  - IP address table with filtering
  - Device management
  - VLAN management
  - User management (admin)
  - Audit log viewer
- **Authentication**: JWT tokens stored in localStorage
- **API Communication**: Axios with interceptors for token refresh

### Backend (FastAPI)

- **Technology**: Python 3.11, FastAPI, SQLAlchemy
- **Features**:
  - RESTful API with OpenAPI documentation
  - JWT authentication with refresh tokens
  - Role-based access control (RBAC)
  - Automatic IP allocation algorithms
  - Conflict detection
  - CSV import/export
  - Audit logging
  - Prometheus metrics
- **Database**: PostgreSQL with INET types for IP addresses
- **Caching**: Redis for session management and async tasks

### Database (PostgreSQL)

- **Version**: 15+
- **Key Features**:
  - INET/CIDR native types for IP addresses
  - JSONB for flexible metadata
  - Foreign key constraints
  - Indexes on frequently queried fields
- **Tables**:
  - users (authentication & RBAC)
  - subnets (CIDR, hierarchy)
  - ip_addresses (status, assignments)
  - devices (inventory)
  - vlans (network segmentation)
  - audit_logs (compliance)

### Scanner Agent

- **Technology**: Python 3.11
- **Modes**:
  - Mock mode (for cloud/restricted environments)
  - Real mode (ICMP ping + TCP port scanning)
- **Features**:
  - Periodic IP scanning
  - Reachability checks
  - Port scanning (80, 443, custom)
  - Updates last_seen timestamps
  - Conflict detection

### Monitoring Stack

- **Prometheus**: Metrics collection
- **Grafana**: Visualization dashboards
- **Metrics Tracked**:
  - API request rates
  - Response times
  - IP utilization
  - Conflict rates
  - Database connections
  - Error rates

## Data Flow

### IP Allocation Flow

```
1. User requests IP allocation
   ↓
2. Backend validates subnet availability
   ↓
3. Algorithm finds first available IP
   ↓
4. IP record created with status=FREE
   ↓
5. Audit log entry created
   ↓
6. Response returned to frontend
```

### Authentication Flow

```
1. User submits credentials
   ↓
2. Backend validates against database
   ↓
3. Password verified with bcrypt
   ↓
4. JWT access + refresh tokens generated
   ↓
5. Tokens returned to frontend
   ↓
6. Frontend stores tokens in localStorage
   ↓
7. Subsequent requests include Bearer token
   ↓
8. Backend validates token on each request
```

### Conflict Detection Flow

```
1. Scanner agent pings IP
   ↓
2. Discovers device at IP
   ↓
3. Checks if IP is assigned to different device
   ↓
4. If conflict: marks IP as quarantined
   ↓
5. Creates audit log entry
   ↓
6. (Optional) Sends notification
   ↓
7. Network engineer resolves via UI
```

## Security Architecture

### Authentication & Authorization

- **Password Storage**: bcrypt hashing (12 rounds)
- **JWT Tokens**:
  - Access token: 15 minutes expiry
  - Refresh token: 7 days expiry
- **RBAC Roles**:
  - Admin: Full access
  - Network Engineer: Manage subnets, IPs, devices
  - Auditor: Read-only + audit logs
  - Read-only: View only

### Network Security

- **HTTPS**: TLS 1.3 (production)
- **CORS**: Configured allowed origins
- **Rate Limiting**: 100 req/min per IP
- **Security Headers**:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Strict-Transport-Security
  - X-XSS-Protection

### Data Security

- **SQL Injection**: Prevented by SQLAlchemy ORM
- **XSS**: React auto-escaping
- **CSRF**: Token-based authentication
- **Secrets**: AWS Secrets Manager / Kubernetes Secrets

## Deployment Architecture

### Development (Docker Compose)

```
docker-compose.yml
├── postgres (persistent volume)
├── redis (persistent volume)
├── backend (hot reload)
├── frontend (hot reload)
├── scanner (mock mode)
├── prometheus
└── grafana
```

### Production (AWS + Kubernetes)

```
AWS Infrastructure (Terraform)
├── VPC
│   ├── Public Subnets (ALB)
│   └── Private Subnets (ECS/EKS, RDS)
├── RDS PostgreSQL (Multi-AZ)
├── ElastiCache Redis
├── ECS/EKS Cluster
├── ECR (Docker Registry)
├── ALB (Load Balancer)
├── Secrets Manager
└── CloudWatch (Logs & Metrics)

Kubernetes (Helm)
├── Backend Deployment (2+ replicas)
├── Frontend Deployment (2+ replicas)
├── Scanner CronJob
├── Services (ClusterIP)
├── Ingress (NGINX)
├── HPA (Auto-scaling)
└── ConfigMaps & Secrets
```

## Scalability

### Horizontal Scaling

- **Backend**: Stateless, scales to N replicas
- **Frontend**: Static assets, CDN-ready
- **Database**: Read replicas for reporting
- **Redis**: Cluster mode for high availability

### Vertical Scaling

- **Database**: RDS instance class upgrade
- **Backend**: Increase pod resources
- **Redis**: Increase memory allocation

### Performance Optimizations

- **Database Indexes**: On frequently queried fields
- **Connection Pooling**: SQLAlchemy pool (10-20 connections)
- **Caching**: Redis for session data
- **Pagination**: All list endpoints
- **Lazy Loading**: Frontend components

## High Availability

### Database

- **RDS Multi-AZ**: Automatic failover
- **Automated Backups**: 7-day retention
- **Point-in-time Recovery**: Up to 35 days

### Application

- **Multiple Replicas**: 2+ pods per service
- **Health Checks**: Liveness & readiness probes
- **Auto-restart**: Kubernetes self-healing
- **Load Balancing**: ALB distributes traffic

### Disaster Recovery

- **RTO**: < 1 hour (Recovery Time Objective)
- **RPO**: < 15 minutes (Recovery Point Objective)
- **Backup Strategy**:
  - Automated RDS snapshots
  - Manual backups to S3
  - Infrastructure as Code (Terraform)

## Monitoring & Observability

### Metrics (Prometheus)

- API request rate & latency
- Database query performance
- IP utilization percentage
- Conflict detection rate
- Error rates by endpoint

### Logs (Structured JSON)

- Application logs (stdout)
- Access logs (ALB)
- Database logs (RDS)
- Audit logs (database table)

### Alerts (Grafana)

- High error rate (> 5%)
- Low IP availability (< 10%)
- Database connection issues
- High response time (> 1s)
- Conflict spike

### Dashboards

- **Overview**: System health, request rates
- **IP Utilization**: Per subnet, trending
- **Performance**: Response times, throughput
- **Audit**: User actions, changes over time

## Technology Choices Justification

### Why FastAPI?

- Native async support
- Automatic OpenAPI documentation
- Type hints with Pydantic
- High performance (comparable to Node.js)
- Python's ipaddress library for IP operations

### Why PostgreSQL?

- Native INET/CIDR types
- JSONB for flexible metadata
- Strong ACID guarantees
- Excellent performance
- Wide cloud provider support

### Why React?

- Component reusability
- Large ecosystem
- TypeScript support
- Performance (Virtual DOM)
- Industry standard

### Why Kubernetes?

- Container orchestration
- Auto-scaling
- Self-healing
- Rolling updates
- Cloud-agnostic

## Future Enhancements

- [ ] LDAP/SSO integration (Okta, Keycloak)
- [ ] DHCP/DNS live sync
- [ ] Multi-tenancy support
- [ ] GraphQL API
- [ ] Mobile app
- [ ] Advanced reporting
- [ ] Network topology visualization
- [ ] Automated compliance checks
- [ ] Integration with network devices (SNMP)
- [ ] Machine learning for capacity planning
