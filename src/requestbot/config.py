"""Конфигурация бота"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Путь к корневой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Настройки бота"""
    
    # Токен бота
    BOT_TOKEN: str = Field(..., description="Токен телеграм бота")
    
    # ID чата администраторов
    ADMIN_CHAT_ID: int = Field(..., description="ID чата администраторов")
    
    # Список каналов/чатов для добавления одобренных пользователей
    # Формат: ["chat_id1", "chat_id2"]
    TARGET_CHATS: list[str] = Field(
        default_factory=list,
        description="Список ID чатов/каналов для добавления пользователей"
    )
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Создаем экземпляр настроек
settings = Settings()

