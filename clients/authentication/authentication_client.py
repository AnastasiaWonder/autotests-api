from httpx import Response
from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client
from clients.authentication.authentication_schema import (
    LoginRequestSchema, LoginResponseSchema, RefreshRequestSchema
)

class AuthenticationClient(APIClient):
    """Клиент для работы с эндпоинтами аутентификации."""

    def login_api(self, request: LoginRequestSchema) -> Response:
        return self.post("/api/v1/authentication/login", json=request.model_dump(by_alias=True))

    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        return self.post("/api/v1/authentication/refresh", json=request.model_dump(by_alias=True))

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        response = self.login_api(request)
        # Валидируем ответ через Pydantic
        return LoginResponseSchema.model_validate_json(response.text)

def get_authentication_client() -> AuthenticationClient:
    """Создает экземпляр клиента аутентификации."""
    return AuthenticationClient(client=get_public_http_client())