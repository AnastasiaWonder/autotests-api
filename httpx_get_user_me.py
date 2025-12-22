import httpx

login_payload = {
    "email": "user@example.com",
    "password": "string"
}

login_response = httpx.post(
    "http://localhost:8000/api/v1/authentication/login",
    json=login_payload
)

print("Login status code:", login_response.status_code)

login_response_data = login_response.json()
access_token = login_response_data["token"]["accessToken"]


headers = {
    "Authorization": f"Bearer {access_token}"
}

user_me_response = httpx.get(
    "http://localhost:8000/api/v1/users/me",
    headers=headers
)

print("User me status code:", user_me_response.status_code)
print("User data:")
print(user_me_response.json())
