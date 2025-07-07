# Tests

This folder contains all test files for the Garments IoT Backend system.

## Test Files

### 🧪 Backend API Tests
- **[test_backend.py](test_backend.py)** - Core backend API functionality tests
- **[test_enhanced_features.py](test_enhanced_features.py)** - Enhanced features and advanced functionality tests
- **[test_machine_targets.py](test_machine_targets.py)** - Machine targets CRUD operations tests
- **[test_worker_targets.py](test_worker_targets.py)** - Worker targets CRUD operations tests

## Running Tests

### Run All Tests
```bash
# From project root
python -m pytest tests/

# Or run individual test files
python tests/test_backend.py
python tests/test_machine_targets.py
python tests/test_worker_targets.py
python tests/test_enhanced_features.py
```

### Test Prerequisites

Before running tests, ensure:

1. **API Server is Running**
   ```bash
   python apps/api/main.py
   ```

2. **Database is Set Up**
   ```bash
   python seeders/seed_database.py
   python seeders/add_sample_data.py
   ```

3. **Valid User Account Exists**
   - Tests will attempt to register and login
   - Or use existing credentials in test files

## Test Coverage

### Authentication Tests
- User registration
- User login
- Token validation
- Protected endpoint access

### Machine Management Tests
- Get all machines
- Machine targets CRUD operations
- Machine status monitoring
- Error handling

### Worker Management Tests
- Get all workers
- Worker targets CRUD operations
- Worker status monitoring
- Error handling

### Integration Tests
- End-to-end API workflows
- Database interactions
- Real-time monitoring features

## Test Configuration

### Environment Setup
Tests use the same environment as the main application:
- **API Base URL**: `http://localhost:8000`
- **Database**: PostgreSQL with TimescaleDB
- **Authentication**: JWT tokens

### Test Data
- Tests create temporary test data
- Some tests may require sample data from seeders
- Tests should clean up after themselves

## Adding New Tests

When adding new tests:

1. **Follow Naming Convention**: `test_feature_name.py`
2. **Include Setup/Teardown**: Proper test initialization
3. **Test All CRUD Operations**: Create, Read, Update, Delete
4. **Test Error Cases**: Invalid inputs, authentication failures
5. **Document Test Purpose**: Clear test descriptions
6. **Mock External Dependencies**: Where appropriate

### Test Template
```python
import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "testpass123"
}

def test_feature():
    """Test description"""
    # Test implementation
    pass

if __name__ == "__main__":
    # Run individual tests
    test_feature()
    print("All tests passed!")
```

## Test Results

### Expected Output
- ✅ Successful API calls return 200/201 status codes
- ✅ Authentication works correctly
- ✅ CRUD operations function properly
- ✅ Error handling returns appropriate status codes
- ✅ Data validation works as expected

### Common Issues
- **Connection Errors**: Ensure API server is running
- **Authentication Failures**: Check user credentials
- **Database Errors**: Verify database setup and seeders
- **Port Conflicts**: Ensure port 8000 is available

## Continuous Integration

For CI/CD integration:

```bash
# Install dependencies
pip install -r requirements.txt

# Start services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Run database setup
python seeders/seed_database.py

# Run tests
python -m pytest tests/ --verbose

# Cleanup
docker-compose down
```

---

**Last Updated**: July 1, 2025
