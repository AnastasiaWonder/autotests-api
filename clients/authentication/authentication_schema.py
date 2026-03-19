from pydantic import BaseModel, Field, ConfigDict

from tools.fakers import fake

class TokenSchema(BaseModel):
    """Структура токенов в ответе сервера."""
    model_config = ConfigDict(populate_by_name=True)

    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")

class LoginRequestSchema(BaseModel):
    """
    Запрос на логин.
    Теперь умеет сам придумывать учетные данные.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)

class LoginResponseSchema(BaseModel):
    """Ответ сервера при успешном входе."""
    token: TokenSchema

class RefreshRequestSchema(BaseModel):
    """
    Запрос на обновление токена.
    По умолчанию генерирует случайную строку-токен.
    """
    model_config = ConfigDict(populate_by_name=True)

    refresh_token: str = Field(alias="refreshToken", default_factory=fake.uuid4)