from fastapi import APIRouter
from validators.request_validators import LoginRequest, ResetPasswordRequest, LogoutRequest
from validators.response_validators import FailResponse, SuccessResponse
from services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()

@router.post("/login", response_model=SuccessResponse)
async def login(request: LoginRequest) -> SuccessResponse:
    try:
        access_token, refresh_token = await auth_service.login(request)
        return SuccessResponse(
            error=False,
            status="success",
            status_code=200,
            message="Login successful",
            detail={
                "access token": access_token,
                "refresh token": refresh_token
            },
        )
    except ValueError as ve:
        return FailResponse(
            error=True,
            status="fail",
            status_code=401,
            message="Failed to login. Try Again Later.",
            detail=str(ve),
        )
    except Exception as e:
        return FailResponse(
            error=True,
            status="fail",
            status_code=500,
            message="This is an internal server error. We are working on resolving the issue. Please try again later.",
            detail=str(e),
        )

@router.post("/logout", response_model=SuccessResponse)
async def logout(request: LogoutRequest) -> SuccessResponse:
    try:
        await auth_service.logout(request)
        return SuccessResponse(
            error=False,
            status="success",
            status_code=200,
            message="User Logged Out Successfully",
            detail={}
        )
    except Exception as e:
        return FailResponse(
            error=True,
            status="fail",
            status_code=500,
            message="This is an internal server error. We are working on resolving the issue. Please try again later.",
            detail=str(e)
        )

@router.post("/reset-password", response_model=SuccessResponse)
async def reset_password(request: ResetPasswordRequest) -> SuccessResponse:
    try:
        await auth_service.reset_password(request)
        return SuccessResponse(
            error=False,
            status="success",
            status_code=200,
            message="Password reset successful",
            detail={}
        )
    except ValueError as e:
        return FailResponse(
            error=True,
            status="fail",
            status_code=400,
            message="Password reset failed",
            detail=str(e)
        )
    except Exception as e:
        return FailResponse(
            error=True,
            status="fail",
            status_code=500,
            message="This is an internal server error. We are working on resolving the issue. Please try again later.",
            detail=str(e)
        )
