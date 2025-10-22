"""Состояния для FSM (Finite State Machine)"""
from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    """Состояния для заполнения анкеты"""
    waiting_for_answer = State()  # Ожидание ответа пользователя на вопросы


class UserReply(StatesGroup):
    """Состояния для ответа пользователя администраторам"""
    waiting_for_reply = State()  # Ожидание сообщения-ответа от пользователя

