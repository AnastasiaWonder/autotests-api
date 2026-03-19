"""
Сценарий создания полной цепочки сущностей:
Пользователь -> Файл -> Курс.
Используется автоматическая генерация данных через Pydantic + Faker.
"""
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema
from clients.private_http_builder import AuthenticationUserSchema

# 1. СОЗДАЕМ ПОЛЬЗОВАТЕЛЯ (Публичный клиент)
# Все данные (email, password, имена) теперь генерируются автоматически
public_users_client = get_public_users_client()
user_request = CreateUserRequestSchema()
user_response = public_users_client.create_user(user_request)

print(f"Пользователь создан. ID: {user_response.user.id}")

# 2. ГОТОВИМ ДАННЫЕ ДЛЯ АВТОРИЗАЦИИ
# Используем те данные, которые модель user_request сгенерировала внутри себя
auth_user = AuthenticationUserSchema(
    email=user_request.email,
    password=user_request.password
)

# Инициализируем клиенты для работы с защищенными методами
files_client = get_files_client(auth_user)
courses_client = get_courses_client(auth_user)

# 3. ЗАГРУЖАЕМ ФАЙЛ (Превью для курса)
# Filename и directory теперь создаются автоматически.
# Передаем только upload_file — путь к реальному файлу.
file_request = CreateFileRequestSchema(
    upload_file="./testdata/files/image.png"
)
file_response = files_client.create_file(file_request)

print(f"Файл загружен. URL: {file_response.file.url}")

# 4. СОЗДАЕМ КУРС
# Title, scores, description и время теперь автоматические.
# Нам ВАЖНО передать только связки (ID), иначе сервер не поймет, к кому привязать курс.
course_request = CreateCourseRequestSchema(
    preview_file_id=file_response.file.id,
    created_by_user_id=user_response.user.id
)

course_response = courses_client.create_course(course_request)

print("-" * 30)
print("КУРС УСПЕШНО СОЗДАН!")
print(f"Название (Faker): {course_response.course.title}")
print(f"Баллы: {course_response.course.min_score} - {course_response.course.max_score}")
print(f"Создатель: {course_response.course.created_by_user.email}")
print("-" * 30)