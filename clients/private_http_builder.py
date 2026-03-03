from typing import TypedDict
import httpx
import time


class AuthenticationUserDict(TypedDict):
    """Структура данных пользователя для авторизации."""
    email: str
    password: str


def get_private_http_client(user: AuthenticationUserDict) -> httpx.Client:
    base_url = "http://localhost:8000"

    # Даем серверу секунду, чтобы он точно запомнил нового юзера
    time.sleep(1)

    with httpx.Client(base_url=base_url) as client:
        login_payload = {"email": user["email"], "password": user["password"]}
        response = client.post("/api/v1/authentication/login", json=login_payload)

        if response.status_code in [200, 201]:
            data = response.json()

            # Достаем токен из той структуры, которую прислал твой сервер
            # Сначала смотрим в 'token', потом внутри ищем 'accessToken'
            token_data = data.get("token", {})

            if isinstance(token_data, dict):
                token = token_data.get("accessToken") or token_data.get("token")
            else:
                token = token_data  # На случай, если токен пришел строкой

            if not token:
                raise Exception(f"Не удалось вытащить accessToken. Ответ сервера: {data}")

            print(f"DEBUG: Токен успешно получен и расшифрован!")

            return httpx.Client(
                base_url=base_url,
                headers={"Authorization": f"Bearer {token}"}
            )
        else:
            raise Exception(f"Ошибка входа ({response.status_code}): {response.text}")