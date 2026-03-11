from clients.courses.courses_client import get_courses_client
from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema
from clients.private_http_builder import AuthenticationUserSchema
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema
from tools.fakers import get_random_email
# Импортируем нашу новую схему для курса
from clients.courses.courses_schema import CreateCourseRequestSchema

# 1. Создаем пользователя (публичный клиент)
public_users_client = get_public_users_client()

user_request = CreateUserRequestSchema(
    email=get_random_email(),
    password="strong_password123",
    last_name="Nazarenko",
    first_name="Anastasia",
    middle_name="Testing"
)
user_response = public_users_client.create_user(user_request)
print(f"✅ Пользователь создан. ID: {user_response.user.id}")

# 2. Готовим данные для авторизации (используем Pydantic-модель)
auth_user = AuthenticationUserSchema(
    email=user_request.email,
    password=user_request.password
)

# 3. Загружаем файл (превью для курса)
files_client = get_files_client(auth_user)
file_request = CreateFileRequestSchema(
    filename="course_cover.png",
    directory="covers",
    upload_file="./testdata/files/image.png" # Убедись, что файл тут лежит!
)
file_response = files_client.create_file(file_request)
print(f"✅ Файл загружен. URL: {file_response.file.url}")

# 4. Создаем курс (используем данные из предыдущих шагов)
courses_client = get_courses_client(auth_user)

course_request = CreateCourseRequestSchema(
    title="Pydantic Mastery",
    max_score=100,
    min_score=10,
    description="Курс по глубокому изучению Pydantic",
    estimated_time="3 weeks",
    preview_file_id=file_response.file.id,    # Берем ID через точку
    created_by_user_id=user_response.user.id  # Берем ID через точку
)

course_response = courses_client.create_course(course_request)

print("-" * 30)
print("🚀 КУРС УСПЕШНО СОЗДАН!")
print(f"Название: {course_response.course.title}")
print(f"Создатель: {course_response.course.created_by_user.email}")
print("-" * 30)