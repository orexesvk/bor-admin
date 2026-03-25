"""Управление контентом для публикаций"""
import json
import random
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
import aiohttp
from datetime import datetime

from bot.logger import logger

class ContentManager:
    """Класс для управления контентом"""
    
    def __init__(self, posts_file: str):
        """
        Инициализация менеджера контента
        
        Args:
            posts_file: Путь к JSON файлу с постами
        """
        self.posts_file = Path(posts_file)
        self.posts: List[Dict[str, Any]] = []
        self.load_posts()
    
    def load_posts(self) -> None:
        """Загрузка постов из JSON файла"""
        try:
            if self.posts_file.exists():
                with open(self.posts_file, 'r', encoding='utf-8') as f:
                    self.posts = json.load(f)
                logger.info(f"Загружено {len(self.posts)} постов из {self.posts_file}")
            else:
                # Создаем файл с примерами, если его нет
                self.create_example_posts()
                logger.warning(f"Файл {self.posts_file} не найден. Создан файл с примерами.")
        except Exception as e:
            logger.error(f"Ошибка загрузки постов: {e}")
            self.posts = []
    
    def create_example_posts(self) -> None:
        """Создание файла с примерами постов"""
        example_posts = [
            {
                "type": "text",
                "content": "🌟 Доброе утро! Начните свой день с улыбки!\n\nСегодня отличный день для новых достижений!",
                "tags": ["morning", "motivation"]
            },
            {
                "type": "photo",
                "content": "https://picsum.photos/800/600",
                "caption": "Красивый пейзаж для вдохновения 📸"
            },
            {
                "type": "text",
                "content": "💡 Интересный факт: Python был создан в 1991 году Гвидо ван Россумом и назван в честь комедийного шоу 'Летающий цирк Монти Пайтона'."
            },
            {
                "type": "text",
                "content": "🚀 Прогресс не стоит на месте! Каждый день мы становимся лучше.\n\n#мотивация #развитие"
            },
            {
                "type": "link",
                "content": "https://github.com/python-telegram-bot",
                "caption": "Отличная библиотека для создания Telegram ботов! 🔧"
            }
        ]
        
        # Создаем директорию, если её нет
        self.posts_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.posts_file, 'w', encoding='utf-8') as f:
            json.dump(example_posts, f, ensure_ascii=False, indent=2)
        
        self.posts = example_posts
    
    def get_next_post(self) -> Optional[Dict[str, Any]]:
        """
        Получение следующего поста для публикации (циклический обход)
        
        Returns:
            Словарь с данными поста или None
        """
        if not self.posts:
            logger.warning("Нет доступных постов для публикации")
            return None
        
        # Простой циклический обход (можно заменить на случайный выбор)
        # Для демонстрации используем случайный выбор
        post = random.choice(self.posts)
        logger.info(f"Выбран пост для публикации: {post.get('type', 'unknown')}")
        return post
    
    async def generate_ai_content(self, prompt: str = None) -> Optional[str]:
        """
        Генерация контента через AI (пример с использованием Hugging Face API)
        
        Args:
            prompt: Подсказка для генерации
        
        Returns:
            Сгенерированный текст или None при ошибке
        """
        # Это пример интеграции с AI API
        # Для работы нужно добавить API ключ в конфигурацию
        
        # Пример с имитацией AI генерации
        templates = [
            "🌟 Сегодняшняя мудрость: {topic}",
            "💡 Идея дня: {topic}",
            "🚀 Вдохновение: {topic}"
        ]
        
        topics = [
            "успех приходит к тем, кто не останавливается на достигнутом",
            "каждый день - это новая возможность",
            "делай сегодня то, что приблизит тебя к мечте"
        ]
        
        if prompt:
            topic = prompt
        else:
            topic = random.choice(topics)
        
        result = random.choice(templates).format(topic=topic)
        
        logger.info(f"Сгенерирован AI контент: {result[:50]}...")
        return result
    
    def add_post(self, post_data: Dict[str, Any]) -> bool:
        """
        Добавление нового поста
        
        Args:
            post_data: Данные поста
            
        Returns:
            True если успешно, иначе False
        """
        try:
            self.posts.append(post_data)
            with open(self.posts_file, 'w', encoding='utf-8') as f:
                json.dump(self.posts, f, ensure_ascii=False, indent=2)
            logger.info(f"Добавлен новый пост: {post_data.get('type', 'unknown')}")
            return True
        except Exception as e:
            logger.error(f"Ошибка добавления поста: {e}")
            return False