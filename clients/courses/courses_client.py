import httpx
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
# Импортируем наши новые схемы
from clients.courses.courses_schema import CreateCourseRequestSchema, CreateCourseResponseSchema

class CoursesClient(APIClient):
    """
    API-клиент для работы с курсами (/api/v1/courses).
    """

    def create_course_api(self, request: CreateCourseRequestSchema) -> httpx.Response:
        """
        Выполняет POST-запрос на создание нового курса.
        """
        return self.post(
            "/api/v1/courses",
            # Превращаем модель в словарь, заменяя snake_case на camelCase для API
            json=request.model_dump(by_alias=True)
        )

    def create_course(self, request: CreateCourseRequestSchema) -> CreateCourseResponseSchema:
        """
        Создает курс и возвращает провалидированный объект ответа.
        """
        response = self.create_course_api(request)
        # Превращаем текст ответа (JSON) сразу в красивый объект Pydantic
        return CreateCourseResponseSchema.model_validate_json(response.text)

def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Билдер для создания авторизованного экземпляра CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))