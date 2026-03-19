"""
Демонстрационный скрипт работы с Pydantic-моделями пользователя.
Показывает автоматическую генерацию данных при создании запроса.
"""
from pydantic import Field, EmailStr, ConfigDict
# 1. Подключаем наш генератор данных
from tools.fakers import fake
from clients.users.users_schema import UserSchema, CreateUserResponseSchema, CreateUserRequestSchema

# Примечание: Мы больше не описываем классы здесь,
# так как они уже есть в clients/users/users_schema.py.
# Это делает код чище и профессиональнее.

if __name__ == "__main__":
    print("--- ТЕСТИРУЕМ АВТОМАТИЧЕСКУЮ ГЕНЕРАЦИЮ ---")

    # 2. Создаем запрос. Благодаря default_factory, нам не нужно ничего передавать!
    request_data = CreateUserRequestSchema()

    print(f"Сгенерированный Email: {request_data.email}")
    print(f"Сгенерированное Имя: {request_data.first_name}")
    print(f"Сгенерированный Пароль: {request_data.password}")

    print("\n--- ИМИТАЦИЯ ОТВЕТА ОТ СЕРВЕРА ---")

    # 3. Допустим, сервер ответил нам JSON-ом, используя данные из нашего запроса
    # и добавив сгенерированный ID.
    raw_response = {
        "user": {
            "id": str(fake.uuid4()),  # Имитируем ID от сервера
            "email": request_data.email,
            "lastName": request_data.last_name,
            "firstName": request_data.first_name,
            "middleName": request_data.middle_name
        }
    }

    # 4. Пробуем распаковать данные в модель ответа
    response = CreateUserResponseSchema(**raw_response)

    print(f"Успешно провалидировали ответ для пользователя: {response.user.first_name}")
    print(f"ID пользователя в системе: {response.user.id}")