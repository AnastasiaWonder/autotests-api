import pytest  # <-- ОБЯЗАТЕЛЬНО ДОБАВЬ ЭТУ СТРОЧКУ!
from http import HTTPStatus
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import LoginRequestSchema, LoginResponseSchema
from tools.assertions.base import assert_status_code
from tools.assertions.authentication import assert_login_response
from tools.assertions.schema import validate_json_schema


@pytest.mark.regression
@pytest.mark.authentication
def test_login():
    """
    Тест проверяет возможность входа пользователя в систему
    с валидными учетными данными.
    """
    # 1. Готовим клиентов
    public_users_client = get_public_users_client()
    auth_client = get_authentication_client()

    # 2. Создаем нового пользователя для теста
    user_request = CreateUserRequestSchema()
    public_users_client.create_user(user_request)

    # 3. Формируем запрос на логин, используя данные созданного юзера
    login_request = LoginRequestSchema(
        email=user_request.email,
        password=user_request.password
    )

    # 4. Выполняем вход
    login_response = auth_client.login_api(login_request)

    # 5. Десериализуем ответ
    login_response_data = LoginResponseSchema.model_validate_json(login_response.text)

    # 6. ПРОВЕРКИ
    # Проверяем статус 200 OK
    assert_status_code(login_response.status_code, HTTPStatus.OK)

    # Проверяем бизнес-логику (токены)
    assert_login_response(login_response_data)

    # ПРОВЕРКА СХЕМЫ (ты её импортировала, давай используем!)
    # Это та самая "строгая проверка", чтобы типы данных были идеальными
    validate_json_schema(login_response.json(), login_response_data.model_json_schema())