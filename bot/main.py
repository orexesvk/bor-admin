"""Основной файл для запуска бота"""
import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent.parent))

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import config
from bot.logger import logger
from bot.handlers import router
from bot.scheduler import PostScheduler
from bot.content_manager import ContentManager

# Глобальные объекты
bot = None
dp = None
scheduler = None
content_manager = None

async def publish_post() -> bool:
    """
    Функция публикации поста в канал
    
    Returns:
        True если успешно, иначе False
    """
    global bot, content_manager
    
    if not bot:
        logger.error("Бот не инициализирован")
        return False
    
    try:
        # Получаем следующий пост
        post = content_manager.get_next_post()
        
        if not post:
            logger.warning("Нет доступных постов для публикации")
            return False
        
        post_type = post.get('type', 'text')
        content = post.get('content', '')
        caption = post.get('caption', '')
        
        # Публикуем в зависимости от типа
        if post_type == 'text':
            await bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=content,
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Опубликован текстовый пост: {content[:50]}...")
            
        elif post_type == 'photo':
            # Отправляем фото по URL
            await bot.send_photo(
                chat_id=config.CHANNEL_ID,
                photo=content,
                caption=caption or "📸 Новое фото",
                parse_mode=ParseMode.HTML
            )
            logger.info(f"Опубликовано фото: {content}")
            
        elif post_type == 'link':
            # Отправляем ссылку с превью
            await bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=f"🔗 {caption}\n\n{content}" if caption else f"🔗 {content}",
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False
            )
            logger.info(f"Опубликована ссылка: {content}")
            
        else:
            logger.error(f"Неизвестный тип поста: {post_type}")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Ошибка публикации поста: {e}", exc_info=True)
        return False

async def main():
    """Основная функция запуска бота"""
    global bot, dp, scheduler, content_manager
    
    try:
        # Проверяем конфигурацию
        config.validate()
        logger.info("Конфигурация проверена успешно")
        
        # Инициализируем менеджер контента
        content_manager = ContentManager(config.POSTS_FILE)
        
        # Создаем бота и диспетчер
        bot = Bot(
            token=config.BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        dp = Dispatcher()
        
        # Подключаем роутер с обработчиками
        dp.include_router(router)
        
        # Настраиваем планировщик
        scheduler = PostScheduler()
        scheduler.add_schedule(publish_post, config.SCHEDULE_HOURS)
        scheduler.start()
        
        # Проверяем доступ к каналу
        try:
            chat = await bot.get_chat(config.CHANNEL_ID)
            logger.info(f"Бот добавлен в канал: {chat.title}")
        except Exception as e:
            logger.error(f"Ошибка доступа к каналу: {e}")
            logger.error("Убедитесь, что бот добавлен в канал и имеет права администратора")
            return
        
        logger.info("Бот успешно запущен!")
        
        # Запускаем polling
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
        raise
    finally:
        if scheduler:
            scheduler.stop()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Необработанная ошибка: {e}", exc_info=True)
        sys.exit(1)