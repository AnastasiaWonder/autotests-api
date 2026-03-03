import time

def get_random_email() -> str:
    """
    Генерирует уникальный email, используя текущее время.
    Это нужно, чтобы каждый раз регистрировать нового пользователя.
    """
    return f"test.{time.time()}@example.com"