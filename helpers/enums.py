from enum import Enum


class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    RESET_PASSWORD = "reset_password"