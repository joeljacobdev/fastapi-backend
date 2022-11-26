from importlib import import_module
from fastapi import FastAPI
from app.config import get_config

setting = getattr(import_module(get_config()), 'Setting')()
print(setting)

app = FastAPI()
