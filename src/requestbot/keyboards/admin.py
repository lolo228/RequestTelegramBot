"""Клавиатуры для администраторов"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_keyboard(user_id: int) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для модерации заявки
    
    Args:
        user_id: ID пользователя, чья заявка рассматривается
    
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками модерации
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Одобрить",
                    callback_data=f"approve_{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"reject_{user_id}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💬 Отправить сообщение",
                    callback_data=f"message_{user_id}"
                )
            ]
        ]
    )
    return keyboard

