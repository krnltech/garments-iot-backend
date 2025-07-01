# Garments IoT Backend API Documentation

## Overview
The Garments IoT Backend API provides a comprehensive RESTful interface for managing IoT-integrated garments production tracking with OAuth2 authentication. The API includes endpoints for user management, machine monitoring, worker tracking, target management, and real-time status monitoring.

**Base URL:** `http://localhost:8000`
**Authentication:** Bearer Token (JWT)
**Content Type:** `application/json`

## Table of Contents
1. [Authentication](#authentication)
2. [Health Check](#health-check)
3. [User Management](#user-management)
4. [Machine Management](#machine-management)
5. [Worker Management](#worker-management)
6. [Machine Targets](#machine-targets)
7. [Worker Targets](#worker-targets)
8. [Status Monitoring](#status-monitoring)
9. [Dashboard](#dashboard)
10. [Admin Endpoints](#admin-endpoints)
11. [Error Responses](#error-responses)
12. [Data Models](#data-models)

---

## Authentication

### Register User
**POST** `/auth/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "string (3-50 chars)",
  "email": "string (valid email)",
  "full_name": "string (1-100 chars)",
  "password": "string (min 6 chars)"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-07-01T10:30:00"
}
```

### Login
**POST** `/auth/login`

Authenticate user and get access token.

**Request Body:** `application/x-www-form-urlencoded`
```
username=john_doe
password=secret123
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2025-07-01T10:30:00"
  }
}
```

### Get Current User
**GET** `/auth/me`

Get current authenticated user information.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2025-07-01T10:30:00"
}
```

---

## Health Check

### Health Status
**GET** `/health`

Check API health status.

**Response:** `200 OK`
```json
{
  "status": "healthy",
  "timestamp": "2025-07-01T10:30:00"
}
```

---

## Machine Management

### Get All Machines
**GET** `/machines`

Retrieve all machines.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "label": "MACHINE001",
    "location": "Floor A"
  },
  {
    "id": 2,
    "label": "MACHINE002",
    "location": "Floor B"
  }
]
```

### Get Machines with Targets
**GET** `/machines-with-targets`

Retrieve all machines with their associated targets.

**Headers:** `Authorization: Bearer <token>`
**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "label": "MACHINE001",
    "location": "Floor A",
    "machine_target": {
      "id_machine": 1,
      "target": 100
    }
  },
  {
    "id": 2,
    "label": "MACHINE002",
    "location": "Floor B",
    "machine_target": null
  }
]
```

---

## Worker Management

### Get All Workers
**GET** `/workers`

Retrieve all workers.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "designation": "Operator"
  },
  {
    "id": 2,
    "name": "Bob Smith",
    "designation": "Supervisor"
  }
]
```

### Get Workers with Targets
**GET** `/workers-with-targets`

Retrieve all workers with their associated targets.

**Headers:** `Authorization: Bearer <token>`
**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Alice Johnson",
    "designation": "Operator",
    "worker_target": {
      "id_worker": 1,
      "target": 50
    }
  },
  {
    "id": 2,
    "name": "Bob Smith",
    "designation": "Supervisor",
    "worker_target": null
  }
]
```

---

## Machine Targets

### Get All Machine Targets
**GET** `/machine-targets`

Retrieve all machine targets.

**Headers:** `Authorization: Bearer <token>`
**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id_machine": 1,
    "target": 100,
    "machine": {
      "id": 1,
      "label": "MACHINE001",
      "location": "Floor A"
    }
  }
]
```

### Get Machine Target by ID
**GET** `/machine-targets/{machine_id}`

Retrieve a specific machine target.

**Headers:** `Authorization: Bearer <token>`
**Path Parameters:**
- `machine_id`: Integer - Machine ID

**Response:** `200 OK`
```json
{
  "id_machine": 1,
  "target": 100,
  "machine": {
    "id": 1,
    "label": "MACHINE001",
    "location": "Floor A"
  }
}
```

### Create Machine Target
**POST** `/machine-targets`

Create a new machine target.

**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "id_machine": 1,
  "target": 100
}
```

**Response:** `201 Created`
```json
{
  "id_machine": 1,
  "target": 100,
  "machine": {
    "id": 1,
    "label": "MACHINE001",
    "location": "Floor A"
  }
}
```

### Update Machine Target
**PUT** `/machine-targets/{machine_id}`

Update an existing machine target. Set target to 0 to delete.

**Headers:** `Authorization: Bearer <token>`
**Path Parameters:**
- `machine_id`: Integer - Machine ID

**Request Body:**
```json
{
  "target": 120
}
```

**Response:** `200 OK`
```json
{
  "id_machine": 1,
  "target": 120,
  "machine": {
    "id": 1,
    "label": "MACHINE001",
    "location": "Floor A"
  }
}
```

### Delete Machine Target
**DELETE** `/machine-targets/{machine_id}`

Delete a machine target.

**Headers:** `Authorization: Bearer <token>`
**Path Parameters:**
- `machine_id`: Integer - Machine ID

**Response:** `200 OK`
```json
{
  "message": "Machine target deleted successfully"
}
```

---

## Worker Targets

### Get All Worker Targets
**GET** `/worker-targets`

Retrieve all worker targets.

**Headers:** `Authorization: Bearer <token>`
**Query Parameters:**
- `skip` (optional): Number of records to skip (default: 0)
- `limit` (optional): Maximum number of records (default: 100)

**Response:** `200 OK`
```json
[
  {
    "id_worker": 1,
    "target": 50,
    "worker": {
      "id": 1,
      "name": "Alice Johnson",
      "designation": "Operator"
    }
  }
]
```

### Get Worker Target by ID
**GET** `/worker-targets/{worker_id}`

Retrieve a specific worker target.

**Headers:** `Authorization: Bearer <token>`
**Path Parameters:**
- `worker_id`: Integer - Worker ID

**Response:** `200 OK`
```json
{
  "id_worker": 1,
  "target": 50,
  "worker": {
    "id": 1,
    "name": "Alice Johnson",
    "designation": "Operator"
  }
}
```

### Create Worker Target
**POST** `/worker-targets`

Create a new worker target.

**Headers:** `Authorization: Bearer <token>`
**Request Body:**
```json
{
  "id_worker": 1,
  "target": 50
}
```

**Response:** `201 Created`
```json
{
  "id_worker": 1,
  "target": 50,
  "worker": {
    "id": 1,
    "name": "Alice Johnson",
    "designation": "Operator"
  }
}
```

### Update Worker Target
**PUT** `/worker-targets/{worker_id}`

Update an existing worker target. Set target to 0 to delete.

**Headers:** `Authorization: Bearer <token>`
**Path Parameters:**
- `worker_id`: Integer - Worker ID

**Request Body:**
```json
{
  "target": 60
}
```

**Response:** `200 OK`
```json
{
  "id_worker": 1,
  "target": 60,
  "worker": {
    "id": 1,
    "name": "Alice Johnson",
    "designation": "Operator"
  }
}
```

### Delete Worker Target
**DELETE** `/worker-targets/{worker_id}`

Delete a worker target.

**Headers:** `Authorization: Bearer <token>`
**Path Parameters:**
- `worker_id`: Integer - Worker ID

**Response:** `200 OK`
```json
{
  "message": "Worker target deleted successfully"
}
```

---

## Status Monitoring

### Get Machine Status
**GET** `/machine-status`

Get real-time machine status with bundle analysis for today.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "machine_id": "MACHINE001",
    "bundle_count": 45,
    "bundles_per_minute": 1.25,
    "last_bundle_time_seconds": 180.0
  },
  {
    "machine_id": "MACHINE002",
    "bundle_count": 12,
    "bundles_per_minute": 0.8,
    "last_bundle_time_seconds": 900.0
  }
]
```

### Get Worker Status
**GET** `/worker-status`

Get real-time worker status with bundle analysis for today.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
[
  {
    "employee_id": "EMP001",
    "bundle_count": 32,
    "bundles_per_minute": 1.1,
    "last_bundle_time_seconds": 240.0
  },
  {
    "employee_id": "EMP002",
    "bundle_count": 18,
    "bundles_per_minute": 0.9,
    "last_bundle_time_seconds": 600.0
  }
]
```

---

## Dashboard

### Get Dashboard Summary
**GET** `/dashboard/summary`

Get dashboard summary statistics.

**Headers:** `Authorization: Bearer <token>`

**Response:** `200 OK`
```json
{
  "total_bundles_today": 156,
  "total_machines": 10,
  "total_workers": 25,
  "timestamp": "2025-07-01T10:30:00",
  "user": "john_doe"
}
```

---

## Admin Endpoints

### Get All Users (Admin Only)
**GET** `/admin/users`

Retrieve all users (admin access required).

**Headers:** `Authorization: Bearer <admin_token>`

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "is_active": true,
    "is_admin": false,
    "created_at": "2025-07-01T10:30:00"
  },
  {
    "id": 2,
    "username": "admin",
    "email": "admin@example.com",
    "full_name": "Administrator",
    "is_active": true,
    "is_admin": true,
    "created_at": "2025-07-01T09:00:00"
  }
]
```

---

## Error Responses

### Standard Error Format
All error responses follow this format:

```json
{
  "detail": "Error message description"
}
```

### Common HTTP Status Codes

- **200 OK** - Request successful
- **201 Created** - Resource created successfully
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Authentication required or invalid token
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **422 Unprocessable Entity** - Validation error
- **500 Internal Server Error** - Server error

### Example Error Responses

**400 Bad Request**
```json
{
  "detail": "Username already registered"
}
```

**401 Unauthorized**
```json
{
  "detail": "Could not validate credentials"
}
```

**403 Forbidden**
```json
{
  "detail": "Not enough permissions"
}
```

**404 Not Found**
```json
{
  "detail": "Machine target not found"
}
```

**422 Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Data Models

### User
```json
{
  "id": "integer",
  "username": "string (3-50 chars)",
  "email": "string (valid email)",
  "full_name": "string (1-100 chars)",
  "is_active": "boolean",
  "is_admin": "boolean",
  "created_at": "datetime"
}
```

### Machine
```json
{
  "id": "integer",
  "label": "string",
  "location": "string"
}
```

### Worker
```json
{
  "id": "integer",
  "name": "string",
  "designation": "string"
}
```

### Machine Target
```json
{
  "id_machine": "integer",
  "target": "integer (>= 0)",
  "machine": "Machine object (optional)"
}
```

### Worker Target
```json
{
  "id_worker": "integer",
  "target": "integer (>= 0)",
  "worker": "Worker object (optional)"
}
```

### Machine Status
```json
{
  "machine_id": "string",
  "bundle_count": "integer",
  "bundles_per_minute": "float (nullable)",
  "last_bundle_time_seconds": "float (nullable)"
}
```

### Worker Status
```json
{
  "employee_id": "string",
  "bundle_count": "integer",
  "bundles_per_minute": "float (nullable)",
  "last_bundle_time_seconds": "float (nullable)"
}
```

### Token
```json
{
  "access_token": "string (JWT)",
  "token_type": "string (bearer)",
  "user": "User object"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting based on your requirements.

---

## CORS Configuration

The API is configured to allow all origins in development. For production, update the CORS configuration to only allow trusted origins.

---

## Security Considerations

1. **JWT Tokens**: Tokens expire after 30 minutes
2. **Password Hashing**: Uses bcrypt for secure password storage
3. **Authentication**: All protected endpoints require valid JWT token
4. **Authorization**: Admin endpoints require admin privileges
5. **Input Validation**: All inputs are validated using Pydantic models

---

## Development Setup

1. **Start the API server:**
   ```bash
   cd garments-iot-backend
   python apps/api/main.py
   ```

2. **API will be available at:** `http://localhost:8000`

3. **Interactive API documentation:** `http://localhost:8000/docs`

4. **OpenAPI JSON schema:** `http://localhost:8000/openapi.json`

---

## Testing

Use the provided test scripts to verify API functionality:

```bash
# Test machine targets
python test_machine_targets.py

# Test worker targets
python test_worker_targets.py

# Test enhanced features
python test_enhanced_features.py
```

---

**Last Updated:** July 1, 2025
**API Version:** 1.0.0
