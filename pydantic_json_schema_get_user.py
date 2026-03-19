from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import CreateUserRequestSchema, GetUserResponseSchema
from clients.private_http_builder import AuthenticationUserSchema
from tools.assertions.schema import validate_json_schema

# 1. ПОДГОТОВКА: Создаем пользователя
public_client = get_public_users_client()

# Модель CreateUserRequestSchema теперь сама генерирует email, password и имена!
create_request = CreateUserRequestSchema()

# Используем метод .create_user, чтобы отправить сгенерированные данные
create_response = public_client.create_user(create_request)
user_id = create_response.user.id

print(f"Пользователь создан. ID: {user_id}")
print(f"Email из Faker: {create_request.email}")

# 2. ПОЛУЧЕНИЕ ДАННЫХ: Используем PrivateUsersClient
# Берем email и password ПРЯМО из объекта create_request
auth_data = AuthenticationUserSchema(
    email=create_request.email,
    password=create_request.password
)
private_client = get_private_users_client(auth_data)

# Вызываем метод *_api, чтобы получить сырой Response для валидации схемы
response = private_client.get_user_api(user_id)

# 3. ВАЛИДАЦИЯ JSON SCHEMA
expected_schema = GetUserResponseSchema.model_json_schema()

try:
    validate_json_schema(instance=response.json(), schema=expected_schema)
    print("JSON Schema валидация пройдена!")
except Exception as e:
    print(f"Ошибка валидации схемы: {e}")

# Дополнительно проверим, что данные в ответе верные
user_data = GetUserResponseSchema.model_validate_json(response.text)
print(f"Данные из ответа: {user_data.user.email} (совпадает с {create_request.email})")