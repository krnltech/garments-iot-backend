# Garments IoT Backend

A comprehensive IoT-integrated garments production tracking system with real-time monitoring, user management, and performance analytics.

## Project Structure

```
garments-iot-backend/
├── apps/                           # Application modules
│   ├── api/                        # FastAPI application
│   │   ├── app/                    # Modular API structure (if using)
│   │   └── main.py                 # Main FastAPI application
│   ├── edge-devices/              # Edge device code
│   ├── event_worker/              # Event processing worker
│   └── mqtt_gateway/              # MQTT gateway service
├── config/                        # Configuration files
│   └── mosquitto/                 # MQTT broker configuration
├── docs/                          # Documentation
│   ├── API_DOCUMENTATION.md       # Complete API documentation
│   ├── README.md                  # Original project README
│   └── WORKER_TARGETS_IMPLEMENTATION.md  # Implementation details
├── seeders/                       # Database seeders
│   ├── add_sample_bundle_data.py  # Bundle data seeder
│   ├── add_sample_data.py         # General sample data
│   └── seed_database.py           # Database initialization
├── tests/                         # Test files
│   ├── test_backend.py            # Backend API tests
│   ├── test_enhanced_features.py  # Enhanced features tests
│   ├── test_machine_targets.py    # Machine targets tests
│   └── test_worker_targets.py     # Worker targets tests
├── docker-compose.yaml            # Docker services configuration
├── init.sql                       # Database initialization script
├── poetry.lock                    # Python dependencies lock file
├── pyproject.toml                 # Python project configuration
└── publisher.py                   # MQTT publisher utility
```

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL with TimescaleDB extension
- Docker (optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd garments-iot-backend
   ```

2. **Install dependencies**
   ```bash
   poetry install
   # or
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   # Start services with Docker
   docker-compose up -d
   
   # Initialize database
   python seeders/seed_database.py
   
   # Add sample data
   python seeders/add_sample_data.py
   python seeders/add_sample_bundle_data.py
   ```

4. **Start the API server**
   ```bash
   python apps/api/main.py
   ```

5. **Access the application**
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - API Schema: http://localhost:8000/openapi.json

## Features

### Core Functionality
- **User Authentication**: JWT-based authentication with role management
- **Machine Management**: CRUD operations for production machines
- **Worker Management**: CRUD operations for factory workers
- **Target Management**: Performance targets for machines and workers
- **Real-time Monitoring**: Live status tracking with bundle analysis
- **Dashboard**: Summary statistics and analytics

### API Endpoints
- **Authentication**: `/auth/*` - User registration, login, profile
- **Machines**: `/machines*` - Machine CRUD and status monitoring
- **Workers**: `/workers*` - Worker CRUD and status monitoring
- **Targets**: `/machine-targets*`, `/worker-targets*` - Target management
- **Status**: `/machine-status`, `/worker-status` - Real-time monitoring
- **Dashboard**: `/dashboard/summary` - Analytics dashboard
- **Admin**: `/admin/*` - Administrative functions

### Real-time Features
- Machine status monitoring with production rates
- Worker productivity tracking
- Bundle analysis with timing metrics
- Auto-refreshing status indicators
- Performance analytics

## Documentation

- **[Complete API Documentation](docs/API_DOCUMENTATION.md)** - Detailed API reference
- **[Worker Targets Implementation](docs/WORKER_TARGETS_IMPLEMENTATION.md)** - Implementation details
- **[Original README](docs/README.md)** - Original project documentation

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific test files
python tests/test_backend.py
python tests/test_machine_targets.py
python tests/test_worker_targets.py
python tests/test_enhanced_features.py
```

## Database Schema

The system uses PostgreSQL with TimescaleDB for time-series data:

- **users** - User accounts and authentication
- **machine** - Production machines
- **worker** - Factory workers
- **machine_target** - Performance targets for machines
- **worker_target** - Performance targets for workers
- **bundle** - Production records (time-series)
- **worker_scan** - Worker activity tracking (time-series)

## Architecture

### Backend Services
- **FastAPI Application** - Main REST API server
- **PostgreSQL + TimescaleDB** - Primary database
- **MQTT Gateway** - IoT device communication
- **Event Worker** - Background processing

### Security
- JWT authentication with 30-minute expiration
- BCrypt password hashing
- Role-based access control (admin/user)
- Input validation with Pydantic
- CORS configuration for cross-origin requests

## Development

### Code Structure
- **Modular Design** - Separated concerns with clear boundaries
- **Type Safety** - Full type hints with Pydantic models
- **Error Handling** - Comprehensive error responses
- **Logging** - Structured logging throughout
- **Testing** - Unit tests for all major functionality

### Adding New Features
1. Update database schema in `init.sql`
2. Add/update models in `apps/api/main.py`
3. Implement CRUD operations
4. Add API endpoints
5. Write tests in `tests/`
6. Update documentation

## Deployment

### Production Considerations
- Update CORS origins for production domains
- Configure proper environment variables
- Set up SSL/TLS certificates
- Implement rate limiting
- Configure logging and monitoring
- Set up database backups

### Environment Variables
```bash
SECRET_KEY=your-secret-key-here
TIMESCALE_USER=postgres
TIMESCALE_PASSWORD=password
TIMESCALE_HOST=localhost
TIMESCALE_DB=metrics
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Update documentation
6. Submit a pull request

## License

[Add your license information here]

## Support

For questions and support, please refer to the documentation in the `docs/` folder or contact the development team.
