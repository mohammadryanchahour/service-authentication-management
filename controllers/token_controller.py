from fastapi import APIRouter
from validators.request_validators import TokenRequest, VerifyTokenRequest
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
    
@router.post("/verify-token", response_model= SuccessResponse)
async def verify_token(request: VerifyTokenRequest) -> SuccessResponse:
    try:
        token_detail = await token_service.validate_token(request.token)
        if token_detail:
            is_token_verified = await token_service.validate_token(token=token_detail.get("token"), token_type=token_detail.get("token_type"))
        if is_token_verified:
            return SuccessResponse(
                error=False,
                status="success",
                status_code=200,
                message=f"{token_detail["token_type"]} token verified successfully.",
                detail={
                    "Token": token_detail["token"],
                    "Token Type": token_detail["token_type"]
                },
            )

    except Exception as e:
        return FailResponse(
            error=True,
            status="fail",
            status_code=500,
            message="This is an internal server error. We are working on resolving the issue. Please try again later.",
            detail=str(e)
        )
