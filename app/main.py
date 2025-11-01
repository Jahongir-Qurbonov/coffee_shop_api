import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings

if settings.SENTRY_DSN and settings.ENVIRONMENT != "development":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)


def include_routers(app: FastAPI):
    from .routers.auth import router as auth_router
    from .routers.users import router as users_router

    app.include_router(auth_router, prefix="/auth")
    app.include_router(users_router, prefix="/users")


def create_app():
    app = FastAPI(
        title="Coffee Shop API",
        description="""
        ## Coffee Shop User Management API

        A comprehensive user management system for coffee shop operations, providing:

        * **User Registration** - Sign up new customers with email verification
        * **Authentication** - Secure JWT-based login with access and refresh tokens
        * **User Management** - Admin and user profile management
        * **Role-based Access** - Different permissions for admin and regular users
        * **Email Verification** - Account verification system for enhanced security

        ### Authentication

        This API uses JWT (JSON Web Tokens) for authentication. After logging in, you'll receive:
        - An `access_token` for API requests (shorter lifespan)
        - A `refresh_token` to obtain new access tokens (longer lifespan)

        ### User Roles

        - **User**: Regular customers with access to their own profile
        - **Admin**: Staff members with access to user management features

        ### API Features

        - Automatic cleanup of unverified accounts after 2 days
        - Secure password hashing with bcrypt
        - CORS support for web applications
        - Comprehensive error handling and validation
        """,
        version="1.0.0",
        terms_of_service="https://example.com/terms/",
        contact={
            "name": "Coffee Shop API Support",
            "url": "https://example.com/contact/",
            "email": "support@coffeeshop.example.com",
        },
        license_info={
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
        tags_metadata=[
            {
                "name": "login",
                "description": "Authentication operations including login, signup, token refresh, and email verification",
            },
            {
                "name": "users",
                "description": "User management operations for profile access and admin functions",
            },
        ],
        openapi_tags=[
            {
                "name": "login",
                "description": "Authentication operations including login, signup, token refresh, and email verification",
            },
            {
                "name": "users",
                "description": "User management operations for profile access and admin functions",
            },
        ],
    )

    if settings.ALL_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALL_CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    include_routers(app)

    return app


app = create_app()
