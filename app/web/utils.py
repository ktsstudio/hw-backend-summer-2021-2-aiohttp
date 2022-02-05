from typing import Any, Optional

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_response import Response


HTTP_ERROR_CODES = {
    400: "bad_request",
    401: "unauthorized",
    403: "forbidden",
    404: "not_found",
    405: "not_implemented",
    409: "conflict",
    500: "internal_server_error",
}

def json_response(data: Any = None, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(
        data={
            "status": status,
            "data": data,
        }
    )

def error_json_response(
    http_status: int,
    status: Optional[str] = None,
    message: Optional[str] = None,
    data: Optional[dict] = None,
) -> Response:
    return aiohttp_json_response(
        status=http_status,
        data={
            "status": status or HTTP_ERROR_CODES[http_status],
            "message": message,
            "data": data,
        }
    )
