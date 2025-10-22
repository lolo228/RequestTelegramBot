"""Вспомогательные функции"""
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
import logging

logger = logging.getLogger(__name__)


async def add_user_to_chats(bot: Bot, user_id: int, chat_ids: list[str]) -> tuple[list[str], list[str]]:
    """
    Добавляет пользователя в указанные чаты/каналы
    
    Args:
        bot: Экземпляр бота
        user_id: ID пользователя для добавления
        chat_ids: Список ID чатов/каналов
    
    Returns:
        tuple: (список успешных добавлений, список ошибок)
    """
    success = []
    errors = []
    
    for chat_id in chat_ids:
        try:
            # Создаем инвайт-ссылку для пользователя
            invite_link = await bot.create_chat_invite_link(
                chat_id=int(chat_id),
                member_limit=1  # Ссылка только для одного пользователя
            )
            
            # Отправляем ссылку пользователю
            await bot.send_message(
                chat_id=user_id,
                text=f"Вы одобрены! Присоединяйтесь к нашему сообществу:\n{invite_link.invite_link}"
            )
            success.append(chat_id)
            logger.info(f"Создана инвайт-ссылка для пользователя {user_id} в чат {chat_id}")
            
        except TelegramBadRequest as e:
            error_msg = f"Ошибка при создании ссылки для чата {chat_id}: {e}"
            errors.append(error_msg)
            logger.error(error_msg)
        except Exception as e:
            error_msg = f"Неизвестная ошибка для чата {chat_id}: {e}"
            errors.append(error_msg)
            logger.error(error_msg)
    
    return success, errors


def format_application(user_id: int, username: str | None, text: str) -> str:
    """
    Форматирует заявку для отправки администраторам
    
    Args:
        user_id: ID пользователя
        username: Username пользователя (может быть None)
        text: Текст ответа пользователя
    
    Returns:
        str: Отформатированное сообщение
    """
    username_str = f"@{username}" if username else "Не указан"
    
    return (
        f"📝 Новая заявка\n\n"
        f"👤 Пользователь: {username_str}\n"
        f"🆔 ID: {user_id}\n\n"
        f"📋 Ответы:\n{text}"
    )

