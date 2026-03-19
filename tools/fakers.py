from faker import Faker

class Fake:
    """
    Класс-обертка для генерации случайных тестовых данных 
    с использованием библиотеки Faker.
    """

    def __init__(self, faker: Faker):
        """
        :param faker: Экземпляр класса Faker.
        """
        self.faker = faker

    def text(self) -> str:
        """Генерирует случайный текст."""
        return self.faker.text()

    def uuid4(self) -> str:
        """Генерирует случайный UUID4 (уникальный идентификатор)."""
        return self.faker.uuid4()

    def email(self) -> str:
        """Генерирует случайный email."""
        return self.faker.email()

    def sentence(self) -> str:
        """Генерирует случайное предложение."""
        return self.faker.sentence()

    def password(self) -> str:
        """Генерирует случайный пароль."""
        return self.faker.password()

    def last_name(self) -> str:
        """Генерирует случайную фамилию."""
        return self.faker.last_name()

    def first_name(self) -> str:
        """Генерирует случайное имя."""
        return self.faker.first_name()

    def middle_name(self) -> str:
        """Генерирует случайное отчество (используем first_name)."""
        return self.faker.first_name()

    def estimated_time(self) -> str:
        """Генерирует строку с временем прохождения (например, '5 weeks')."""
        return f"{self.integer(1, 10)} weeks"

    def integer(self, start: int = 1, end: int = 100) -> int:
        """Генерирует случайное целое число в диапазоне."""
        return self.faker.random_int(start, end)

    def max_score(self) -> int:
        """Генерирует случайный максимальный балл (50-100)."""
        return self.integer(50, 100)

    def min_score(self) -> int:
        """Генерирует случайный минимальный балл (1-30)."""
        return self.integer(1, 30)

# Создаем единственный экземпляр класса для использования во всем проекте
fake = Fake(faker=Faker())