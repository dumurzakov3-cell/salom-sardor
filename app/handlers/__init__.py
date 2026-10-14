from aiogram import Router
from aiogram.types import Message
from app import texts, keyboards
from .common import common_router
from .application import application_router
from .admin import admin_router

main_router = Router()

# 1. Funksional routerlar
main_router.include_router(admin_router)
main_router.include_router(common_router)
main_router.include_router(application_router)

# 2. Tanilmagan xabarlar uchun alohida oxirgi router (Standart 7)
fallback_router = Router()

@fallback_router.message()
async def fallback_handler(message: Message) -> None:
    await message.answer(
        text=texts.NOT_UNDERSTOOD,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )

main_router.include_router(fallback_router)
