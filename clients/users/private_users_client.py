from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema

class PrivateUsersClient(APIClient):
    """
    Клиент для работы с защищенными методами /api/v1/users
    """

    # ЭТОТ МЕТОД НУЖЕН ДЛЯ ТЕСТА /me (который мы сейчас чиним)
    def get_user_me_api(self) -> Response:
        """
        Метод получения данных ТЕКУЩЕГО пользователя.
        GET /api/v1/users/me
        """
        return self.get("/api/v1/users/me")

    # Этот метод у тебя уже был (он для получения ЛЮБОГО юзера по ID)
    def get_user_api(self, user_id: str) -> Response:
        """
        Метод получения данных пользователя по ID.
        GET /api/v1/users/{user_id}
        """
        return self.get(f"/api/v1/users/{user_id}")

def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Создаёт экземпляр PrivateUsersClient с настроенной авторизацией.
    """
    return PrivateUsersClient(client=get_private_http_client(user))