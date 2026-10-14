import os
from dataclasses import dataclass
from typing import List, Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_ids: List[int]
    admin_chat_id: Optional[int]
    db_path: str

def load_config() -> Config:
    token = os.getenv("BOT_TOKEN")
    if not token or not token.strip():
        raise ValueError("BOT_TOKEN .env faylida topilmadi! Iltimos, .env faylida BOT_TOKEN ni ko'rsating.")

    # ADMIN_IDS ni ro'yxatga aylantirish (masalan: 1234567,8901234)
    raw_admin_ids = os.getenv("ADMIN_IDS", "")
    admin_ids: List[int] = []
    for item in raw_admin_ids.split(","):
        item = item.strip()
        if item.isdigit() or (item.startswith("-") and item[1:].isdigit()):
            admin_ids.append(int(item))

    # ADMIN_CHAT_ID
    raw_admin_chat = os.getenv("ADMIN_CHAT_ID", "").strip()
    admin_chat_id: Optional[int] = None
    if raw_admin_chat:
        try:
            admin_chat_id = int(raw_admin_chat)
        except ValueError:
            pass

    db_path = os.getenv("DB_PATH", "data/bot.db").strip()

    return Config(
        bot_token=token.strip(),
        admin_ids=admin_ids,
        admin_chat_id=admin_chat_id,
        db_path=db_path
    )
