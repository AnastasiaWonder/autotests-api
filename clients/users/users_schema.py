from pydantic import BaseModel, Field, EmailStr, ConfigDict

class UserSchema(BaseModel):
    """Описание структуры пользователя."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

class CreateUserRequestSchema(BaseModel):
    """Запрос на создание пользователя."""
    model_config = ConfigDict(populate_by_name=True)

    email: EmailStr
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")

class CreateUserResponseSchema(BaseModel):
    """Ответ сервера при создании пользователя."""
    user: UserSchema

class GetUserResponseSchema(BaseModel):
    """Ответ сервера при получении данных пользователя."""
    user: UserSchema