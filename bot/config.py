"""Конфигурация бота"""
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

class Config:
    """Класс конфигурации"""
    # Telegram
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    
    # Файлы
    POSTS_FILE = os.getenv('POSTS_FILE', 'data/posts.json')
    
    # Логирование
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Расписание публикаций (формат: часы через запятую)
    # По умолчанию: 9:00, 15:00, 21:00
    SCHEDULE_HOURS = [9, 15, 21]
    
    # Максимальное количество попыток при ошибке
    MAX_RETRIES = 3
    
    @classmethod
    def validate(cls):
        """Проверка обязательных параметров"""
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN не установлен в переменных окружения")
        if not cls.CHANNEL_ID:
            raise ValueError("CHANNEL_ID не установлен в переменных окружения")
        return True

# Создаем экземпляр конфигурации
config = Config()