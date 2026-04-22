from clients.users.users_schema import UserSchema, GetUserResponseSchema, CreateUserResponseSchema
from tools.assertions.base import assert_equal

def assert_user(actual: UserSchema, expected: UserSchema):
    """Сравнивает поля двух объектов UserSchema с указанием имени поля."""
    # Добавляем третий аргумент — название поля
    assert_equal(actual.id, expected.id, "ID пользователя")
    assert_equal(actual.email, expected.email, "Email пользователя")
    assert_equal(actual.first_name, expected.first_name, "Имя пользователя")
    assert_equal(actual.last_name, expected.last_name, "Фамилия пользователя")
    assert_equal(actual.middle_name, expected.middle_name, "Отчество пользователя")

def assert_get_user_response(get_user_response: GetUserResponseSchema, create_user_response: CreateUserResponseSchema):
    """Проверка ответа эндпоинта /me."""
    assert_user(
        actual=get_user_response.user,
        expected=create_user_response.user
    )