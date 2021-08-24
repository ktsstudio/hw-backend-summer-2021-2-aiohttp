def ok_response(data: dict):
    return {
        "status": "ok",
        "data": data,
    }


def error_response(status: str, message: str, data: dict):
    return {
        "status": status,
        "message": message,
        "data": data,
    }
