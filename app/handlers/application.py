import re
import logging
from html import escape as html_quote
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError

logger = logging.getLogger(__name__)

from app import texts, keyboards
from app.states import ApplicationStates
from app.db import Database, get_now_uzb_str
from app.config import Config

application_router = Router()

COURSE_MAP = {
    "python": "Python Backend",
    "frontend": "Frontend",
    "foundation": "Foundation"
}

FORMAT_MAP = {
    texts.BTN_FORMAT_OFFLINE: "Oflayn",
    texts.BTN_FORMAT_ONLINE: "Onlayn"
}

TIME_MAP = {
    texts.BTN_TIME_MORNING: "09:00 - 12:00",
    texts.BTN_TIME_AFTERNOON: "14:00 - 17:00",
    texts.BTN_TIME_EVENING: "18:30 - 21:00"
}

# 1. Kursga yozilishni boshlash
@application_router.message(StateFilter("*"), Command("register"))
@application_router.message(StateFilter("*"), F.text == texts.BTN_REGISTER)
async def start_apply(message: Message, state: FSMContext) -> None:
    """Kurs tanlash menyusini ochadi."""
    await state.clear()
    await state.set_state(ApplicationStates.course)
    await message.answer(
        text="Qaysi kursga yozilmoqchisiz? Tanlang:",
        reply_markup=keyboards.get_course_select_inline(),
        parse_mode="HTML"
    )

# Kurs tanlanganda (apply: yoki enroll:)
@application_router.callback_query(F.data.startswith("apply:"))
@application_router.callback_query(F.data.startswith("enroll:"))
async def process_course_selection(
    callback: CallbackQuery,
    state: FSMContext,
    db: Database
) -> None:
    action, course_key = callback.data.split(":", 1)
    if course_key == "cancel":
        await state.clear()
        try:
            await callback.message.delete()
        except TelegramAPIError:
            pass
        await callback.message.answer(
            text=texts.CANCEL_SUCCESS,
            reply_markup=keyboards.get_main_menu(),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    course_name = COURSE_MAP.get(course_key)
    if not course_name:
        await callback.answer("Kurs topilmadi!", show_alert=True)
        return

    user_id = callback.from_user.id
    # Takroriy ariza tekshiruvi (zo'r ishlash standarti 14)
    has_recent = await db.check_recent_application(user_id, course_name)
    if has_recent:
        await callback.answer()
        await callback.message.answer(
            text=texts.APP_ALREADY_EXISTS,
            reply_markup=keyboards.get_main_menu(),
            parse_mode="HTML"
        )
        await state.clear()
        return

    await state.update_data(course_name=course_name)
    await state.set_state(ApplicationStates.full_name)
    await callback.answer()

    try:
        await callback.message.delete()
    except TelegramAPIError:
        pass

    await callback.message.answer(
        text=f"📚 Tanlangan kurs: <b>{course_name}</b>\n\n{texts.ASK_FULL_NAME}",
        reply_markup=keyboards.get_cancel_keyboard(),
        parse_mode="HTML"
    )

# 2. F.I.Sh. qabul qilish
@application_router.message(ApplicationStates.full_name, F.text)
async def process_full_name(message: Message, state: FSMContext) -> None:
    if message.text == texts.BTN_CANCEL:
        await state.clear()
        await message.answer(texts.CANCEL_SUCCESS, reply_markup=keyboards.get_main_menu())
        return

    raw_name = message.text.strip()
    words = raw_name.split()
    
    # Validatsiya: kamida 2 ta so'z, harflar, 5-60 belgi
    if len(words) < 2 or len(raw_name) < 5 or len(raw_name) > 60:
        await message.answer(texts.INVALID_NAME, parse_mode="HTML")
        return

    # Belgilarni tekshirish (faqat harflar, apostrof va probellar)
    cleaned_test = re.sub(r"[\s\'-’`]", "", raw_name)
    if not cleaned_test.isalpha():
        await message.answer(texts.INVALID_NAME, parse_mode="HTML")
        return

    safe_name = html_quote(raw_name)
    await state.update_data(full_name=safe_name)
    await state.set_state(ApplicationStates.phone_number)
    await message.answer(
        text=texts.ASK_PHONE,
        reply_markup=keyboards.get_phone_keyboard(),
        parse_mode="HTML"
    )

# 3. Telefon raqam qabul qilish (Kontakt)
@application_router.message(ApplicationStates.phone_number, F.contact)
async def process_phone_contact(message: Message, state: FSMContext) -> None:
    phone = message.contact.phone_number.strip()
    if not phone.startswith("+"):
        phone = f"+{phone}"

    await state.update_data(phone_number=phone)
    await state.set_state(ApplicationStates.study_format)
    await message.answer(
        text=texts.ASK_FORMAT,
        reply_markup=keyboards.get_format_keyboard(),
        parse_mode="HTML"
    )

# Telefon raqam qabul qilish (Matn)
@application_router.message(ApplicationStates.phone_number, F.text)
async def process_phone_text(message: Message, state: FSMContext) -> None:
    if message.text == texts.BTN_CANCEL:
        await state.clear()
        await message.answer(texts.CANCEL_SUCCESS, reply_markup=keyboards.get_main_menu())
        return

    raw_phone = message.text.strip()
    digits = re.sub(r"\D", "", raw_phone)

    # Validatsiya: O'zbekiston raqami (998 va 9 raqam) yoki xalqaro 9-12 raqam
    if digits.startswith("998") and len(digits) == 12:
        formatted_phone = f"+{digits}"
    elif len(digits) == 9:
        formatted_phone = f"+998{digits}"
    else:
        await message.answer(texts.INVALID_PHONE, parse_mode="HTML")
        return

    await state.update_data(phone_number=formatted_phone)
    await state.set_state(ApplicationStates.study_format)
    await message.answer(
        text=texts.ASK_FORMAT,
        reply_markup=keyboards.get_format_keyboard(),
        parse_mode="HTML"
    )

# 4. Ta'lim shakli qabul qilish
@application_router.message(ApplicationStates.study_format, F.text)
async def process_format(message: Message, state: FSMContext) -> None:
    if message.text == texts.BTN_CANCEL:
        await state.clear()
        await message.answer(texts.CANCEL_SUCCESS, reply_markup=keyboards.get_main_menu())
        return

    format_val = FORMAT_MAP.get(message.text)
    if not format_val:
        await message.answer(texts.INVALID_OPTION)
        return

    await state.update_data(study_format=format_val)
    await state.set_state(ApplicationStates.preferred_time)
    await message.answer(
        text=texts.ASK_TIME,
        reply_markup=keyboards.get_time_keyboard(),
        parse_mode="HTML"
    )

# 5. Qulay vaqt qabul qilish
@application_router.message(ApplicationStates.preferred_time, F.text)
async def process_time(message: Message, state: FSMContext) -> None:
    if message.text == texts.BTN_CANCEL:
        await state.clear()
        await message.answer(texts.CANCEL_SUCCESS, reply_markup=keyboards.get_main_menu())
        return

    time_val = TIME_MAP.get(message.text)
    if not time_val:
        await message.answer(texts.INVALID_OPTION)
        return

    await state.update_data(preferred_time=time_val)
    await state.set_state(ApplicationStates.district)
    await message.answer(
        text=texts.ASK_DISTRICT,
        reply_markup=keyboards.get_cancel_keyboard(),
        parse_mode="HTML"
    )

# 6. Tuman qabul qilish
@application_router.message(ApplicationStates.district, F.text)
async def process_district(message: Message, state: FSMContext) -> None:
    if message.text == texts.BTN_CANCEL:
        await state.clear()
        await message.answer(texts.CANCEL_SUCCESS, reply_markup=keyboards.get_main_menu())
        return

    raw_dist = message.text.strip()
    if len(raw_dist) < 3 or len(raw_dist) > 50:
        await message.answer(
            text="⚠️ Tuman nomi 3 tadan 50 tagacha belgidan iborat bo'lishi kerak. Qayta kiriting:",
            parse_mode="HTML"
        )
        return

    safe_dist = html_quote(raw_dist)
    await state.update_data(district=safe_dist)
    data = await state.get_data()

    await state.set_state(ApplicationStates.confirm)
    card_text = texts.CONFIRM_CARD.format(
        course_name=data["course_name"],
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        study_format=data["study_format"],
        preferred_time=data["preferred_time"],
        district=data["district"]
    )
    await message.answer(
        text=card_text,
        reply_markup=keyboards.get_confirm_inline(),
        parse_mode="HTML"
    )

# 7. Tasdiqlash callback
@application_router.callback_query(ApplicationStates.confirm, F.data.startswith("confirm_apply:"))
async def process_confirm(
    callback: CallbackQuery,
    state: FSMContext,
    db: Database,
    config: Config
) -> None:
    action = callback.data.split(":")[1]
    if action == "no":
        await state.clear()
        try:
            await callback.message.delete()
        except TelegramAPIError:
            pass
        await callback.message.answer(texts.CANCEL_SUCCESS, reply_markup=keyboards.get_main_menu())
        await callback.answer()
        return

    data = await state.get_data()
    user_id = callback.from_user.id
    username = callback.from_user.username

    # Bazaga foydalanuvchini saqlash
    await db.save_user(
        user_id=user_id,
        username=username,
        full_name=data["full_name"],
        phone_number=data["phone_number"],
        district=data["district"]
    )

    # Bazaga arizani saqlash
    app_id = await db.create_application(
        user_id=user_id,
        course_name=data["course_name"],
        study_format=data["study_format"],
        preferred_time=data["preferred_time"],
        district=data["district"]
    )

    await state.clear()
    await callback.answer()

    try:
        await callback.message.delete()
    except TelegramAPIError:
        pass

    # Foydalanuvchiga muvaffaqiyat xabari
    await callback.message.answer(
        text=texts.APP_SUBMITTED,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )

    # Menejer / Adminlarga bildirishnoma (Zo'r ishlash standarti 13)
    user_mention = f"@{username}" if username else "Mavjud emas"
    admin_notification = (
        f"🔔 <b>YANGI ARIZA #{app_id}</b>\n\n"
        f"📚 <b>Kurs:</b> {data['course_name']}\n"
        f"👤 <b>O'quvchi:</b> {data['full_name']} ({user_mention})\n"
        f"📞 <b>Telefon:</b> <code>{data['phone_number']}</code>\n"
        f"💻 <b>Format:</b> {data['study_format']}\n"
        f"⏰ <b>Qulay vaqt:</b> {data['preferred_time']}\n"
        f"📍 <b>Tuman:</b> {data['district']}\n"
        f"📅 <b>Vaqti:</b> {get_now_uzb_str()} (Toshkent)\n\n"
        f"<b>Holat:</b> 🟡 Yangi"
    )

    target_chat_ids = set()
    if config.admin_chat_id:
        target_chat_ids.add(config.admin_chat_id)
    for a_id in config.admin_ids:
        target_chat_ids.add(a_id)

    for chat_id in target_chat_ids:
        try:
            await callback.bot.send_message(
                chat_id=chat_id,
                text=admin_notification,
                reply_markup=keyboards.get_admin_status_inline(app_id),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Adminga ariza xabari yetkazilmadi (chat_id={chat_id}): {e}")

# Kutilmagan har qanday narsani (stiker, rasm, video va h.k.) ushlab qoluvchi filtr (Standart 6)
@application_router.message(ApplicationStates.full_name)
@application_router.message(ApplicationStates.phone_number)
@application_router.message(ApplicationStates.study_format)
@application_router.message(ApplicationStates.preferred_time)
@application_router.message(ApplicationStates.district)
async def process_unexpected_content(message: Message) -> None:
    await message.answer(texts.ONLY_TEXT_ALLOWED)
