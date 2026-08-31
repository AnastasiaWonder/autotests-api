from http import HTTPStatus
import pytest

# Импортируем типы для аннотаций
from clients.users.public_users_client import PublicUsersClient # если он нужен
from clients.users.private_users_client import PrivateUsersClient # <--- ТЕПЕРЬ ОН ТУТ
from clients.users.users_schema import GetUserResponseSchema
from tests.conftest import UserFixture
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import fake

# Импортируем наши "проверялки"
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.assertions.users import assert_get_user_response

@pytest.mark.users
@pytest.mark.regression
def test_get_user_me(private_users_client: PrivateUsersClient, function_user: UserFixture):
    """
    Тест проверяет получение данных текущего авторизованного пользователя.
    """
    # 1. Отправляем запрос (через клиента, который уже знает наш токен)
    response = private_users_client.get_user_me_api()

    # 2. Проверяем статус-код (должен быть 200 OK)
    assert_status_code(response.status_code, HTTPStatus.OK)

    # 3. Преобразуем JSON-ответ в модель Pydantic
    response_data = GetUserResponseSchema.model_validate_json(response.text)

    # 4. Проверяем, что данные в профиле (/me) совпадают с данными при регистрации
    # Сравниваем ответ GET с тем, что хранится в нашей фикстуре пользователя
    assert_get_user_response(get_user_response=response_data, create_user_response=function_user.response)

    # 5. Валидируем JSON-схему (строгая проверка типов данных)
    validate_json_schema(response.json(), response_data.model_json_schema())

@pytest.mark.users
@pytest.mark.parametrize(
        "email",
        ["mail.ru", "gmail.com", "example.com"]
    )
def test_create_user(email: str, public_users_client: PublicUsersClient):
        """
        Тест проверяет создание пользователя с разными доменами почты.
        """
        # 1. Генерируем email с нужным доменом (mail.ru, потом gmail.com и т.д.)
        generated_email = fake.email(domain=email)

        # 2. Формируем тело запроса (пароль и имя пусть будут случайными)
        request = CreateUserRequestSchema(
            email=generated_email,
            password=fake.password(),
            name=fake.first_name()
        )

        # 3. Отправляем запрос в API на создание пользователя
        response = public_users_client.create_user(request)

        # 4. Проверяем, что email в ответе совпадает с тем, что мы сгенерировали
        assert response.user.email == generated_email