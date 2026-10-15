import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError
from aiogram.types import ErrorEvent

from app.config import load_config
from app.db import Database
from app.handlers import main_router

# Global log sozlamalari
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("bot")

async def error_handler(event: ErrorEvent) -> bool:
    """Bitta xato butun botni to'xtatib qo'ymasligi uchun global xatolik tutuvchi."""
    exception = event.exception
    if isinstance(exception, TelegramForbiddenError):
        logger.warning(f"Foydalanuvchi botni bloklagan: {exception}")
        return True
    if isinstance(exception, TelegramAPIError):
        logger.error(f"Telegram API xatosi: {exception}")
        return True

    logger.exception(f"Kutilmagan xatolik yuz berdi: {exception}")
    return True

async def main() -> None:
    try:
        config = load_config()
    except Exception as e:
        logger.critical(f"Konfiguratsiya yuklanmadi: {e}")
        return

    # Ma'lumotlar bazasini tayyorlash
    db = Database(config.db_path)
    await db.init()
    logger.info("Ma'lumotlar bazasi initsializatsiya qilindi.")

    # Bot va Dispatcher yaratish
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Baza va konfiguratsiyani dependency injection orqali uzatish
    dp["db"] = db
    dp["config"] = config

    # Global xatolik tutuvchini ro'yxatdan o'tkazish
    dp.errors.register(error_handler)

    # Handler routerlarini ulash
    dp.include_router(main_router)

    # Webhookni tozalash (yangi kelgan xabarlar o'chib ketmasligi uchun drop_pending_updates=False)
    await bot.delete_webhook(drop_pending_updates=False)
    logger.info("Bot polling rejimida ishga tushirilmoqda...")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Bot sessiyasi yopildi.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot foydalanuvchi tomonidan to'xtatildi.")
