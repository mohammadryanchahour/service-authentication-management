from fastapi import APIRouter
from validators.request_validators import TokenRequest
from validators.response_validators import FailResponse, SuccessResponse
from services.token_service import TokenService

router = APIRouter()

token_service = TokenService()

@router.post("/generate-password-reset-token", response_model=SuccessResponse)
async def generate_password_reset_token(request: TokenRequest) -> SuccessResponse:
    try:
        reset_token = await token_service.generate_password_reset_token(request.user_id)
        return SuccessResponse(
            error=False,
            status="success",
            status_code=200,
            message="Password reset token generated successfully.",
            detail={
                "reset token": reset_token
            },
        )
    except ValueError as ve:
        return FailResponse(
            error=True,
            status="fail",
            status_code=400,
            message="Error While Generating Reset Token.",
            detail=str(ve)
        )
    except Exception as e:
        return FailResponse(
            error=True,
            status="fail",
            status_code=500,
            message="This is an internal server error. We are working on resolving the issue. Please try again later.",
            detail=str(e)
        )
