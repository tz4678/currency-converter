from dataclasses import dataclass


@dataclass
class ApiError(Exception):
    message: str = 'Bad Request'
    status_code: int = 400

    def get_response(self):
        return self.status_code, {'code': self.status_code, 'message': self.message}


class NotFound(ApiError):

    def __init__(self, message: str = 'Not Found') -> None:
        super().__init__(message=message, status_code=404)


class InternalError(ApiError):

    def __init__(self, e) -> None:
        super().__init__(message=str(e), status_code=500)
