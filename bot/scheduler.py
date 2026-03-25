"""Планировщик публикаций"""
import asyncio
from typing import List, Callable, Any
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from bot.logger import logger

class PostScheduler:
    """Класс для планирования публикаций"""
    
    def __init__(self):
        """Инициализация планировщика"""
        self.scheduler = AsyncIOScheduler()
        self.jobs: List[str] = []
    
    def add_schedule(self, func: Callable, hours: List[int], *args, **kwargs) -> None:
        """
        Добавление расписания публикаций
        
        Args:
            func: Функция для выполнения
            hours: Список часов для публикации
            *args: Аргументы для функции
            **kwargs: Ключевые аргументы для функции
        """
        for hour in hours:
            # Создаем триггер для каждого часа
            trigger = CronTrigger(hour=hour, minute=0)
            job = self.scheduler.add_job(
                func,
                trigger,
                args=args,
                kwargs=kwargs,
                id=f"post_{hour}",
                replace_existing=True
            )
            self.jobs.append(job.id)
            logger.info(f"Запланирована публикация на {hour}:00")
    
    def start(self) -> None:
        """Запуск планировщика"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("Планировщик запущен")
        else:
            logger.warning("Планировщик уже запущен")
    
    def stop(self) -> None:
        """Остановка планировщика"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Планировщик остановлен")
    
    def list_jobs(self) -> List[str]:
        """
        Получение списка запланированных задач
        
        Returns:
            Список ID задач
        """
        return self.jobs