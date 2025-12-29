import httpx
import time


BASE_URL = "http://localhost:8000"


def get_random_email() -> str:
    return f"user.{time.time()}@example.com"


def create_user():
    payload = {
        "email": get_random_email(),
        "password": "string",
        "lastName": "Initial",
        "firstName": "User",
        "middleName": "Test"
    }

    response = httpx.post(f"{BASE_URL}/api/v1/users", json=payload)
    response.raise_for_status()

    print("Create user status code:", response.status_code)
    print("Create user response:", response.json())

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

    print("Login status code:", response.status_code)
    print("Login response:", response.json())

    return response.json()["token"]["accessToken"]


def update_user(user_id: str, access_token: str):
    payload = {
        "email": get_random_email(),
        "lastName": "Updated",
        "firstName": "User",
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
    print("Updated user data:", response.json())


def main():
    email, password, user_id = create_user()
    token = login_user(email, password)
    update_user(user_id, token)


if __name__ == "__main__":
    main()
