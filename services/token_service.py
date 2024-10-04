import jwt
import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
from typing import Optional
from models.token import Token
from config import settings
from helpers.enums import TokenType

class TokenService:
    def __init__(self, secret_key: str = settings.SECRET_KEY, algorithm: str = settings.ALGORITHM):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client["auth"]
        self.token_collection = self.db.get_collection('tokens')

    async def create_access_token(self, user_id: str) -> dict:
        """
        Create an access token for the user.
        """
        try:
            access_token_expires = datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            payload = {
                "sub": user_id,
                "exp": access_token_expires,
                "type": TokenType.access_token.value
            }
            access_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            return access_token
        except Exception as e:
            raise e

    async def create_refresh_token(self, user_id: str) -> str:
        """
        Create a refresh token for the user.
        """
        try:
            refresh_token_expires = datetime.datetime.now() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            payload = {
                "sub": user_id,
                "exp": refresh_token_expires,
                "type": TokenType.refresh_token.value
            }
            refresh_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

            token_data = Token(
                user_id=user_id,
                token=refresh_token,
                token_type=TokenType.refresh_token.value,
                expires_at=refresh_token_expires,
                created_at=datetime.datetime.now()
            )
            await self.token_collection.insert_one(token_data.model_dump())
            
            return refresh_token
        except Exception as e:
            raise e

    async def validate_token(self, token: str, token_type: TokenType) -> Optional[str]:
        """
        Validate the token based on its type (access/refresh/password_reset).
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != token_type.value:
                raise ValueError("Invalid token type")
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

    async def revoke_token(self, token: str) -> None:
        """
        Revoke a token (used for refresh tokens).
        """
        try:
            result = await self.token_collection.delete_one({"token": token})
            if result.deleted_count == 0:
                raise ValueError("Token not found or already revoked")
        except Exception as e:
            raise e

    async def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Refresh the access token using a valid refresh token.
        """
        try:
            user_id = await self.validate_token(refresh_token, TokenType.refresh_token)
            
            token_data = await self.token_collection.find_one({"token": refresh_token})
            if not token_data:
                raise ValueError("Invalid or revoked refresh token")
            
            return await self.create_access_token(user_id)
        except ValueError as e:
            raise e

    async def generate_password_reset_token(self, user_id: str) -> str:
        """
        Generate a password reset token for the user.
        """
        try:
            reset_token_expires = datetime.datetime.now() + datetime.timedelta(hours=48)
            payload = {
                "sub": user_id,
                "exp": reset_token_expires,
                "type": TokenType.password_reset_token.value
            }
            reset_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            
            token_data = Token(
                user_id=user_id,
                token=reset_token,
                token_type=TokenType.password_reset_token.value,
                expires_at=reset_token_expires,
                created_at=datetime.datetime.now()
            )
            await self.token_collection.insert_one(token_data.model_dump())

            return reset_token
        
        except ValueError as ve:
            raise ve
            
        except Exception as e:
            raise e

    async def verify_password_reset_token(self, token: str) -> str:
        """
        Verify a password reset token and return the user ID if valid.
        """
        try:
            return await self.validate_token(token, TokenType.password_reset_token)
        except Exception as e:
            raise e
        
    async def fetch_token_detail(self, token: str) -> dict:
        try:
            token_detail = await self.token_collection.find_one({"token": token})
            if not token_detail:
                raise ValueError("Invalid Token, doesnot exist!")
            return token_detail
        except Exception as e:
            raise e
