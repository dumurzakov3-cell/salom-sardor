from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from app import texts

def get_main_menu() -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_COURSES)],
            [KeyboardButton(text=texts.BTN_REGISTER)],
            [KeyboardButton(text=texts.BTN_ABOUT)]
        ],
        resize_keyboard=True
    )

def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """FSM bosqichlarida bekor qilish tugmasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_CANCEL)]
        ],
        resize_keyboard=True
    )

def get_phone_keyboard() -> ReplyKeyboardMarkup:
    """Telefon raqamni yuborish klaviaturasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_SEND_PHONE, request_contact=True)],
            [KeyboardButton(text=texts.BTN_CANCEL)]
        ],
        resize_keyboard=True
    )

def get_format_keyboard() -> ReplyKeyboardMarkup:
    """Ta'lim shaklini tanlash klaviaturasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_FORMAT_OFFLINE), KeyboardButton(text=texts.BTN_FORMAT_ONLINE)],
            [KeyboardButton(text=texts.BTN_CANCEL)]
        ],
        resize_keyboard=True
    )

def get_time_keyboard() -> ReplyKeyboardMarkup:
    """Qulay vaqtni tanlash klaviaturasi."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=texts.BTN_TIME_MORNING)],
            [KeyboardButton(text=texts.BTN_TIME_AFTERNOON)],
            [KeyboardButton(text=texts.BTN_TIME_EVENING)],
            [KeyboardButton(text=texts.BTN_CANCEL)]
        ],
        resize_keyboard=True
    )

def get_courses_inline() -> InlineKeyboardMarkup:
    """Kurslar haqida ma'lumot olish menyusi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐍 Python Backend", callback_data="info:python")],
            [InlineKeyboardButton(text="💻 Frontend", callback_data="info:frontend")],
            [InlineKeyboardButton(text="🧱 Foundation", callback_data="info:foundation")],
            [InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="info:back_main")]
        ]
    )

def get_course_detail_inline(course_key: str) -> InlineKeyboardMarkup:
    """Tanlangan kurs tafsiloti ostidagi tugmalar."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✍️ Ushbu kursga yozilish", callback_data=f"enroll:{course_key}")],
            [InlineKeyboardButton(text="🔙 Barcha kurslar", callback_data="info:courses_list")]
        ]
    )

def get_course_select_inline() -> InlineKeyboardMarkup:
    """Kursga yozilish uchun kurs tanlash menyusi."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🐍 Python Backend", callback_data="apply:python")],
            [InlineKeyboardButton(text="💻 Frontend", callback_data="apply:frontend")],
            [InlineKeyboardButton(text="🧱 Foundation", callback_data="apply:foundation")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="apply:cancel")]
        ]
    )

def get_confirm_inline() -> InlineKeyboardMarkup:
    """Arizani tasdiqlash tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="confirm_apply:yes"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data="confirm_apply:no")
            ]
        ]
    )

def get_admin_status_inline(app_id: int) -> InlineKeyboardMarkup:
    """Menejer uchun arizani boshqarish tugmalari."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Bog'lanildi", callback_data=f"status:{app_id}:boglanildi"),
                InlineKeyboardButton(text="⏳ O'ylayapti", callback_data=f"status:{app_id}:oylamoqda")
            ],
            [
                InlineKeyboardButton(text="❌ Bekor qilindi", callback_data=f"status:{app_id}:bekor_qilindi")
            ]
        ]
    )

remove_keyboard = ReplyKeyboardRemove()
