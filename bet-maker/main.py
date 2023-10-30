from fastapi import FastAPI
from uvicorn import Server, Config
from fastapi.middleware.cors import CORSMiddleware

from app.adapters.databases.postgres import AlchemyMaster
from app.api.endpoints import first_router
from settings import ApiSettings, AppMode, get_api_settings

app = FastAPI(docs_url="/docs" if get_api_settings().APP_MODE == AppMode.DEV else None, redoc_url=None)
app.include_router(first_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def server_setup(settings: ApiSettings = get_api_settings()):

    AlchemyMaster.prepare_engine(pg_username=settings.POSTGRES_USER,
                                 pg_password=settings.POSTGRES_PASSWORD,
                                 pg_host=settings.POSTGRES_HOST)


    if settings.APP_MODE == AppMode.DEV:
        print(f'[S] API ROOT http://localhost:{settings.API_PORT}')
        print(f'[S] API DOCS http://localhost:{settings.API_PORT}/docs')
        log_level = 'warning'
        reload_policy = True
    else:
        print(f'API WIIL BE STARTED IN PRODUCTION MODE EXPOSED AT PORT:{settings.API_PORT}')
        log_level = 'info'
        reload_policy = False

    return Server(config=Config('main:app', host="0.0.0.0",
                                port=settings.API_PORT,
                                log_level=log_level, reload=reload_policy
                                ))


if __name__ == "__main__":
    server = server_setup()
    server.run()
