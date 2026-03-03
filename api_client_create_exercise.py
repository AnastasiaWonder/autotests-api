"""
Скрипт автоматического создания цепочки сущностей:
Пользователь -> Файл -> Курс -> Упражнение.
"""
from clients.users.public_users_client import get_public_users_client, CreateUserRequestDict
from clients.files.files_client import get_files_client, CreateFileRequestDict
from clients.courses.courses_client import get_courses_client, CreateCourseRequestDict
from clients.exercises.exercises_client import get_exercises_client, CreateExerciseRequestDict, GetExercisesQueryDict
from clients.private_http_builder import AuthenticationUserDict
from tools.fakers import get_random_email

def run():
    # 1. Создаем пользователя (Public)
    public_users_client = get_public_users_client()
    user_request = CreateUserRequestDict(
        email=get_random_email(),
        password="password123",
        lastName="Nazarenko",
        firstName="Anastasia",
        middleName="Testing"
    )
    user_response = public_users_client.create_user(user_request)
    # Нам нужен ID юзера для создания курса позже
    user_id = user_response['user']['id']

    # 2. Инициализируем приватные клиенты
    auth_user = AuthenticationUserDict(
        email=user_request['email'],
        password=user_request['password']
    )
    files_client = get_files_client(auth_user)
    courses_client = get_courses_client(auth_user)
    exercises_client = get_exercises_client(auth_user)

    # 3. Загружаем файл
    file_request = CreateFileRequestDict(
        filename="image.png",
        directory="courses",
        upload_file="./testdata/files/image.png" # Путь к файлу в твоем проекте
    )
    file_data = files_client.create_file(file_request)
    print(f"Create file data: {file_data}")

    if 'detail' in file_data:
        print(f"ОШИБКА ОТ СЕРВЕРА: {file_data['detail']}")
        return  # Останавливаем выполнение, чтобы не было KeyError

    # 4. Создаем курс
    course_request = CreateCourseRequestDict(
        title="Python API Course",
        maxScore=100,
        minScore=10,
        description="Курс по автоматизации тестирования API",
        estimatedTime="2 weeks",
        previewFileId=file_data['file']['id'],
        createdByUserId=user_id
    )
    course_data = courses_client.create_course(course_request)
    print(f'Create course data: {course_data}')

    # 5. Создаем задание (Exercise)
    exercise_request = CreateExerciseRequestDict(
        title="Exercise 1",
        courseId=course_data['course']['id'], # Передаем ID созданного курса
        maxScore=5,
        minScore=1,
        orderIndex=0,
        description="Написание первого автотеста",
        estimatedTime="5 minutes"
    )
    exercise_data = exercises_client.create_exercise(exercise_request)
    print(f'Create exercise data: {exercise_data}')

if __name__ == "__main__":
    run()