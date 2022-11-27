import typing
from types import MethodType
from fastapi import Request
from app.core import json


class FastJsonRequest(Request):
    def __new__(cls, request: Request):
        request.json = MethodType(cls.json, request)
        return request

    async def json(self) -> typing.Any:
        if not hasattr(self, "_json"):
            body = await self.body()
            self._json = json.loads(body)
        return self._json
