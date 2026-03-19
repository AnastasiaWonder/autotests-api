from pydantic import BaseModel, Field, EmailStr, ConfigDict
# Импортируем наш экземпляр fake для генерации данных
from tools.fakers import fake

class UserSchema(BaseModel):
    """
    Описание структуры пользователя в ответе от API.
    Здесь данные НЕ генерируются, так как это выходная модель.
    """
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

class CreateUserRequestSchema(BaseModel):
    """
    Схема запроса на создание пользователя.
    Все поля заполняются автоматически при создании объекта.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)

class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа сервера при создании пользователя.
    """
    user: UserSchema

class UpdateUserRequestSchema(BaseModel):
    """
    Схема запроса на обновление данных пользователя.
    Поля могут быть None, но по умолчанию генерируются новые значения.
    """
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr | None = Field(default_factory=fake.email)
    last_name: str | None = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str | None = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str | None = Field(alias="middleName", default_factory=fake.middle_name)

class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа сервера при получении данных пользователя.
    """
    user: UserSchema