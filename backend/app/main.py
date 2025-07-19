from pathlib import Path
from app.services.vector_store import calendar_vector_store
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.api.v1 import api_router
from app.core import settings
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.utils import (
    AppExceptionCase,
    CustomizeLogger,
    app_exception_handler,
    http_exception_handler,
    request_validation_exception_handler,
)
from app.database.repositories.calendar import CalendarRepository

config_path = Path(__file__).with_name("logging_conf.json")

engine = create_async_engine(str(settings.db_url), echo=False)
SessionFactory = async_sessionmaker(bind=engine, expire_on_commit=False)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.session_factory = SessionFactory
    app.state.pool = SessionFactory  

    # Startup: initialize FAISS
    async with SessionFactory() as session:
        repo = CalendarRepository(session)

        rows_by_user = await repo.get_all_with_embeddings_by_user()
        if not rows_by_user:
            app.logger.warning("⚠️ No events found to initialize FAISS.")
        else:
            for user_id, user_rows in rows_by_user.items():
                embeddings = [r[0] for r in user_rows]
                metadata = [r[1:] for r in user_rows]
                calendar_vector_store.build_user_index(user_id, embeddings, metadata)

            app.logger.info(f"✅ FAISS index initialized for {len(rows_by_user)} users.")

    yield

def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan, **settings.fastapi_kwargs)
    
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_middleware(CorrelationIdMiddleware)
    _app.logger = CustomizeLogger.make_logger(config_path)
    _app.include_router(api_router, prefix=settings.api_v1_prefix)
    _app.mount("/static", StaticFiles(directory="app/static"))

    @_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=_app.openapi_url,
            title=_app.title + " - Swagger UI custom",
            oauth2_redirect_url=_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"{settings.openapi_prefix}/static/swagger-ui-bundle.js",
            swagger_css_url=f"{settings.openapi_prefix}/static/swagger-ui.css",
        )

    @_app.get(_app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @_app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=_app.openapi_url,
            title=_app.title + " - ReDoc",
            redoc_js_url=f"{settings.openapi_prefix}/static/redoc.standalone.js",
        )

    @_app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request, e):
        return await http_exception_handler(request, e)

    @_app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        return await request_validation_exception_handler(request, e)

    @_app.exception_handler(AppExceptionCase)
    async def custom_app_exception_handler(request, e):
        return await app_exception_handler(request, e)

    _app.add_event_handler("startup", create_start_app_handler(_app, settings))
    _app.add_event_handler("shutdown", create_stop_app_handler(_app))


    
    return _app

app = create_app()
