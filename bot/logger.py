"""Настройка логирования"""
import logging
import sys

def setup_logger(level: str = "INFO"):
    """
    Настройка логгера для всего приложения
    
    Args:
        level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
    """
    # Создаем логгер
    logger = logging.getLogger(__name__)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))
    
    # Формат логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Добавляем обработчик к корневому логгеру
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(getattr(logging, level.upper()))
    
    return logger

# Глобальный логгер
logger = setup_logger()