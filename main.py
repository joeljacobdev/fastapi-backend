import asyncio
import uvloop
from importlib import import_module
from fastapi import FastAPI

from app.search import setup as search_setup
from app.db import setup as db_setup
from app.config import get_config
from app.fastapi import route as api_route
from app.domain import router as app_router

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
setting = getattr(import_module(get_config()), 'Setting')()

app = FastAPI()
es = search_setup.setup()
app.router.route_class = api_route.CustomRoute
app.include_router(app_router.router)


@app.on_event('startup')
async def on_startup():
    await db_setup.setup(setting.DATABASES_CONFIG)
    await search_setup.setup()


@app.on_event('shutdown')
async def on_shutdown():
    await db_setup.cleanup()
    await search_setup.setup()
