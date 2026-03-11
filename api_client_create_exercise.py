"""
Скрипт автоматического создания цепочки сущностей на Pydantic:
Пользователь -> Файл -> Курс -> Упражнение.
"""
from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema

from clients.files.files_client import get_files_client
from clients.files.files_schema import CreateFileRequestSchema

from clients.courses.courses_client import get_courses_client
from clients.courses.courses_schema import CreateCourseRequestSchema

from clients.exercises.exercises_client import get_exercises_client
from clients.exercises.exercises_schema import CreateExerciseRequestSchema

from clients.private_http_builder import AuthenticationUserSchema
from tools.fakers import get_random_email


def run():
    # 1. Создаем пользователя (Public)
    public_users_client = get_public_users_client()

    # Используем Схему и snake_case (last_name вместо lastName)
    user_request = CreateUserRequestSchema(
        email=get_random_email(),
        password="password123",
        last_name="Nazarenko",
        first_name="Anastasia",
        middle_name="Testing"
    )
    user_response = public_users_client.create_user(user_request)

    # Достаем ID через точку — PyCharm тебе подскажет!
    user_id = user_response.user.id
    print(f"✅ User created: {user_id}")

    # 2. Инициализируем данные для авторизации (BaseModel)
    auth_user = AuthenticationUserSchema(
        email=user_request.email,
        password=user_request.password
    )

    # Инициализируем клиенты
    files_client = get_files_client(auth_user)
    courses_client = get_courses_client(auth_user)
    exercises_client = get_exercises_client(auth_user)

    # 3. Загружаем файл
    file_request = CreateFileRequestSchema(
        filename="exercise_image.png",
        directory="courses",
        upload_file="./testdata/files/image.png"
    )
    file_data = files_client.create_file(file_request)
    # Здесь Pydantic сам проверит структуру, если сервер вернет ошибку,
    # мы узнаем об этом на этапе валидации.
    print(f"✅ File uploaded: {file_data.file.url}")

    # 4. Создаем курс
    course_request = CreateCourseRequestSchema(
        title="Python API Course with Pydantic",
        max_score=100,
        min_score=10,
        description="Курс по автоматизации тестирования API",
        estimated_time="2 weeks",
        preview_file_id=file_data.file.id,  # Точка решает!
        created_by_user_id=user_id
    )
    course_data = courses_client.create_course(course_request)
    print(f"✅ Course created: {course_data.course.id}")

    # 5. Создаем задание (Exercise)
    exercise_request = CreateExerciseRequestSchema(
        title="Exercise 1: Pydantic Power",
        course_id=course_data.course.id,
        max_score=5,
        min_score=1,
        order_index=0,
        description="Написание первого автотеста на объектах",
        estimated_time="5 minutes"
    )
    exercise_data = exercises_client.create_exercise(exercise_request)

    print("-" * 30)
    print("🎯 ВСЯ ЦЕПОЧКА УСПЕШНО СОЗДАНА!")
    print(f"ID Упражнения: {exercise_data.exercise.id}")
    print(f"Название: {exercise_data.exercise.title}")
    print("-" * 30)


if __name__ == "__main__":
    run()