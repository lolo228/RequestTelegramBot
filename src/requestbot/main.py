"""Главный файл для запуска бота"""
import asyncio
import logging
import sys
from pathlib import Path

# Добавляем корневую директорию в путь для корректных импортов
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.requestbot.config import settings
from src.requestbot.handlers import user_router, admin_router

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Главная функция запуска бота"""
    logger.info("Запуск бота...")
    
    # Инициализация бота и диспетчера
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    
    # Регистрация роутеров
    dp.include_router(user_router)
    dp.include_router(admin_router)
    
    logger.info("Бот запущен и готов к работе!")
    
    # Запуск polling
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")

