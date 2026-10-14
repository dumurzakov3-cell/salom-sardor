from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app import texts, keyboards

common_router = Router()

@common_router.message(StateFilter("*"), CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """/start buyrug'i: FSM ni tozalaydi va asosiy menyuni ko'rsatadi."""
    await state.clear()
    await message.answer(
        text=texts.WELCOME_TEXT,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )

@common_router.message(StateFilter("*"), Command("help"))
async def cmd_help(message: Message) -> None:
    """/help buyrug'i: yordam ma'lumotlari."""
    await message.answer(
        text=texts.HELP_TEXT,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )

@common_router.message(StateFilter("*"), Command("cancel"))
@common_router.message(StateFilter("*"), F.text == texts.BTN_CANCEL)
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """/cancel yoki '❌ Bekor qilish' tugmasi: FSM ni tozalaydi."""
    await state.clear()
    await message.answer(
        text=texts.CANCEL_SUCCESS,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )

@common_router.message(StateFilter("*"), F.text == texts.BTN_ABOUT)
async def show_about(message: Message, state: FSMContext) -> None:
    """'📍 Biz haqimizda va Manzil' bo'limi."""
    await state.clear()
    await message.answer(
        text=texts.ABOUT_TEXT,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )

@common_router.message(StateFilter("*"), F.text == texts.BTN_COURSES)
async def show_courses_list(message: Message, state: FSMContext) -> None:
    """'📚 Kurslar haqida ma'lumot' bo'limi."""
    await state.clear()
    await message.answer(
        text=texts.COURSES_INTRO,
        reply_markup=keyboards.get_courses_inline(),
        parse_mode="HTML"
    )

# Kurslar bo'yicha inline ma'lumotlar
@common_router.callback_query(F.data == "info:courses_list")
async def cb_courses_list(callback: CallbackQuery) -> None:
    """Barcha kurslar ro'yxatiga qaytish."""
    await callback.message.edit_text(
        text=texts.COURSES_INTRO,
        reply_markup=keyboards.get_courses_inline(),
        parse_mode="HTML"
    )
    await callback.answer()

@common_router.callback_query(F.data == "info:python")
async def cb_course_python(callback: CallbackQuery) -> None:
    """Python kursi ma'lumoti."""
    await callback.message.edit_text(
        text=texts.COURSE_PYTHON,
        reply_markup=keyboards.get_course_detail_inline("python"),
        parse_mode="HTML"
    )
    await callback.answer()

@common_router.callback_query(F.data == "info:frontend")
async def cb_course_frontend(callback: CallbackQuery) -> None:
    """Frontend kursi ma'lumoti."""
    await callback.message.edit_text(
        text=texts.COURSE_FRONTEND,
        reply_markup=keyboards.get_course_detail_inline("frontend"),
        parse_mode="HTML"
    )
    await callback.answer()

@common_router.callback_query(F.data == "info:foundation")
async def cb_course_foundation(callback: CallbackQuery) -> None:
    """Foundation kursi ma'lumoti."""
    await callback.message.edit_text(
        text=texts.COURSE_FOUNDATION,
        reply_markup=keyboards.get_course_detail_inline("foundation"),
        parse_mode="HTML"
    )
    await callback.answer()

@common_router.callback_query(F.data == "info:back_main")
async def cb_back_to_main(callback: CallbackQuery, state: FSMContext) -> None:
    """Asosiy menyuga qaytish inline callback."""
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        text=texts.WELCOME_TEXT,
        reply_markup=keyboards.get_main_menu(),
        parse_mode="HTML"
    )
    await callback.answer()
