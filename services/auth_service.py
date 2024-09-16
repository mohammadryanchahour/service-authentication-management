from fastapi import requests
from passlib.context import CryptContext
from validators.request_validators import LoginRequest, ResetPasswordRequest, LogoutRequest
from services.token_service import TokenService
from config import settings

class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.token_service = TokenService()

    async def login(self, request: LoginRequest):
        try:
            user = await self._get_user_by_username(request.username)
            if not user or not self.pwd_context.verify(request.password, user['password']):
                raise ValueError("Invalid username or password")

            access_token = await self.token_service.create_access_token(user_id=user['id'])
            refresh_token = await self.token_service.create_refresh_token(user_id=user['id'])

            return access_token, refresh_token
        except Exception as e:
            raise e

    async def logout(self, request: LogoutRequest):
        try:
            return await self.token_service.revoke_token(request.token)
        except Exception as e:
            raise e

    async def reset_password(self, request: ResetPasswordRequest):
        try:
            user = await self._get_user_by_username(request.email)
            if not user:
                raise ValueError("Invalid email address")

            hashed_password = self.pwd_context.hash(request.new_password)
            return await self._update_user_password(user['id'], hashed_password)
        except Exception as e:
            raise e
    
    def _get_user_by_username(self, username: str):
        """
        Fetch user details from the User Management service.
        """
        try:
            response = requests.get(f"{settings.USER_MANAGEMENT_URL}/users/{username}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Error fetching user: {str(e)}")

    def _update_user_password(self, user_id: str, hashed_password: str):
        """
        Update the user's password in the User Management service.
        """
        try:
            response = requests.put(
                f"{settings.USER_MANAGEMENT_URL}/users/{user_id}/password",
                json={"password": hashed_password}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Error updating password: {str(e)}")
