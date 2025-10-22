"""Клавиатуры для пользователей"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_reply_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопкой "Ответить"
    
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой ответа
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Ответить",
                    callback_data="reply_to_admin"
                )
            ]
        ]
    )
    return keyboard

