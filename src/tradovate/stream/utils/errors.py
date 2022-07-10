## Imports
from __future__ import annotations


## Classes
class SessionException(Exception):
    """Base Session exception"""
    pass


class LoginException(SessionException):
    """Base Session exception for authentication"""
    pass


class LoginInvalidException(LoginException):
    """Session exception for authentication invalid credentials"""

    # -Constructor
    def __init__(self, message: str) -> LoginInvalidException:
        super().__init__(message)


class LoginCaptchaException(LoginException):
    """Session exception for authentication rate limiting and captcha"""

    # -Constructor
    def __init__(self, ticket: str, time: int, captcha: bool) -> LoginInvalidException:
        message = ("Unable to login due to rate limiting. Ticket #"
                  f"{ticket}, {time} seconds. Captcha required: {captcha}.")
        super().__init__(message)


class WebSocketException(Exception):
    """Base WebSocket exception"""
    pass


class WebSocketOpenException(Exception):
    """WebSocket exception for open failures"""

    # -Constructor
    def __init__(self, url: str) -> WebSocketOpenException:
        super().__init__(f"Unable to open websocket with address: {url}.")


class WebSocketAuthorizationException(Exception):
    """WebSocket exception for authentication"""

    # -Constructor
    def __init__(self, url: str, token: str) -> WebSocketOpenException:
        super().__init__(
            f"Unable to authorize websocket with address: {url}. Token used: {token}."
        )


class WebSocketClosedException(Exception):
    """WebSocket exception for already closed"""

    # -Constructor
    def __init__(self, url: str) -> WebSocketOpenException:
        super().__init__(f"Connection with address: {url} has expired.")
