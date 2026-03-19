import httpx
# 1. Вместо import time импортируем наш fake
from tools.fakers import fake

BASE_URL = "http://localhost:8000"


# 2. Локальную функцию get_random_email() мы удалили

def create_user():
    # 3. Теперь используем fake.email()
    payload = {
        "email": fake.email(),
        "password": "password123",
        "lastName": fake.last_name(),  # Раз уж гуляем, добавим и сюда фейки!
        "firstName": fake.first_name(),
        "middleName": "Test"
    }

    response = httpx.post(f"{BASE_URL}/api/v1/users", json=payload)
    response.raise_for_status()

    print("Create user status code:", response.status_code)

    # Возвращаем данные для логина
    return payload["email"], payload["password"], response.json()["user"]["id"]


def login_user(email: str, password: str) -> str:
    payload = {
        "email": email,
        "password": password
    }

    response = httpx.post(
        f"{BASE_URL}/api/v1/authentication/login",
        json=payload
    )
    response.raise_for_status()

    print("Login success! Token received.")
    return response.json()["token"]["accessToken"]


def update_user(user_id: str, access_token: str):
    # 4. И здесь меняем на fake.email() и другие методы
    payload = {
        "email": fake.email(),
        "lastName": fake.last_name(),
        "firstName": fake.first_name(),
        "middleName": "HTTPX"
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = httpx.patch(
        f"{BASE_URL}/api/v1/users/{user_id}",
        json=payload,
        headers=headers
    )
    response.raise_for_status()

    print("Update user status code:", response.status_code)
    print("Updated user data:", response.json()["user"]["email"])


def main():
    email, password, user_id = create_user()
    token = login_user(email, password)
    update_user(user_id, token)


if __name__ == "__main__":
    main()