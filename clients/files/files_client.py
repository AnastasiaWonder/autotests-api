import httpx
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserSchema
# Импортируем наши новые схемы
from clients.files.files_schema import CreateFileRequestSchema, CreateFileResponseSchema

class FilesClient(APIClient):
    """
    API-клиент для работы с файлами (/api/v1/files) на Pydantic.
    """

    def create_file_api(self, request: CreateFileRequestSchema) -> httpx.Response:
        """
        Выполняет POST-запрос для загрузки файла.
        """
        # Вместо request['upload_file'] теперь используем request.upload_file
        with open(request.upload_file, "rb") as f:
            # Отправляем файл. Pydantic-объект позволяет обращаться к полям через точку
            files = {"upload_file": (request.filename, f)}

            # Данные формы (текстовые поля)
            data = {
                "directory": request.directory,
                "filename": request.filename
            }

            return self.post("/api/v1/files", data=data, files=files)

    def create_file(self, request: CreateFileRequestSchema) -> CreateFileResponseSchema:
        """
        Загружает файл и возвращает провалидированный объект ответа.
        """
        response = self.create_file_api(request)
        # Превращаем JSON-текст в объект CreateFileResponseSchema
        return CreateFileResponseSchema.model_validate_json(response.text)

def get_files_client(user: AuthenticationUserSchema) -> FilesClient:
    """
    Билдер для создания авторизованного экземпляра FilesClient.
    """
    return FilesClient(client=get_private_http_client(user))