from typing import TypedDict
import httpx
from clients.api_client import APIClient
from clients.private_http_builder import get_private_http_client, AuthenticationUserDict


class CreateFileRequestDict(TypedDict):
    """
    Схема данных для загрузки файла.
    :param filename: Имя файла для сохранения на сервере.
    :param directory: Директория на сервере (например, 'courses').
    :param upload_file: Локальный путь к файлу (например, './testdata/files/image.png').
    """
    filename: str
    directory: str
    upload_file: str


class FilesClient(APIClient):
    """
    API-клиент для работы с файлами (/api/v1/files).
    """

    def create_file_api(self, request: CreateFileRequestDict) -> httpx.Response:
        """
        Выполняет POST-запрос для загрузки файла.
        Поля приведены в соответствие с требованиями сервера (upload_file и filename).
        """
        with open(request['upload_file'], "rb") as f:
            # Отправляем файл под ключом 'upload_file'
            files = {"upload_file": (request['filename'], f)}

            # Передаем 'filename' и 'directory' как обычные текстовые поля
            data = {
                "directory": request['directory'],
                "filename": request['filename']
            }

            return self.post("/api/v1/files", data=data, files=files)

    def create_file(self, request: CreateFileRequestDict) -> dict:
        """
        Загружает файл и возвращает JSON-ответ от сервера.
        """
        response = self.create_file_api(request)
        return response.json()


def get_files_client(user: AuthenticationUserDict) -> FilesClient:
    """
    Билдер для создания авторизованного экземпляра FilesClient.
    """
    return FilesClient(client=get_private_http_client(user))