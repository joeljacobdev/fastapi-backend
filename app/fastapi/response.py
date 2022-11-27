import typing
from fastapi.responses import JSONResponse
from app.core import json


class FastJsonResponse(JSONResponse):
    def render(self, content: typing.Any) -> bytes:
        return json.dumps_bytes(content)
