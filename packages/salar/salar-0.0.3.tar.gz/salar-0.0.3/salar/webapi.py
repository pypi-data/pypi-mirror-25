
status_dict = {
    200: 'OK',
    201: 'Created',
    202: 'Accepted',
    204: 'No Content',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    307: 'Temporary Redirect',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    405: 'Method Not Allowed',
    406: 'Not Acceptable',
    409: 'Conflict',
    410: 'Gone',
    412: 'Precondition Failed',
    415: 'Unsupported Media Type',
    422: 'Unprocessable Entity',
    451: 'Unavailable For Legal Reasons',
    500: 'Internal Server Error',
}


class HttpError(Exception):
    def __init__(self, status_code, text, headers=None):
        self.status_code = status_code
        self.text = text
        self.headers = headers or {}

    def update(self, ctx):
        ctx.status_code = self.status_code
        ctx.reason = status_dict.get(ctx.status_code, 'Unknown')
        ctx.headers = self.headers


class BadRequestError(HttpError):
    def __init__(self, text):
        self.status_code = 400
        self.text = text
        self.headers = {}
