import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app import texts, keyboards
from app.states import RegistrationStates
from app.db import Database

registration_router = Router()

@registration_router.message(Command("register"))
@registration_router.message(F.text == texts.BTN_START_REG)
@registration_router.message(F.text == texts.BTN_RE_REGISTER)
async def start_registration(message: Message, state: FSMContext) -> None:
    """Ro'yxatdan o'tish jarayonini boshlaydi."""
    await state.clear()
    await state.set_state(RegistrationStates.full_name)
    await message.answer(
        text=texts.ASK_FULL_NAME,
        reply_markup=keyboards.get_cancel_keyboard(),
        parse_mode="HTML"
    )

@registration_router.message(RegistrationStates.full_name, F.text)
async def process_full_name(message: Message, state: FSMContext) -> None:
    """Ism va familiyani qabul qiladi."""
    name = message.text.strip()
    if len(name) < 3 or len(name) > 100:
        await message.answer(texts.INVALID_NAME, parse_mode="HTML")
        return

    await state.update_data(full_name=name)
    await state.set_state(RegistrationStates.phone_number)
    await message.answer(
        text=texts.ASK_PHONE,
        reply_markup=keyboards.get_phone_keyboard(),
        parse_mode="HTML"
    )

@registration_router.message(RegistrationStates.phone_number, F.contact)
async def process_phone_contact(message: Message, state: FSMContext) -> None:
    """Kontakt tugmasi orqali yuborilgan raqamni qabul qiladi."""
    phone = message.contact.phone_number
    if not phone.startswith("+"):
        phone = f"+{phone}"
        
    await state.update_data(phone_number=phone)
    await state.set_state(RegistrationStates.age)
    await message.answer(
        text=texts.ASK_AGE,
        reply_markup=keyboards.get_cancel_keyboard(),
        parse_mode="HTML"
    )

@registration_router.message(RegistrationStates.phone_number, F.text)
async def process_phone_text(message: Message, state: FSMContext) -> None:
    """Qo'lda kiritilgan telefon raqamini tekshirib qabul qiladi."""
    raw_phone = message.text.strip()
    # Faqat raqamlar va + belgisini qoldirish
    cleaned = re.sub(r"[^\d+]", "", raw_phone)
    
    # Standart O'zbekiston yoki xalqaro raqam formatini tekshirish (kamida 9 ta raqam)
    digits_only = re.sub(r"\D", "", cleaned)
    if len(digits_only) < 9 or len(digits_only) > 15:
        await message.answer(texts.INVALID_PHONE, parse_mode="HTML")
        return

    if not cleaned.startswith("+"):
        cleaned = f"+{cleaned}"

    await state.update_data(phone_number=cleaned)
    await state.set_state(RegistrationStates.age)
    await message.answer(
        text=texts.ASK_AGE,
        reply_markup=keyboards.get_cancel_keyboard(),
        parse_mode="HTML"
    )

@registration_router.message(RegistrationStates.age, F.text)
async def process_age(message: Message, state: FSMContext) -> None:
    """Yoshni qabul qiladi va tasdiqlash bosqichiga o'tkazadi."""
    age_text = message.text.strip()
    if not age_text.isdigit():
        await message.answer(texts.INVALID_AGE, parse_mode="HTML")
        return

    age = int(age_text)
    if age < 7 or age > 120:
        await message.answer(texts.INVALID_AGE, parse_mode="HTML")
        return

    await state.update_data(age=age)
    data = await state.get_data()

    await state.set_state(RegistrationStates.confirm)
    
    summary = texts.CONFIRM_SUMMARY.format(
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        age=data["age"]
    )

    await message.answer(
        text=summary,
        reply_markup=keyboards.get_confirm_keyboard(),
        parse_mode="HTML"
    )

@registration_router.callback_query(RegistrationStates.confirm, F.data == "confirm_reg")
async def confirm_registration(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    """Ro'yxatdan o'tishni tasdiqlaydi va ma'lumotlarni bazaga saqlaydi."""
    data = await state.get_data()
    user_id = callback.from_user.id

    await db.save_user(
        user_id=user_id,
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        age=data.get("age")
    )

    await state.clear()
    
    # Inline tugmalarni olib tashlash
    await callback.message.edit_reply_markup(reply_markup=None)
    
    await callback.message.answer(
        text=texts.REGISTRATION_SUCCESS,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()

@registration_router.callback_query(RegistrationStates.confirm, F.data == "cancel_reg")
async def cancel_registration_callback(callback: CallbackQuery, state: FSMContext, db: Database) -> None:
    """Tasdiqlash bosqichida bekor qilish."""
    await state.clear()
    await callback.message.edit_reply_markup(reply_markup=None)

    user = await db.get_user(callback.from_user.id)
    reply_markup = keyboards.get_main_menu() if user else keyboards.get_start_keyboard()

    await callback.message.answer(
        text=texts.REGISTRATION_CANCELLED,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    await callback.answer()
