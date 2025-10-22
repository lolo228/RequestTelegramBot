"""Обработчики для администраторов"""
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import ChatMemberUpdatedFilter

from ..config import settings
from ..utils.storage import waiting_for_message
from ..utils.helpers import add_user_to_chats
from ..keyboards import get_reply_keyboard

router = Router(name="admin")


@router.callback_query(F.data.startswith("approve_"))
async def approve_application(callback: CallbackQuery):
    """
    Обработчик одобрения заявки
    Добавляет пользователя в указанные чаты/каналы
    """
    # Извлекаем ID пользователя из callback_data
    user_id = int(callback.data.split("_")[1])
    
    # Отправляем уведомление модератору
    await callback.answer("Заявка одобрена ✅")
    
    # Отправляем сообщение пользователю
    try:
        await callback.bot.send_message(
            chat_id=user_id,
            text="🎉 Поздравляем! Ваша заявка одобрена!"
        )
        
        # Добавляем пользователя в чаты
        if settings.TARGET_CHATS:
            success, errors = await add_user_to_chats(
                bot=callback.bot,
                user_id=user_id,
                chat_ids=settings.TARGET_CHATS
            )
            
            # Обновляем сообщение с результатами
            result_text = f"✅ Заявка одобрена\n"
            if success:
                result_text += f"✅ Создано приглашений: {len(success)}\n"
            if errors:
                result_text += f"❌ Ошибки: {len(errors)}\n"
                for error in errors:
                    result_text += f"  • {error}\n"
            
            await callback.message.edit_text(
                text=f"{callback.message.text}\n\n{result_text}",
                reply_markup=None
            )
        else:
            await callback.message.edit_text(
                text=f"{callback.message.text}\n\n✅ Заявка одобрена\n⚠️ Список чатов не настроен",
                reply_markup=None
            )
            
    except Exception as e:
        await callback.message.answer(f"Ошибка при обработке одобрения: {e}")


@router.callback_query(F.data.startswith("reject_"))
async def reject_application(callback: CallbackQuery):
    """
    Обработчик отклонения заявки
    Отправляет пользователю сообщение об отклонении
    """
    # Извлекаем ID пользователя из callback_data
    user_id = int(callback.data.split("_")[1])
    
    # Отправляем уведомление модератору
    await callback.answer("Заявка отклонена ❌")
    
    # Отправляем сообщение пользователю
    try:
        await callback.bot.send_message(
            chat_id=user_id,
            text="❌ К сожалению, ваша заявка была отклонена модераторами!"
        )
        
        # Обновляем сообщение
        await callback.message.edit_text(
            text=f"{callback.message.text}\n\n❌ Заявка отклонена",
            reply_markup=None
        )
        
    except Exception as e:
        await callback.message.answer(f"Ошибка при отклонении: {e}")


@router.callback_query(F.data.startswith("message_"))
async def send_message_to_user(callback: CallbackQuery):
    """
    Обработчик кнопки "Отправить сообщение"
    Активирует режим отправки сообщения пользователю
    """
    # Извлекаем ID пользователя из callback_data
    user_id = int(callback.data.split("_")[1])
    
    # Сохраняем информацию о том, что модератор хочет отправить сообщение
    waiting_for_message[callback.from_user.id] = user_id
    
    await callback.answer(
        "Отправьте следующее сообщение, оно будет переслано пользователю",
        show_alert=True
    )


@router.message(F.chat.id == settings.ADMIN_CHAT_ID)
async def forward_admin_message(message: Message):
    """
    Обработчик сообщений в чате администраторов
    Пересылает сообщение пользователю, если модератор активировал режим отправки
    """
    # Проверяем, ожидается ли сообщение от этого модератора
    if message.from_user.id in waiting_for_message:
        user_id = waiting_for_message.pop(message.from_user.id)
        
        try:
            # Пересылаем сообщение пользователю с кнопкой "Ответить"
            if message.text:
                await message.bot.send_message(
                    chat_id=user_id,
                    text=f"💬 Сообщение от модератора:\n\n{message.text}",
                    reply_markup=get_reply_keyboard()
                )
            else:
                # Если это не текстовое сообщение, копируем его с кнопкой
                await message.copy_to(
                    chat_id=user_id,
                    reply_markup=get_reply_keyboard()
                )
            
            # Подтверждаем отправку
            await message.reply("✅ Сообщение отправлено пользователю")
            
        except Exception as e:
            await message.reply(f"❌ Ошибка при отправке сообщения: {e}")

