import json
import typing

from aiohttp.web_exceptions import (
    HTTPBadRequest,
    HTTPUnauthorized,
    HTTPForbidden,
    HTTPNotFound,
    HTTPMethodNotAllowed,
    HTTPConflict,
    HTTPUnprocessableEntity,
    HTTPInternalServerError
)
from aiohttp.web_middlewares import middleware
from aiohttp_apispec import validation_middleware, setup_aiohttp_apispec

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application, Request

HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}


@middleware
async def error_handling_middleware(request: "Request", handler):
    try:
        response = await handler(request)
        return response
    except (HTTPBadRequest, HTTPUnprocessableEntity) as e:
        return error_json_response(
            http_status=400,
            status=HTTP_ERROR_CODES[400],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPUnauthorized as e:
        return error_json_response(
            http_status=401,
            status=HTTP_ERROR_CODES[401],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPForbidden as e:
        return error_json_response(
            http_status=403,
            status=HTTP_ERROR_CODES[403],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPNotFound as e:
        return error_json_response(
            http_status=404,
            status=HTTP_ERROR_CODES[404],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPMethodNotAllowed as e:
        return error_json_response(
            http_status=405,
            status=HTTP_ERROR_CODES[405],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPConflict as e:
        return error_json_response(
            http_status=409,
            status=HTTP_ERROR_CODES[409],
            message=e.reason,
            data=json.loads(e.text),
        )
    except HTTPInternalServerError as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=e.reason,
            data=json.loads(e.text),
        )
    except Exception as e:
        return error_json_response(
            http_status=500,
            status=HTTP_ERROR_CODES[500],
            message=e.__doc__,
            data={ "args": e.args },
        )


def setup_middlewares(app: "Application"):
    setup_aiohttp_apispec(app)
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
