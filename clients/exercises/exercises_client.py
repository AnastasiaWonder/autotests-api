from typing import TypedDict
from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserDict

# --- Схемы данных (Контракты) ---

class Exercise(TypedDict):
    """
    Описание структуры задания (Exercise).
    """
    id: str
    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str

class GetExercisesQueryDict(TypedDict):
    """Параметры для GET /api/v1/exercises"""
    courseId: str  # Обязательный UUID курса

class GetExercisesResponseDict(TypedDict):
    """Структура ответа со списком упражнений."""
    exercises: list[Exercise]

class CreateExerciseResponseDict(TypedDict):
    """Структура ответа при создании упражнения."""
    exercise: Exercise

class CreateExerciseRequestDict(TypedDict):
    """Тело запроса для POST /api/v1/exercises"""
    title: str               # [1, 250] characters
    courseId: str            # uuid4
    maxScore: int | None     # integer | null
    minScore: int | None     # integer | null
    orderIndex: int          # default=0
    description: str         # >= 1 characters
    estimatedTime: str | None # [1, 50] characters | null

class UpdateExerciseRequestDict(TypedDict, total=False):
    """Тело запроса для PATCH /api/v1/exercises/{exercise_id}"""
    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None

# --- Реализация клиента ---

class ExercisesClient(APIClient):
    """
    Клиент для управления упражнениями через API.
    Работает с эндпоинтом /api/v1/exercises.
    """

    # --- Методы, возвращающие Response (низкоуровневые) ---

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """Получение списка упражнений для конкретного курса."""
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """Получение детальной информации об упражнении по его UUID."""
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """Создание нового упражнения (запрос)."""
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """Частичное обновление данных упражнения."""
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """Удаление упражнения по его ID."""
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    # --- Методы, возвращающие JSON (высокоуровневые, требуемые по ДЗ) ---

    def get_exercises(self, query: GetExercisesQueryDict) -> GetExercisesResponseDict:
        """
        Метод получает список упражнений и возвращает JSON.
        """
        response = self.get_exercises_api(query)
        return response.json()

    def get_exercise(self, exercise_id: str) -> dict:
        """
        Метод получает данные одного упражнения и возвращает JSON.
        """
        response = self.get_exercise_api(exercise_id)
        return response.json()

    def create_exercise(self, request: CreateExerciseRequestDict) -> CreateExerciseResponseDict:
        """
        Метод создает упражнение и возвращает JSON-ответ.
        """
        response = self.create_exercise_api(request)
        return response.json()

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestDict) -> dict:
        """
        Метод обновляет упражнение и возвращает JSON.
        """
        response = self.update_exercise_api(exercise_id, request)
        return response.json()

# --- Билдер ---

def get_exercises_client(user: AuthenticationUserDict) -> ExercisesClient:
    """
    Функция создаёт экземпляр ExercisesClient с настроенным приватным HTTP-клиентом.
    :param user: Словарь с данными для авторизации (email, password).
    :return: Настроенный ExercisesClient.
    """
    return ExercisesClient(client=get_private_http_client(user))