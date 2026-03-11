from pydantic import BaseModel, Field

class TokenSchema(BaseModel):
    """Структура токенов."""
    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")

class LoginRequestSchema(BaseModel):
    """Запрос на логин."""
    email: str
    password: str

class LoginResponseSchema(BaseModel):
    """Ответ при логине."""
    token: TokenSchema

class RefreshRequestSchema(BaseModel):
    """Запрос на обновление токена."""
    refresh_token: str = Field(alias="refreshToken")