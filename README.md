# Coffee Shop API - User Management System

A comprehensive user management API built with FastAPI for coffee shop operations, providing authentication, authorization, and user management capabilities.


## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Environment Setup
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   
2. Update the `.env` file with your configuration (database credentials, secret key, etc.)

### Running the Application
Start the application with commands:

```bash
docker compose pull
docker compose build
docker compose run --rm app alembic upgrade head
docker compose up -d
```

This will start:
- **API Server** on `http://localhost:8000`
- **PostgreSQL Database** on `localhost:5432`
- **Background Worker** for scheduled tasks

### API Documentation
Once running, access the interactive API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📋 Features

### Authentication & Authorization
- **JWT-based authentication** with access and refresh tokens
- **User registration** with email verification
- **Role-based access control** (User/Admin)
- **Automatic cleanup** of unverified accounts after 2 days

### User Management
- User profile management
- Admin user administration
- Secure password hashing with bcrypt
- Email verification system

### API Endpoints

#### Authentication (`/auth`)
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login (get tokens)
- `POST /auth/refresh` - Refresh access token
- `POST /auth/verify` - Verify email address

#### Users (`/users`)
- `GET /users/me` - Get current user profile
- `GET /users` - List all users (Admin only)
- `GET /users/{id}` - Get user by ID (Admin only)
- `PATCH /users/{id}` - Update user data
- `DELETE /users/{id}` - Delete user (Admin only)

## 🏗️ Project Architecture

### Directory Structure
```
coffee_shop_api/
├── app/                          # Main application package
│   ├── main.py                   # FastAPI application factory
│   ├── scheduler.py              # Background task scheduler
│   ├── utils.py                  # Utility functions
│   │
│   ├── actors/                   # Background job actors
│   │   └── clear_expired_authorizations.py
│   │
│   ├── alembic/                  # Database migration management
│   │   ├── env.py
│   │   └── versions/
│   │
│   ├── core/                     # Core configuration
│   │   ├── config.py             # Application settings
│   │   ├── database.py           # Database connection
│   │   └── security.py           # Security utilities
│   │
│   ├── exceptions/               # Custom exceptions
│   │   └── __init__.py
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── base.py               # Base model class
│   │   └── user.py               # User model
│   │
│   ├── repositories/             # Data access layer
│   │   └── user.py               # User repository
│   │
│   ├── routers/                  # API route handlers
│   │   ├── auth.py               # Authentication routes
│   │   └── users.py              # User management routes
│   │
│   ├── schemas/                  # Pydantic models for API
│   │   ├── auth.py               # Authentication schemas
│   │   └── user.py               # User schemas
│   │
│   └── services/                 # Business logic layer
│       └── user.py               # User service
│
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── tests/                        # Test suite
├── docker-compose.yml            # Docker services configuration
├── Dockerfile                    # Application container
├── alembic.ini                   # Alembic configuration
└── pyproject.toml                # Project dependencies and configuration
```

### Architecture Pattern: Clean Architecture

The application follows **Clean Architecture** principles with clear separation of concerns:

#### 1. **Presentation Layer** (`routers/`)
- **FastAPI routers** handle HTTP requests/responses
- **Input validation** using Pydantic schemas
- **Authentication/authorization** decorators
- **Error handling** and HTTP status codes

#### 2. **Business Logic Layer** (`services/`)
- **Domain logic** and business rules
- **Service classes** coordinate between repositories and external services
- **Independent of frameworks** and external concerns
- **Testable** without infrastructure dependencies

#### 3. **Data Access Layer** (`repositories/`)
- **Repository pattern** abstracts database operations
- **SQLAlchemy ORM** for database interactions
- **Query optimization** and data mapping
- **Database-agnostic** interface

#### 4. **Infrastructure Layer** (`core/`, `models/`)
- **Database configuration** and connection management
- **Security utilities** (JWT, password hashing)
- **External service integrations**
- **Configuration management**

### Key Architectural Decisions

#### 1. **Dependency Injection**
- Services depend on abstractions (repository interfaces)
- Easy to mock dependencies for testing
- Configurable implementations per environment

#### 2. **Async/Await Pattern**
- **Non-blocking I/O** for better performance
- **SQLAlchemy async** for database operations
- **FastAPI async handlers** for concurrent request handling

#### 3. **Background Task Processing**
- **Scheduled tasks** for maintenance operations (expired user cleanup)

#### 4. **Security Architecture**
- **JWT tokens** with access/refresh token pattern
- **bcrypt** for secure password hashing
- **Role-based permissions** using decorators
- **Input validation** at API boundaries

#### 5. **Database Design**
- **PostgreSQL** for production reliability
- **Alembic migrations** for version control
- **ULID** for user IDs (better than UUIDs for database performance)
- **Proper indexing** for query optimization

### Technology Stack

#### Backend Framework
- **FastAPI** - Modern, fast web framework for Python APIs
- **Pydantic** - Data validation using Python type hints
- **SQLAlchemy 2.0** - Python SQL toolkit and ORM

#### Database
- **PostgreSQL** - Production-grade relational database
- **Alembic** - Database migration tool

#### Authentication
- **PyJWT** - JSON Web Token implementation
- **bcrypt** - Password hashing
- **passlib** - Password context management

#### Background Processing
- **APScheduler** - Task scheduling

#### Development & Deployment
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Ruff** - Python linter and formatter
- **MyPy** - Static type checking

### Design Patterns Used

1. **Repository Pattern** - Abstracts data access
2. **Service Pattern** - Encapsulates business logic
3. **Factory Pattern** - Application creation (`create_app()`)
4. **Dependency Injection** - Service dependencies
5. **Strategy Pattern** - Authentication strategies

### Scalability Considerations

#### Horizontal Scaling
- **Stateless API design** allows multiple instances
- **JWT tokens** eliminate server-side session storage
- **Database connection pooling** for efficient resource usage

#### Performance Optimization
- **Async/await** for I/O bound operations
- **Database indexing** on frequently queried fields
- **Background task processing** for long-running operations
- **Response caching** strategies (future enhancement)

#### Monitoring & Observability
- **Sentry integration** for error tracking
- **Structured logging** for debugging
- **Health check endpoints** (future enhancement)
- **Metrics collection** (future enhancement)

### Future Enhancements

1. **Caching Layer** (Redis) for frequent queries
2. **Rate Limiting** to prevent API abuse
3. **Email Service Integration** for real verification
4. **API Versioning** for backward compatibility
5. **Monitoring Dashboard** with metrics and logs
6. **CI/CD Pipeline** for automated testing and deployment

## 🛠️ Development

### Local Development Setup
```bash
# Install dependencies
pip install -e .

# Run database migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload

# Format code
./scripts/format.sh

# Lint code
./scripts/lint.sh
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.