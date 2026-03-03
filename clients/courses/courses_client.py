from typing import TypedDict
import httpx
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserDict

class CreateCourseRequestDict(TypedDict):
    """
    Схема данных для создания курса.
    :param title: Название курса.
    :param maxScore: Максимальный балл.
    :param minScore: Минимальный балл для прохождения.
    :param description: Описание курса.
    :param estimatedTime: Примерное время прохождения (например, '2 weeks').
    :param previewFileId: ID загруженного файла обложки.
    :param createdByUserId: ID пользователя-создателя.
    """
    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    previewFileId: str
    createdByUserId: str

class CoursesClient(APIClient):
    """
    API-клиент для работы с курсами (/api/v1/courses).
    """

    def create_course_api(self, request: CreateCourseRequestDict) -> httpx.Response:
        """
        Выполняет POST-запрос на создание нового курса.
        """
        return self.post("/api/v1/courses", json=request)

    def create_course(self, request: CreateCourseRequestDict) -> dict:
        """
        Создает курс и возвращает JSON-ответ от сервера.
        """
        response = self.create_course_api(request)
        return response.json()

def get_courses_client(user: AuthenticationUserDict) -> CoursesClient:
    """
    Билдер для создания авторизованного экземпляра CoursesClient.
    """
    return CoursesClient(client=get_private_http_client(user))