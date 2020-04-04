from dataclasses import dataclass


@dataclass
class ApiError(Exception):
    error_message: str = 'Bad Request'
    status_code: int = 400

    def get_response(self):
        return self.status_code, {'error': self.error_message}


class NotFound(ApiError):

    def __init__(self, error_message: str = 'Not Found') -> None:
        super().__init__(error_message=error_message, status_code=404)


class InternalError(ApiError):

    def __init__(self, e) -> None:
        super().__init__(error_message=str(e), status_code=500)
