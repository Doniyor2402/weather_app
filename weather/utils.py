from datetime import datetime


def convert_seconds_to_data(seconds: int, timezone: int):
    """Конвертируем секунды в удобный формат учитывая часовой пояс"""
    return datetime.utcfromtimestamp(seconds + timezone).strftime("%H:%M:%S")
