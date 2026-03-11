from httpx import Response
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
# Импортируем наши новые схемы
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema, CreateExerciseResponseSchema,
    UpdateExerciseRequestSchema, GetExercisesResponseSchema,
    GetExercisesQuerySchema, ExerciseSchema
)

class ExercisesClient(APIClient):
    """
    Клиент для управления упражнениями через API с использованием Pydantic.
    """

    # --- Низкоуровневые методы (API) ---

    def get_exercises_api(self, query: GetExercisesQuerySchema) -> Response:
        """Получение списка упражнений. Теперь используем model_dump для параметров."""
        return self.get("/api/v1/exercises", params=query.model_dump(by_alias=True))

    def get_exercise_api(self, exercise_id: str) -> Response:
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        return self.post("/api/v1/exercises", json=request.model_dump(by_alias=True))

    def update_exercise_api(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> Response:
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request.model_dump(by_alias=True))

    def delete_exercise_api(self, exercise_id: str) -> Response:
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    # --- Высокоуровневые методы (Business logic) ---

    def get_exercises(self, query: GetExercisesQuerySchema) -> GetExercisesResponseSchema:
        response = self.get_exercises_api(query)
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def get_exercise(self, exercise_id: str) -> ExerciseSchema:
        # Теперь возвращаем конкретную схему упражнения, обернув ответ
        response = self.get_exercise_api(exercise_id)
        # Если в ответе от сервера ключ "exercise", убедись, как выглядит JSON.
        # Обычно GET возвращает сразу объект упражнения.
        return ExerciseSchema.model_validate_json(response.text)

    def create_exercise(self, request: CreateExerciseRequestSchema) -> CreateExerciseResponseSchema:
        response = self.create_exercise_api(request)
        return CreateExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(self, exercise_id: str, request: UpdateExerciseRequestSchema) -> ExerciseSchema:
        response = self.update_exercise_api(exercise_id, request)
        return ExerciseSchema.model_validate_json(response.text)

# --- Билдер ---

def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """Создаёт экземпляр клиента, принимая Pydantic-модель пользователя."""
    return ExercisesClient(client=get_private_http_client(user))