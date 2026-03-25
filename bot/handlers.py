"""Обработчики команд бота"""
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
import asyncio

from bot.logger import logger
from bot.content_manager import ContentManager
from bot.config import config

router = Router()
content_manager = ContentManager(config.POSTS_FILE)

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    welcome_text = """
🤖 Привет! Я бот для автоматической публикации постов в канал.

Доступные команды:
/start - показать это сообщение
/help - помощь
/publish_now - немедленно опубликовать пост
/stats - статистика постов
/add_post - добавить новый пост (в разработке)
    """
    await message.answer(welcome_text)
    logger.info(f"Пользователь {message.from_user.id} использовал команду /start")

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    help_text = """
📚 Справка по работе бота:

Бот автоматически публикует посты в канал по расписанию:
• Утро (9:00)
• День (15:00)  
• Вечер (21:00)

Посты берутся из файла data/posts.json.
Вы можете редактировать этот файл для изменения контента.

Для ручной публикации используйте команду /publish_now
    """
    await message.answer(help_text)
    logger.info(f"Пользователь {message.from_user.id} использовал команду /help")

@router.message(Command("publish_now"))
async def cmd_publish_now(message: Message):
    """Обработчик команды /publish_now - ручная публикация"""
    await message.answer("🔄 Публикую пост...")
    
    # Импортируем здесь, чтобы избежать циклических импортов
    from bot.main import publish_post
    
    try:
        await publish_post()
        await message.answer("✅ Пост успешно опубликован!")
    except Exception as e:
        error_msg = f"❌ Ошибка публикации: {str(e)}"
        await message.answer(error_msg)
        logger.error(f"Ошибка при ручной публикации: {e}")

@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Обработчик команды /stats - статистика"""
    try:
        with open(config.POSTS_FILE, 'r', encoding='utf-8') as f:
            import json
            posts = json.load(f)
        
        stats_text = f"""
📊 Статистика бота:

📝 Всего постов в базе: {len(posts)}
⏰ Расписание: {', '.join(str(h) + ':00' for h in config.SCHEDULE_HOURS)}
📁 Файл постов: {config.POSTS_FILE}
        """
        await message.answer(stats_text)
    except Exception as e:
        await message.answer(f"❌ Ошибка получения статистики: {e}")
        logger.error(f"Ошибка статистики: {e}")

@router.message(Command("add_post"))
async def cmd_add_post(message: Message):
    """Добавление нового поста (упрощенная версия)"""
    # Для полной реализации нужно сделать машину состояний
    await message.answer(
        "📝 Для добавления поста отредактируйте файл data/posts.json\n"
        "Формат поста:\n"
        '{"type": "text", "content": "Текст поста"}\n'
        '{"type": "photo", "content": "URL фото", "caption": "Подпись"}'
    )