"""
Скрипт автоматического создания цепочки сущностей на Pydantic:
Пользователь -> Файл -> Курс -> Упражнение.
С использованием автоматической генерации данных (Faker) в моделях.
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


def run():
    # 1. Создаем пользователя
    # Данные (email, password, name) теперь генерируются автоматически внутри модели
    public_users_client = get_public_users_client()
    user_request = CreateUserRequestSchema()
    user_response = public_users_client.create_user(user_request)

    user_id = user_response.user.id
    print(f"User created: {user_id} ({user_request.email})")

    # 2. Инициализируем данные для авторизации
    # Используем данные, которые сгенерировались в user_request
    auth_user = AuthenticationUserSchema(
        email=user_request.email,
        password=user_request.password
    )

    # Инициализируем клиенты
    files_client = get_files_client(auth_user)
    courses_client = get_courses_client(auth_user)
    exercises_client = get_exercises_client(auth_user)

    # 3. Загружаем файл
    # filename и directory генерируются моделью, передаем только путь к физическому файлу
    file_request = CreateFileRequestSchema(
        upload_file="./testdata/files/image.png"
    )
    file_data = files_client.create_file(file_request)
    print(f"File uploaded: {file_data.file.url}")

    # 4. Создаем курс
    # title, scores, description и т.д. — автоматические.
    # Передаем только связки: ID файла и ID автора.
    course_request = CreateCourseRequestSchema(
        preview_file_id=file_data.file.id,
        created_by_user_id=user_id
    )
    course_data = courses_client.create_course(course_request)
    print(f"Course created: {course_data.course.id}")

    # 5. Создаем задание (Exercise)
    # Почти все поля заполнены фейками, привязываем только к ID курса.
    exercise_request = CreateExerciseRequestSchema(
        course_id=course_data.course.id
    )
    exercise_data = exercises_client.create_exercise(exercise_request)

    print("-" * 30)
    print("ВСЯ ЦЕПОЧКА УСПЕШНО СОЗДАНА!")
    print(f"ID Упражнения: {exercise_data.exercise.id}")
    print(f"Название (сгенерировано): {exercise_data.exercise.title}")
    print(f"Баллы: {exercise_data.exercise.min_score} - {exercise_data.exercise.max_score}")
    print("-" * 30)


if __name__ == "__main__":
    run()