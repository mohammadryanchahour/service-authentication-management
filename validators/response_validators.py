from pydantic import BaseModel
from typing import Optional, Dict

# Base class for all responses
class BaseResponse(BaseModel):
    error: bool
    status: str
    status_code: int
    message: str
    detail: Optional[Dict] = {}

# Success Response
class SuccessResponse(BaseResponse):
    error: bool = False
    status: str = "success"
    status_code: int = 200
    message: str = "Request successful"
    detail: Optional[Dict] = {}

# Fail Response
class FailResponse(BaseResponse):
    error: bool = True
    status: str = "fail"
    status_code: int = 400
    message: str = "Request failed"
    detail: Optional[str] = ""

# Specific Response Models for Different Scenarios

# class LoginResponse(SuccessResponse):
#     pass

# class ResetPasswordResponse(SuccessResponse):
#     pass

# class LogoutResponse(SuccessResponse):
#     pass

# class ValidateTokenResponse(SuccessResponse):
#     valid: bool = False

# class RevokeTokenResponse(SuccessResponse):
#     pass
