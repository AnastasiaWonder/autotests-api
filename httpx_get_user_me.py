import httpx
# Импортируем наш завод данных
from tools.fakers import fake

BASE_URL = "http://localhost:8000"


def create_and_get_me():
    # 1. СОЗДАЕМ ПОЛЬЗОВАТЕЛЯ (чтобы нам было под кем заходить)
    user_payload = {
        "email": fake.email(),
        "password": fake.password(),
        "lastName": fake.last_name(),
        "firstName": fake.first_name(),
        "middleName": "HttpxTest"
    }

    create_res = httpx.post(f"{BASE_URL}/api/v1/users", json=user_payload)
    create_res.raise_for_status()
    print(f"Пользователь создан: {user_payload['email']}")

    # 2. ЛОГИН
    login_payload = {
        "email": user_payload["email"],
        "password": user_payload["password"]
    }

    login_response = httpx.post(
        f"{BASE_URL}/api/v1/authentication/login",
        json=login_payload
    )
    login_response.raise_for_status()

    access_token = login_response.json()["token"]["accessToken"]
    print("Токен получен.")

    # 3. ПОЛУЧАЕМ ДАННЫЕ О СЕБЕ (/me)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    user_me_response = httpx.get(
        f"{BASE_URL}/api/v1/users/me",
        headers=headers
    )
    user_me_response.raise_for_status()

    print(f"Статус /me: {user_me_response.status_code}")
    print("Данные из профиля:")
    print(user_me_response.json())


if __name__ == "__main__":
    create_and_get_me()