
class IllegalArgumentError(ValueError):
    def __init__(self, msg=''):
        self.message = msg


class ExceptionWithErrorCode(Exception):
    def __init__(self, err_code, msg='', data=None):
        self.message = msg
        self.err_code = err_code
        self.data = data


class UnauthorizedException(Exception):
    def __init__(self, err_code=None, msg=''):
        self.message = msg
        self.err_code = err_code


class ForbiddenException(Exception):
    def __init__(self, err_code=None, msg=''):
        self.message = msg
        self.err_code = err_code
