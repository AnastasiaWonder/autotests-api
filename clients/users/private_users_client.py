from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema

class PrivateUsersClient(APIClient):
    """
    Клиент для работы с защищенными методами /api/v1/users
    """

    def get_user_api(self, user_id: str) -> Response:
        """
        Метод получения данных пользователя.
        GET /api/v1/users/{user_id}
        """
        return self.get(f"/api/v1/users/{user_id}")

def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Создаёт экземпляр PrivateUsersClient с настроенной авторизацией.
    """
    return PrivateUsersClient(client=get_private_http_client(user))