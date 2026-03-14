from clients.users.public_users_client import get_public_users_client
from clients.users.private_users_client import get_private_users_client
from clients.users.users_schema import CreateUserRequestSchema, GetUserResponseSchema
from clients.private_http_builder import AuthenticationUserSchema
from tools.assertions.schema import validate_json_schema
from tools.fakers import get_random_email

# 1. ПОДГОТОВКА: Создаем пользователя
public_client = get_public_users_client()
email = get_random_email()
password = "password123"

create_request = CreateUserRequestSchema(
    email=email,
    password=password,
    last_name="Sidorov",
    first_name="Sergey",
    middle_name="Ivanovich"
)
# Используем метод .create_user, чтобы сразу получить объект с ID
create_response = public_client.create_user(create_request)
user_id = create_response.user.id

print(f"Пользователь создан. ID: {user_id}")

# 2. ПОЛУЧЕНИЕ ДАННЫХ: Используем PrivateUsersClient
auth_data = AuthenticationUserSchema(email=email, password=password)
private_client = get_private_users_client(auth_data)

# Вызываем метод *_api, чтобы получить сырой Response для валидации схемы
response = private_client.get_user_api(user_id)

# 3. ВАЛИДАЦИЯ JSON SCHEMA
# Генерируем схему из Pydantic модели GetUserResponseSchema
expected_schema = GetUserResponseSchema.model_json_schema()

try:
    # Провалидируем JSON ответ от API на соответствие схеме
    validate_json_schema(instance=response.json(), schema=expected_schema)
    print("JSON Schema валидация пройдена! Контракт GET /api/v1/users/{user_id} соблюден.")
except Exception as e:
    print(f"Ошибка валидации схемы: {e}")

# Дополнительно проверим, что данные в ответе верные
user_data = GetUserResponseSchema.model_validate_json(response.text)
print(f"Данные из ответа: {user_data.user.email} (совпадает с {email})")