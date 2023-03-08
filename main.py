from importlib import import_module

from fastapi import FastAPI

from app.db import setup as db_setup
from app.domain import router as app_router
from app.fastapi import route as api_route
from app.firebase import setup as firebase_setup
from app.search import setup as search_setup
from app.settings import get_settings, common as common_settings

setting: common_settings.CommonSetting = getattr(import_module(get_settings()), 'Setting')()

app = FastAPI()
app.router.route_class = api_route.CustomRoute
app.include_router(app_router.router)


@app.on_event('startup')
async def on_startup():
    await db_setup.setup(setting.DATABASES_CONFIG)
    # await search_setup.setup(setting.ELASTIC_CONFIG)
    await firebase_setup.setup(setting.FIREBASE_ADMIN_CONFIG)


@app.on_event('shutdown')
async def on_shutdown():
    await db_setup.cleanup()
    # await search_setup.cleanup()
