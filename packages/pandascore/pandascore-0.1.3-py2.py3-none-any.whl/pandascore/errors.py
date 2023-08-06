""" Exceptions for PandaScore API """


class Error(Exception):
    pass


class TokenError(Error):
    pass


class DataReadError(Error):
    pass


class JSONReadError(Error):
    pass


class NotFoundError(Error):
    pass


class UnauthorizedError(Error):
    pass


class MalformedRequestError(Error):
    pass


class ForbiddenError(Error):
    pass


class UnprocessableError(Error):
    pass


class UnknownError(Error):
    pass


_api_error_map = {
    404: NotFoundError,
    401: UnauthorizedError,
    400: MalformedRequestError,
    403: ForbiddenError,
    422: UnprocessableError,
}


def check_status(expected, req):
    if req.status_code == expected:
        return
    try:
        err_cls = _api_error_map[req.status_code]
    except KeyError:
        err_cls = UnknownError
    raise err_cls('[%d]resp: %s' % (req.status_code, req.content))
