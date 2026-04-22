import pytest
from pydantic import BaseModel, EmailStr

# 1. Импортируем клиента аутентификации
from clients.authentication.authentication_client import AuthenticationClient, get_authentication_client

# 2. Импортируем публичного клиента пользователей
from clients.users.public_users_client import PublicUsersClient, get_public_users_client

# 3. Импортируем приватного клиента пользователей (из его собственного файла)
from clients.users.private_users_client import PrivateUsersClient, get_private_users_client

# 4. Импортируем нужные схемы
from clients.users.users_schema import CreateUserRequestSchema, CreateUserResponseSchema, UserSchema, GetUserResponseSchema
from clients.authentication.authentication_schema import AuthenticationUserSchema

# 1. Модель для хранения данных пользователя в тестах
class UserFixture(BaseModel):
    request: CreateUserRequestSchema
    response: CreateUserResponseSchema

    @property
    def email(self) -> EmailStr:
        return self.request.email

    @property
    def password(self) -> str:
        return self.request.password

    # ТО САМОЕ НОВОЕ СВОЙСТВО: формирует данные для авторизации
    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        return AuthenticationUserSchema(email=self.email, password=self.password)

# 2. Фикстура для обычного клиента (без авторизации)
@pytest.fixture
def authentication_client() -> AuthenticationClient:
    return get_authentication_client()

# 3. Фикстура для клиента пользователей (публичный API)
@pytest.fixture
def public_users_client() -> PublicUsersClient:
    return get_public_users_client()

# 4. Фикстура для создания пользователя (Function scope по умолчанию)
@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)
    return UserFixture(request=request, response=response)

# 5. НОВАЯ ФИКСТУРА: Приватный клиент, который уже "знает" нашего пользователя
@pytest.fixture
def private_users_client(function_user: UserFixture) -> PrivateUsersClient:
    # Мы передаем в билдер наше новое свойство authentication_user
    return get_private_users_client(function_user.authentication_user)