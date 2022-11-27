from typing import (
    Callable, Type, Coroutine, Any
)
from fastapi import Request, Response
from fastapi.routing import APIRoute
from app.fastapi import request as fastapi_request, response as fastapi_response


class CustomRoute(APIRoute):
    """
    Custom Route class to use orjson for json dumps/loads
    """
    def __init__(self, *args, request_class=fastapi_request.FastJsonRequest, **kwargs):
        self.request_class = request_class
        kwargs['response_class'] = fastapi_response.FastJsonResponse
        super(CustomRoute, self).__init__(*args, **kwargs)

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_request_handler = super().get_route_handler()

        async def custom_request_handler(request: Request) -> Type[Response]:
            request = self.request_class(request)
            response = await original_request_handler(request)
            return response

        return custom_request_handler
