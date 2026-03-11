from httpx import Client

def get_public_http_client() -> Client:
    """
    Создаёт базовый HTTP-клиент без заголовков авторизации.
    """
    return Client(
        base_url="http://localhost:8000",
        timeout=100
    )