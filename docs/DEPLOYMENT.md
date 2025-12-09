# Deployment Guide

## Local Development Deployment

### Prerequisites

- Docker and Docker Compose installed
- Git

### Steps

1. **Clone the repository**

```bash
git clone <repository-url>
cd ipam-system
```

2. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your settings (optional for local dev)
```

3. **Start all services**

```bash
docker-compose up --build
```

4. **Access the application**

- Frontend: http://localhost:3000
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- Grafana: http://localhost:3001 (admin/admin)
- Prometheus: http://localhost:9090

5. **Default credentials**

- Email: `admin@ipam.local`
- Password: `Admin123!`

## AWS Production Deployment

### Prerequisites

- AWS CLI configured with appropriate credentials
- Terraform >= 1.0
- kubectl installed
- Helm >= 3.0
- Docker

### Step 1: Provision Infrastructure with Terraform

```bash
cd infra/terraform

# Initialize Terraform
terraform init

# Review the plan
terraform plan -out=tfplan

# Apply the infrastructure
terraform apply tfplan

# Note the outputs
terraform output
```

This creates:

- VPC with public/private subnets
- RDS PostgreSQL database
- ECS cluster
- ECR repositories
- Application Load Balancer
- Security groups
- Secrets Manager for database password

### Step 2: Build and Push Docker Images

```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Get ECR URLs from Terraform output
BACKEND_REPO=$(terraform output -raw ecr_backend_url)
FRONTEND_REPO=$(terraform output -raw ecr_frontend_url)

# Build and push backend
docker build -f docker/backend.Dockerfile -t $BACKEND_REPO:latest .
docker push $BACKEND_REPO:latest

# Build and push frontend
docker build -f docker/frontend.Dockerfile -t $FRONTEND_REPO:latest .
docker push $FRONTEND_REPO:latest
```

### Step 3: Deploy to Kubernetes (if using EKS)

```bash
# Update kubeconfig
aws eks update-kubeconfig --name ipam-cluster --region us-east-1

# Get database endpoint and password
DB_ENDPOINT=$(terraform output -raw db_endpoint)
DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id ipam-db-password --query SecretString --output text)

# Deploy with Helm
cd ../../infra/helm
helm install ipam ./ipam-chart \
  --set database.host=$DB_ENDPOINT \
  --set database.password=$DB_PASSWORD \
  --set image.backend.repository=$BACKEND_REPO \
  --set image.frontend.repository=$FRONTEND_REPO

# Check deployment status
kubectl get pods
kubectl get services
kubectl get ingress
```

### Step 4: Run Database Migrations

```bash
# Get backend pod name
BACKEND_POD=$(kubectl get pods -l app=ipam-backend -o jsonpath='{.items[0].metadata.name}')

# Run migrations
kubectl exec -it $BACKEND_POD -- alembic upgrade head

# Seed initial data
kubectl exec -it $BACKEND_POD -- python scripts/seed_data.py
```

### Step 5: Configure DNS

```bash
# Get load balancer URL
kubectl get ingress ipam-ingress

# Create DNS record pointing to the load balancer
# Example: ipam.yourdomain.com -> <alb-dns-name>
```

### Step 6: Enable HTTPS (Optional but Recommended)

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Update Helm values to enable TLS
helm upgrade ipam ./ipam-chart \
  --set ingress.tls[0].secretName=ipam-tls \
  --set ingress.tls[0].hosts[0]=ipam.yourdomain.com
```

## Alternative: Docker Compose Production Deployment

For simpler deployments without Kubernetes:

```bash
# On your production server
git clone <repository-url>
cd ipam-system

# Configure production environment
cp .env.example .env
nano .env  # Update with production values

# Use production docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Run migrations
docker-compose exec backend alembic upgrade head
docker-compose exec backend python scripts/seed_data.py
```

## Post-Deployment Checklist

- [ ] Change default admin password
- [ ] Configure email settings for notifications
- [ ] Set up automated backups
- [ ] Configure monitoring alerts
- [ ] Review security group rules
- [ ] Enable CloudWatch logs
- [ ] Test disaster recovery procedure
- [ ] Document custom configurations
- [ ] Set up CI/CD pipeline
- [ ] Configure scanner agent on-premises

## Monitoring

### Access Grafana

```bash
# Port forward to Grafana
kubectl port-forward svc/grafana 3000:3000

# Access at http://localhost:3000
# Default: admin/admin
```

### View Logs

```bash
# Backend logs
kubectl logs -f deployment/ipam-backend

# Frontend logs
kubectl logs -f deployment/ipam-frontend

# Or use CloudWatch Logs in AWS Console
```

## Backup and Restore

### Backup Database

```bash
# Get RDS endpoint
DB_ENDPOINT=$(terraform output -raw db_endpoint)

# Create backup
pg_dump -h $DB_ENDPOINT -U ipam ipam > backup_$(date +%Y%m%d).sql

# Or use AWS RDS automated backups (configured in Terraform)
```

### Restore Database

```bash
psql -h $DB_ENDPOINT -U ipam ipam < backup_20240101.sql
```

## Scaling

### Horizontal Scaling

```bash
# Scale backend pods
kubectl scale deployment ipam-backend --replicas=5

# Or use HPA (configured in Helm chart)
kubectl get hpa
```

### Vertical Scaling

```bash
# Update RDS instance class in Terraform
# Edit variables.tf: db_instance_class = "db.t3.medium"
terraform apply
```

## Troubleshooting

### Database Connection Issues

```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:15 --restart=Never -- psql -h $DB_ENDPOINT -U ipam

# Check security groups
aws ec2 describe-security-groups --group-ids <sg-id>
```

### Application Not Starting

```bash
# Check pod status
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Check environment variables
kubectl exec <pod-name> -- env
```

### Performance Issues

```bash
# Check resource usage
kubectl top pods
kubectl top nodes

# Review Prometheus metrics
kubectl port-forward svc/prometheus 9090:9090
# Access http://localhost:9090
```

## Rollback

### Rollback Helm Deployment

```bash
# List releases
helm history ipam

# Rollback to previous version
helm rollback ipam <revision-number>
```

### Rollback Terraform Changes

```bash
# Revert to previous state
terraform state pull > backup.tfstate
terraform apply -target=<resource>
```

## Security Hardening

1. **Enable AWS WAF** on ALB
2. **Configure VPC Flow Logs**
3. **Enable GuardDuty**
4. **Use AWS Secrets Manager** for all secrets
5. **Enable MFA** for admin users
6. **Regular security audits** with AWS Security Hub
7. **Implement least privilege** IAM policies
8. **Enable encryption at rest** for RDS and EBS

## Cost Optimization

- Use RDS Reserved Instances for production
- Enable ECS Fargate Spot for non-critical workloads
- Configure S3 lifecycle policies for backups
- Use CloudWatch Logs retention policies
- Right-size EC2 instances based on metrics

## Support

For issues or questions:

- Check logs: `kubectl logs <pod-name>`
- Review documentation in `/docs`
- Check GitHub Issues
- Contact: support@example.com
