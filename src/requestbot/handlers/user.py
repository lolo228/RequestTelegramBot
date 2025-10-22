"""Обработчики для пользователей"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from ..config import settings
from ..keyboards import get_admin_keyboard
from ..utils import ApplicationForm, UserReply
from ..utils.helpers import format_application

router = Router(name="user")


# Текст с вопросами для пользователя
QUESTIONS_TEXT = """
Пожалуйста, ответьте на следующие вопросы одним сообщением:

1. Возраст?
2. Опишите ваш опыт работы в нескольких словах?
3. Опишите ваш опыт в общении с людьми?
4. Готовы ли вы обучиться работе с нами?
5. Откуда узнали о нас?

Отправьте все ответы одним сообщением.
"""


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start
    Отправляет пользователю вопросы анкеты
    """
    await message.answer(QUESTIONS_TEXT)
    await state.set_state(ApplicationForm.waiting_for_answer)


@router.message(ApplicationForm.waiting_for_answer)
async def process_application(message: Message, state: FSMContext):
    """
    Обработчик ответа пользователя на вопросы
    Отправляет заявку в чат администраторов
    """
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение с ответами.")
        return
    
    # Отправляем подтверждение пользователю
    await message.answer("✅ Ваш ответ принят, ожидайте решения администрации!")
    
    # Очищаем состояние
    await state.clear()
    
    # Форматируем заявку
    application_text = format_application(
        user_id=message.from_user.id,
        username=message.from_user.username,
        text=message.text
    )
    
    # Отправляем заявку администраторам с кнопками
    try:
        await message.bot.send_message(
            chat_id=settings.ADMIN_CHAT_ID,
            text=application_text,
            reply_markup=get_admin_keyboard(message.from_user.id)
        )
    except Exception as e:
        # Логируем ошибку, но не сообщаем пользователю
        print(f"Ошибка при отправке заявки администраторам: {e}")


@router.callback_query(F.data == "reply_to_admin")
async def reply_to_admin_button(callback: CallbackQuery, state: FSMContext):
    """
    Обработчик кнопки "Ответить"
    Активирует режим ответа администраторам
    """
    await callback.answer()
    await callback.message.answer(
        "📝 Отправьте ваше сообщение, и оно будет переслано администраторам."
    )
    await state.set_state(UserReply.waiting_for_reply)


@router.message(UserReply.waiting_for_reply)
async def process_user_reply(message: Message, state: FSMContext):
    """
    Обработчик сообщения-ответа от пользователя
    Пересылает сообщение в чат администраторов
    """
    # Формируем сообщение для админов
    username_str = f"@{message.from_user.username}" if message.from_user.username else "Не указан"
    admin_text = (
        f"💬 Ответ от пользователя\n\n"
        f"👤 Пользователь: {username_str}\n"
        f"🆔 ID: {message.from_user.id}\n\n"
        f"📨 Сообщение:\n{message.text if message.text else '[Медиа-контент]'}"
    )
    
    try:
        # Отправляем сообщение в админ чат
        if message.text:
            await message.bot.send_message(
                chat_id=settings.ADMIN_CHAT_ID,
                text=admin_text
            )
        else:
            # Если это медиа, сначала отправляем медиа, потом текст с информацией
            await message.copy_to(chat_id=settings.ADMIN_CHAT_ID)
            await message.bot.send_message(
                chat_id=settings.ADMIN_CHAT_ID,
                text=f"💬 Ответ от пользователя {username_str} (ID: {message.from_user.id})"
            )
        
        # Подтверждаем пользователю
        await message.answer("✅ Ваше сообщение отправлено администраторам!")
        
        # Очищаем состояние
        await state.clear()
        
    except Exception as e:
        await message.answer("❌ Произошла ошибка при отправке сообщения. Попробуйте позже.")
        print(f"Ошибка при отправке ответа пользователя в админ чат: {e}")

