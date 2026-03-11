from httpx import Response
from clients.api_client import APIClient
from clients.public_http_builder import get_public_http_client
# Импортируем наши новые схемы
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema

class PublicUsersClient(APIClient):
    """
    API-клиент для публичных методов работы с пользователями.
    """

    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """
        Создание нового пользователя через публичный API.
        """
        # ВОТ ТУТ ИСПРАВЛЕНИЕ ОШИБКИ:
        # .model_dump(by_alias=True) превращает объект Pydantic обратно в словарь,
        # который понимает библиотека httpx, и меняет first_name на firstName.
        return self.post(
            url="/api/v1/users",
            json=request.model_dump(by_alias=True)
        )

    def create_user(self, request: CreateUserRequestSchema) -> CreateUserResponseSchema:
        """
        Метод создает пользователя и возвращает типизированный объект ответа.
        """
        response = self.create_user_api(request)
        # Превращаем текст ответа в красивый объект с подсказками (через точку)
        return CreateUserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> PublicUsersClient:
    """
    Билдер для создания публичного клиента.
    Используем общий public_http_builder, чтобы настройки были в одном месте.
    """
    return PublicUsersClient(client=get_public_http_client())