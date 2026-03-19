from pydantic import BaseModel, HttpUrl, Field
# Импортируем наш генератор данных
from tools.fakers import fake


class FileSchema(BaseModel):
    """Описание структуры файла в системе (Ответ от API)."""
    id: str
    url: str
    filename: str
    directory: str


class CreateFileRequestSchema(BaseModel):
    """
    Схема данных для загрузки (Запрос к API).
    Теперь поля генерируются автоматически.
    """
    # Генерируем уникальное имя через UUID и добавляем расширение
    filename: str = Field(default_factory=lambda: f"{fake.uuid4()}.png")

    # Директорию фиксируем как "tests", так как нам обычно
    # не нужно плодить кучу разных папок на сервере
    directory: str = Field(default="tests")

    # Это поле остается обязательным, так как путь к файлу на твоем ПК
    # Faker знать не может
    upload_file: str


class CreateFileResponseSchema(BaseModel):
    """Описание структуры ответа сервера при загрузке файла."""
    file: FileSchema