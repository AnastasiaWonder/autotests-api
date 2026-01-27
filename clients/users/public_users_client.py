from typing import TypedDict
import httpx

from clients.api_client import APIClient


class CreateUserRequest(TypedDict):
    """
    Структура тела запроса для создания пользователя.

    Поля соответствуют контракту API эндпоинта /api/v1/users.
    """
    email: str
    password: str
    firstName: str
    lastName: str
    middleName: str


class PublicUsersClient(APIClient):
    """
    API-клиент для публичных методов работы с пользователями.

    Данный клиент предназначен для эндпоинтов, которые
    не требуют авторизации (например, создание пользователя).

    Наследуется от APIClient, который содержит общую логику
    работы с HTTP-клиентом.
    """

    def create_user_api(self, request: CreateUserRequest) -> httpx.Response:
        """
        Создание нового пользователя через публичный API.

        Метод выполняет POST-запрос на эндпоинт `/api/v1/users`
        и передаёт данные пользователя в формате JSON.

        Args:
            request (CreateUserRequest):
                Данные пользователя для создания.
                Ожидаемая структура:
                {
                    "email": str,
                    "password": str,
                    "firstName": str,
                    "lastName": str,
                    "middleName": str
                }

        Returns:
            httpx.Response:
                HTTP-ответ от сервера.
                Используется в автотестах для проверки:
                - статус-кода
                - тела ответа
                - заголовков
        """
        return self.post(
            url="/api/v1/users",
            json=request
        )
