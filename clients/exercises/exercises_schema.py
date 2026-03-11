from pydantic import BaseModel, Field, ConfigDict

class ExerciseSchema(BaseModel):
    """Базовая структура упражнения."""
    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")

class GetExercisesQuerySchema(BaseModel):
    """Схема параметров для GET запроса."""
    model_config = ConfigDict(populate_by_name=True)
    course_id: str = Field(alias="courseId")

class GetExercisesResponseSchema(BaseModel):
    """Ответ со списком упражнений."""
    exercises: list[ExerciseSchema]

class CreateExerciseRequestSchema(BaseModel):
    """Тело запроса на создание."""
    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(alias="courseId")
    max_score: int | None = Field(alias="maxScore", default=None)
    min_score: int | None = Field(alias="minScore", default=None)
    order_index: int = Field(alias="orderIndex", default=0)
    description: str
    estimated_time: str | None = Field(alias="estimatedTime", default=None)

# ВОТ ЭТОТ КЛАСС СКОРЕЕ ВСЕГО ПРОПУЩЕН:
class UpdateExerciseRequestSchema(BaseModel):
    """Тело запроса на частичное обновление."""
    model_config = ConfigDict(populate_by_name=True)

    title: str | None = None
    max_score: int | None = Field(alias="maxScore", default=None)
    min_score: int | None = Field(alias="minScore", default=None)
    order_index: int | None = Field(alias="orderIndex", default=None)
    description: str | None = None
    estimated_time: str | None = Field(alias="estimatedTime", default=None)

class CreateExerciseResponseSchema(BaseModel):
    """Ответ при создании упражнения."""
    exercise: ExerciseSchema