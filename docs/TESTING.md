# Testing Guide

## Overview

The IPAM system includes comprehensive testing at multiple levels:

- Unit tests (backend)
- Integration tests (API)
- Frontend tests (React components)
- End-to-end tests (user flows)

## Backend Testing

### Setup Test Environment

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Install test dependencies
pip install pytest pytest-cov pytest-asyncio faker
```

### Run All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_login

# Run with verbose output
pytest -v

# Run and stop on first failure
pytest -x
```

### Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_api.py           # API endpoint tests
├── test_auth.py          # Authentication tests
├── test_subnets.py       # Subnet logic tests
├── test_ip_service.py    # IP allocation tests
└── test_security.py      # Security tests
```

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient

def test_create_subnet(client, auth_headers):
    response = client.post(
        "/api/v1/subnets",
        json={
            "cidr": "10.0.0.0/24",
            "description": "Test subnet"
        },
        headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json()["cidr"] == "10.0.0.0/24"
```

## Frontend Testing

### Setup

```bash
cd frontend

# Install dependencies
npm install

# Install test dependencies (already in package.json)
npm install --save-dev @testing-library/react @testing-library/jest-dom
```

### Run Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch

# Run specific test file
npm test -- Login.test.tsx
```

### Test Structure

```
frontend/src/
├── components/
│   └── __tests__/
│       └── Layout.test.tsx
├── pages/
│   └── __tests__/
│       ├── Login.test.tsx
│       └── Dashboard.test.tsx
└── services/
    └── __tests__/
        └── api.test.ts
```

### Writing Component Tests

```typescript
import { render, screen, fireEvent } from "@testing-library/react";
import Login from "../Login";

test("renders login form", () => {
  render(<Login />);
  expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
});

test("submits login form", async () => {
  render(<Login />);

  fireEvent.change(screen.getByLabelText(/email/i), {
    target: { value: "test@example.com" },
  });
  fireEvent.change(screen.getByLabelText(/password/i), {
    target: { value: "password123" },
  });

  fireEvent.click(screen.getByRole("button", { name: /login/i }));

  // Assert expected behavior
});
```

## Integration Testing

### API Integration Tests

```bash
# Start test database
docker-compose up -d postgres redis

# Run integration tests
cd backend
pytest tests/integration/
```

### Test Scenarios

1. **Complete User Flow**

```python
def test_complete_ip_allocation_flow(client, auth_headers):
    # 1. Create subnet
    subnet_response = client.post("/api/v1/subnets", ...)
    subnet_id = subnet_response.json()["id"]

    # 2. Allocate IP
    ip_response = client.post("/api/v1/ips/allocate", ...)
    ip_id = ip_response.json()[0]["id"]

    # 3. Create device
    device_response = client.post("/api/v1/devices", ...)
    device_id = device_response.json()["id"]

    # 4. Assign IP to device
    assign_response = client.put(f"/api/v1/ips/{ip_id}/assign", ...)

    # 5. Verify assignment
    assert assign_response.json()["assigned_to_id"] == device_id
```

2. **Conflict Detection**

```python
def test_conflict_detection(client, auth_headers):
    # Create two devices with same IP
    # Verify conflict is detected
    # Resolve conflict
    # Verify resolution
```

3. **CSV Import/Export**

```python
def test_csv_import_export(client, auth_headers):
    # Export subnets
    # Modify CSV
    # Import modified CSV
    # Verify changes
```

## End-to-End Testing

### Using Playwright (Optional)

```bash
# Install Playwright
npm install -D @playwright/test

# Run E2E tests
npx playwright test
```

### E2E Test Example

```typescript
import { test, expect } from "@playwright/test";

test("complete IP allocation workflow", async ({ page }) => {
  // Login
  await page.goto("http://localhost:3000/login");
  await page.fill('input[type="email"]', "admin@ipam.local");
  await page.fill('input[type="password"]', "Admin123!");
  await page.click('button[type="submit"]');

  // Navigate to subnets
  await page.click("text=Subnets");

  // Create subnet
  await page.click("text=Add Subnet");
  await page.fill('input[placeholder*="CIDR"]', "10.99.0.0/24");
  await page.click("text=Create Subnet");

  // Verify subnet created
  await expect(page.locator("text=10.99.0.0/24")).toBeVisible();
});
```

## Performance Testing

### Load Testing with Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class IPAMUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Login
        response = self.client.post("/api/v1/auth/login", json={
            "email": "admin@ipam.local",
            "password": "Admin123!"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def list_subnets(self):
        self.client.get("/api/v1/subnets", headers=self.headers)

    @task(2)
    def list_ips(self):
        self.client.get("/api/v1/ips", headers=self.headers)

    @task(1)
    def allocate_ip(self):
        self.client.post("/api/v1/ips/allocate",
                        json={"subnet_id": 1, "count": 1},
                        headers=self.headers)
```

Run load test:

```bash
pip install locust
locust -f locustfile.py --host=http://localhost:8000
# Open http://localhost:8089
```

## Security Testing

### SQL Injection Tests

```python
def test_sql_injection_protection(client, auth_headers):
    # Try SQL injection in search
    response = client.get(
        "/api/v1/ips?hostname=' OR '1'='1",
        headers=auth_headers
    )
    # Should not return all records
    assert response.status_code == 200
```

### XSS Tests

```python
def test_xss_protection(client, auth_headers):
    # Try XSS in description
    response = client.post(
        "/api/v1/subnets",
        json={
            "cidr": "10.0.0.0/24",
            "description": "<script>alert('xss')</script>"
        },
        headers=auth_headers
    )
    # Should be escaped
    assert "<script>" not in response.json()["description"]
```

### Authentication Tests

```python
def test_unauthorized_access(client):
    response = client.get("/api/v1/subnets")
    assert response.status_code == 403

def test_expired_token(client):
    # Use expired token
    headers = {"Authorization": "Bearer expired_token"}
    response = client.get("/api/v1/subnets", headers=headers)
    assert response.status_code == 401
```

## Test Data Management

### Fixtures

```python
# conftest.py
import pytest
from app.models.user import User, UserRole

@pytest.fixture
def test_user(db):
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password=get_password_hash("testpass"),
        role=UserRole.ADMIN
    )
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def test_subnet(db, test_user):
    subnet = Subnet(
        cidr="10.0.0.0/24",
        description="Test subnet",
        created_by_id=test_user.id
    )
    db.add(subnet)
    db.commit()
    return subnet
```

### Factory Pattern

```python
# factories.py
from faker import Faker
fake = Faker()

class SubnetFactory:
    @staticmethod
    def create(db, **kwargs):
        subnet = Subnet(
            cidr=kwargs.get('cidr', '10.0.0.0/24'),
            description=kwargs.get('description', fake.text()),
            location=kwargs.get('location', fake.city())
        )
        db.add(subnet)
        db.commit()
        return subnet
```

## Continuous Integration

### GitHub Actions

Tests run automatically on:

- Every push to main/develop
- Every pull request
- Scheduled daily runs

View results:

```bash
# Check workflow status
gh run list

# View specific run
gh run view <run-id>
```

## Test Coverage Goals

- **Overall**: > 70%
- **Critical paths**: > 90%
- **API endpoints**: 100%
- **Security functions**: 100%

## Troubleshooting Tests

### Database Issues

```bash
# Reset test database
docker-compose down -v
docker-compose up -d postgres
cd backend && alembic upgrade head
```

### Port Conflicts

```bash
# Check what's using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>
```

### Flaky Tests

```bash
# Run test multiple times
pytest tests/test_api.py::test_name --count=10

# Run with random order
pytest --random-order
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Fast**: Keep tests fast (< 1s per test)
3. **Descriptive**: Use clear test names
4. **Arrange-Act-Assert**: Follow AAA pattern
5. **Mock External Services**: Don't call real APIs
6. **Clean Up**: Use fixtures for setup/teardown
7. **Test Edge Cases**: Not just happy paths
8. **Keep Tests Simple**: One assertion per test when possible

## Running All Tests

```bash
# Backend tests
cd backend && pytest --cov=app --cov-report=term

# Frontend tests
cd frontend && npm test -- --coverage --watchAll=false

# Integration tests
docker-compose up -d
cd backend && pytest tests/integration/

# Generate combined report
# (requires coverage.py and coverage-badge)
coverage combine
coverage report
coverage html
```

## Test Reports

Test results are available:

- **Local**: `backend/htmlcov/index.html`
- **CI/CD**: GitHub Actions artifacts
- **Coverage**: Codecov dashboard (if configured)
