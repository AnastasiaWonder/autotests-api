from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    """
    Модель данных пользователя, используемая в ответах API.
    Содержит полную информацию о пользователе, включая его ID.
    """
    id: str = Field(description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(description="Электронная почта пользователя")
    last_name: str = Field(alias="lastName", description="Фамилия")
    first_name: str = Field(alias="firstName", description="Имя")
    middle_name: str = Field(alias="middleName", description="Отчество")

    # Настройка для работы с алиасами
    model_config = {
        "populate_by_name": True
    }

class CreateUserRequestSchema(BaseModel):
    """
    Схема запроса на создание нового пользователя (POST /api/v1/users).
    Не содержит id, так как он генерируется сервером.
    """
    email: EmailStr = Field(description="Электронная почта для регистрации")
    password: str = Field(description="Пароль пользователя")
    last_name: str = Field(alias="lastName", description="Фамилия")
    first_name: str = Field(alias="firstName", description="Имя")
    middle_name: str = Field(alias="middleName", description="Отчество")

    model_config = {
        "populate_by_name": True
    }

class CreateUserResponseSchema(BaseModel):
    """
    Схема ответа сервера после успешного создания пользователя.
    Оборачивает объект UserSchema в ключ 'user'.
    """
    user: UserSchema = Field(description="Объект с данными созданного пользователя")


if __name__ == "__main__":
    # Пример данных от сервера (JSON)
    raw_data = {
        "user": {
            "id": "123-uuid",
            "email": "nastya@example.com",
            "lastName": "Nazarenko",
            "firstName": "Anastasia",
            "middleName": "Testing"
        }
    }

    # Пробуем распаковать данные в модель
    response = CreateUserResponseSchema(**raw_data)
    print(f"Успешно создали пользователя: {response.user.first_name}")