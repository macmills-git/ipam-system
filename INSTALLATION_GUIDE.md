# IPAM System - Installation Guide for Windows

## Prerequisites

Before running the IPAM system, you need to install Docker Desktop.

## Step 1: Install Docker Desktop

1. **Download Docker Desktop**

   - Visit: https://www.docker.com/products/docker-desktop/
   - Click "Download for Windows"
   - Run the installer (Docker Desktop Installer.exe)

2. **Installation Steps**

   - Accept the license agreement
   - Use WSL 2 instead of Hyper-V (recommended)
   - Complete the installation
   - **Restart your computer**

3. **Verify Installation**
   ```powershell
   docker --version
   docker compose version
   ```

## Step 2: Start the IPAM Application

1. **Open PowerShell or Command Prompt**

   - Press `Win + X` and select "Windows PowerShell" or "Terminal"

2. **Navigate to the project directory**

   ```powershell
   cd C:\path\to\ipam-system
   ```

3. **Start all services**

   ```powershell
   docker compose up --build
   ```

   This will:

   - Build the Docker images (first time takes 5-10 minutes)
   - Start PostgreSQL database
   - Start Redis cache
   - Start the backend API
   - Start the frontend React app
   - Start Prometheus and Grafana for monitoring
   - Run database migrations
   - Seed sample data

4. **Wait for services to start**
   - Look for messages like:
     - "backend-1 | INFO: Application startup complete"
     - "frontend-1 | webpack compiled successfully"

## Step 3: Access the Application

Once all services are running, open your web browser:

### Main Application

- **URL**: http://localhost:3000
- **Default Login**:
  - Email: `admin@ipam.local`
  - Password: `Admin123!`

### API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Monitoring

- **Grafana**: http://localhost:3001
  - Username: `admin`
  - Password: `admin`
- **Prometheus**: http://localhost:9090

## Step 4: Explore the Application

### Dashboard

After logging in, you'll see:

- **Total Subnets** - Count of all network subnets
- **Free IPs** - Available IP addresses
- **Assigned IPs** - IPs currently in use
- **Quarantined IPs** - IPs with conflicts
- **IP Status Distribution** - Pie chart showing IP allocation
- **Recent Subnets** - List of recently created subnets

### Navigation Menu

- **Dashboard** - Overview and statistics
- **Subnets** - Manage network subnets
- **IP Addresses** - View and allocate IPs
- **Devices** - Manage network devices
- **VLANs** - VLAN configuration
- **Audit Logs** - View all system changes (Admin/Auditor only)
- **Users** - User management (Admin only)

### Try These Actions

1. **Create a Subnet**

   - Click "Subnets" in the navigation
   - Click "Add Subnet"
   - Enter CIDR: `192.168.1.0/24`
   - Enter Description: "Test Network"
   - Click "Create Subnet"

2. **Allocate IP Addresses**

   - Click "IP Addresses"
   - Click "Allocate IP"
   - Enter Subnet ID: 1
   - Click "Allocate"

3. **View API Documentation**

   - Open http://localhost:8000/docs
   - Try the interactive API endpoints
   - Click "Authorize" and enter your JWT token

4. **Check Monitoring**
   - Open http://localhost:3001
   - Login with admin/admin
   - View the IPAM dashboard

## Step 5: Stop the Application

When you're done:

```powershell
# Stop all services (keeps data)
docker compose down

# Stop and remove all data
docker compose down -v
```

## Troubleshooting

### Port Already in Use

If you see "port is already allocated":

```powershell
# Check what's using the port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Docker Not Starting

- Make sure Docker Desktop is running (check system tray)
- Restart Docker Desktop
- Check Docker Desktop settings → Resources

### Services Not Starting

```powershell
# View logs
docker compose logs backend
docker compose logs frontend

# Restart a specific service
docker compose restart backend
```

### Database Connection Issues

```powershell
# Check if PostgreSQL is running
docker compose ps

# View database logs
docker compose logs postgres

# Restart database
docker compose restart postgres
```

### Frontend Can't Reach Backend

- Check that backend is running: http://localhost:8000/health
- Check CORS settings in `.env`
- Restart backend: `docker compose restart backend`

## Alternative: Run Without Docker

If you can't use Docker, you can run services individually:

### Backend (Requires Python 3.11+)

```powershell
cd backend
pip install -r requirements.txt

# Install and start PostgreSQL separately
# Update DATABASE_URL in .env

alembic upgrade head
python scripts/seed_data.py
uvicorn app.main:app --reload
```

### Frontend (Requires Node.js 18+)

```powershell
cd frontend
npm install
npm start
```

## Next Steps

1. **Read the Documentation**

   - [QUICKSTART_GUIDE.md](QUICKSTART_GUIDE.md) - Quick overview
   - [docs/API.md](docs/API.md) - API reference
   - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design

2. **Import Sample Data**

   - Use the CSV files in `sample-data/`
   - Go to the UI and use the import feature

3. **Explore the API**

   - Open http://localhost:8000/docs
   - Import `docs/postman_collection.json` into Postman

4. **Run Tests**

   ```powershell
   cd backend
   pytest --cov=app --cov-report=html
   ```

5. **Deploy to Production**
   - Follow [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)
   - Use Terraform for AWS infrastructure
   - Use Helm for Kubernetes deployment

## Support

If you encounter issues:

1. Check the logs: `docker compose logs`
2. Review [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) troubleshooting section
3. Check that all ports are available (3000, 8000, 5432, 6379)
4. Ensure Docker Desktop has enough resources (4GB+ RAM recommended)

## What You'll See

### Login Screen

- Clean, modern interface
- Email and password fields
- Demo credentials displayed

### Dashboard

- 4 stat cards showing key metrics
- Pie chart for IP status distribution
- List of recent subnets
- Responsive design

### Subnet Management

- Table view of all subnets
- Add/Edit/Delete functionality
- CIDR validation
- Location and description fields

### IP Address Management

- Filterable table of IPs
- Status badges (Free, Assigned, Reserved, Quarantined)
- Bulk allocation
- Device assignment

### Monitoring (Grafana)

- Pre-configured dashboards
- Real-time metrics
- API performance graphs
- IP utilization trends

---

**Enjoy your IPAM system!** 🎉

For questions or issues, refer to the comprehensive documentation in the `docs/` folder.
