from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from app import texts, keyboards
from app.db import Database

profile_router = Router()

@profile_router.message(Command("profile"))
@profile_router.message(F.text == texts.BTN_PROFILE)
async def view_profile(message: Message, db: Database) -> None:
    """Foydalanuvchi profili haqida ma'lumotni ko'rsatadi."""
    user = await db.get_user(message.from_user.id)
    
    if not user:
        await message.answer(
            text=texts.NOT_REGISTERED_YET,
            reply_markup=keyboards.get_start_keyboard(),
            parse_mode="HTML"
        )
        return

    profile_text = texts.PROFILE_INFO.format(
        user_id=user["user_id"],
        full_name=user["full_name"],
        phone_number=user["phone_number"],
        age=user["age"] if user["age"] is not None else "Ko'rsatilmagan",
        created_at=user["created_at"]
    )

    await message.answer(
        text=profile_text,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )

@profile_router.message(Command("about"))
@profile_router.message(F.text == texts.BTN_ABOUT)
async def view_about(message: Message) -> None:
    """Bot haqida ma'lumot beradi."""
    await message.answer(
        text=texts.ABOUT_BOT,
        parse_mode="HTML"
    )
