from typing import TypedDict
from httpx import Response
from clients.api_client import APIClient

# --- Схемы данных (Контракты) ---

class GetExercisesQueryDict(TypedDict):
    """Параметры для GET /api/v1/exercises"""
    courseId: str  # Обязательный UUID курса

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

    def get_exercises_api(self, query: GetExercisesQueryDict) -> Response:
        """Получение списка упражнений для конкретного курса."""
        return self.get("/api/v1/exercises", params=query)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """Получение детальной информации об упражнении по его UUID."""
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """Создание нового упражнения."""
        return self.post("/api/v1/exercises", json=request)

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestDict) -> Response:
        """Частичное обновление данных упражнения."""
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """Удаление упражнения по его ID."""
        return self.delete(f"/api/v1/exercises/{exercise_id}")