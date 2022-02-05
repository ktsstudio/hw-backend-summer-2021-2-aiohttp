import typing

from aiohttp.web_exceptions import (
    HTTPError,
    HTTPBadRequest,
    HTTPUnprocessableEntity,
)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware, setup_aiohttp_apispec

from app.web.utils import exception_json_response, http_error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        try:
            response = await handler(request)
            return response
        except HTTPUnprocessableEntity as e:
            raise HTTPBadRequest(
                reason=e.reason,
                text=e.text   
            )
    except HTTPError as e:
        return http_error_json_response(e)
    except Exception as e:
        return exception_json_response(e)


def setup_middlewares(app: "Application"):
    setup_aiohttp_apispec(app)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
