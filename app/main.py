from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .config.config import settings, initiate_database
from .routes.weather import router


async def start_database():
    await initiate_database()


def get_application() -> FastAPI:
    # Create application
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION
    )
    # Middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"]
    )
    # Add handlers
    application.add_event_handler("startup", start_database)
    # Include routers
    application.include_router(router, tags=["weather"])

    return application


app = get_application()
