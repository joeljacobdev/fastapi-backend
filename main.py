import asyncio
import uvloop
from importlib import import_module
from fastapi import FastAPI
from app.config import get_config
from app.fastapi import route as api_route

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
setting = getattr(import_module(get_config()), 'Setting')()

app = FastAPI()
app.router.route_class = api_route.CustomRoute
