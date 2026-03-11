import time
from httpx import Client
from pydantic import BaseModel
from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema


# 1. Описываем схему пользователя через BaseModel
class AuthenticationUserSchema(BaseModel):
    """Структура данных пользователя для авторизации."""
    email: str
    password: str


def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    """
    Создает авторизованный HTTP-клиент, используя Pydantic-модели.
    """
    base_url = "http://localhost:8000"

    # Даем серверу секунду, чтобы он точно запомнил нового юзера (согласно твоей логике)
    time.sleep(1)

    # 2. Используем готовый клиент аутентификации
    auth_client = get_authentication_client()

    # 3. Формируем запрос на логин (используем данные из объекта через точку)
    login_request = LoginRequestSchema(
        email=user.email,
        password=user.password
    )

    # 4. Выполняем вход. Метод .login() сам проверит ответ и вернет LoginResponseSchema
    login_response = auth_client.login(login_request)

    print(f"DEBUG: Токен успешно получен через Pydantic-клиент!")

    # 5. Возвращаем клиент. Доступ к токену теперь тоже максимально простой — через точку!
    return Client(
        base_url=base_url,
        headers={"Authorization": f"Bearer {login_response.token.access_token}"},
        timeout=100
    )