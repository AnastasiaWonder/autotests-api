from pydantic import BaseModel, HttpUrl

class FileSchema(BaseModel):
    """Описание структуры файла в системе."""
    id: str
    url: str  # Можно использовать HttpUrl, если сервер всегда присылает валидный URL
    filename: str
    directory: str

class CreateFileRequestSchema(BaseModel):
    """Схема данных для загрузки (то, что мы заполняем в скрипте)."""
    filename: str
    directory: str
    upload_file: str  # Это локальный путь к файлу на твоем ПК

class CreateFileResponseSchema(BaseModel):
    """То, что прилетает от сервера в ответ на загрузку."""
    file: FileSchema