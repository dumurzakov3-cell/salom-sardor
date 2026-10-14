import io
import csv
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.exceptions import TelegramForbiddenError, TelegramAPIError

from app import texts, keyboards
from app.db import Database, UZB_TZ
from app.config import Config

admin_router = Router()

STATUS_TEXTS = {
    "boglanildi": "🟢 Bog'lanildi",
    "oylamoqda": "🔵 O'ylayapti",
    "bekor_qilindi": "🔴 Bekor qilindi",
    "yangi": "🟡 Yangi"
}

def is_admin(user_id: int, config: Config) -> bool:
    """Foydalanuvchi admin ro'yxatida borligini tekshiradi."""
    return user_id in config.admin_ids

# 1. /stats komandasi
@admin_router.message(Command("stats"))
async def cmd_stats(message: Message, db: Database, config: Config) -> None:
    if not is_admin(message.from_user.id, config):
        await message.answer("⚠️ Kechirasiz, sizda admin huquqi mavjud emas.")
        return

    stats = await db.get_stats()
    total = stats["total_apps"]

    lines = [
        "📊 <b>IT LIVE — ARIZALAR STATISTIKASI</b>\n",
        f"📌 <b>Jami arizalar soni:</b> {total} ta\n",
        "<b>📚 Kurslar kesimida:</b>"
    ]

    if stats["courses"]:
        for c in stats["courses"]:
            lines.append(f"• {c['course_name']}: {c['count']} ta")
    else:
        lines.append("• Hozircha ma'lumot yo'q")

    lines.append("\n<b>🏷 Holatlar (statuslar) kesimida:</b>")
    if stats["statuses"]:
        for s in stats["statuses"]:
            s_name = STATUS_TEXTS.get(s["status"], s["status"])
            lines.append(f"• {s_name}: {s['count']} ta")
    else:
        lines.append("• Hozircha ma'lumot yo'q")

    await message.answer("\n".join(lines), parse_mode="HTML")

# 2. /export komandasi (Excel o'qiydigan utf-8-sig CSV)
@admin_router.message(Command("export"))
async def cmd_export(message: Message, db: Database, config: Config) -> None:
    if not is_admin(message.from_user.id, config):
        await message.answer("⚠️ Kechirasiz, sizda admin huquqi mavjud emas.")
        return

    rows = await db.export_applications()
    if not rows:
        await message.answer("ℹ️ Hozircha bazada arizalar mavjud emas.")
        return

    # Excel o'qiydigan UTF-8-SIG formatida CSV tayyorlash
    output = io.StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow([
        "ID",
        "Sana (Toshkent)",
        "F.I.Sh.",
        "Telefon",
        "Telegram",
        "Kurs",
        "Format",
        "Qulay vaqt",
        "Tuman",
        "Holat"
    ])

    for r in rows:
        uname = f"@{r['username']}" if r.get("username") else "Yo'q"
        st = STATUS_TEXTS.get(r["status"], r["status"])
        writer.writerow([
            r["id"],
            r["created_at"],
            r["full_name"],
            r["phone_number"],
            uname,
            r["course_name"],
            r["study_format"],
            r["preferred_time"],
            r["district"],
            st
        ])

    csv_bytes = output.getvalue().encode("utf-8-sig")
    now_str = datetime.now(UZB_TZ).strftime("%Y%m%d_%H%M")
    filename = f"itlive_arizalar_{now_str}.csv"

    doc = BufferedInputFile(csv_bytes, filename=filename)
    await message.answer_document(
        document=doc,
        caption=f"📁 Jami <b>{len(rows)} ta</b> ariza eksport qilindi.",
        parse_mode="HTML"
    )

# 3. Status tugmalari callback
@admin_router.callback_query(F.data.startswith("status:"))
async def process_status_change(
    callback: CallbackQuery,
    db: Database,
    config: Config
) -> None:
    # Faqat adminlar o'zgartira oladi
    if not is_admin(callback.from_user.id, config):
        await callback.answer("⚠️ Faqat adminlar statusni o'zgartirishi mumkin!", show_alert=True)
        return

    parts = callback.data.split(":")
    if len(parts) != 3:
        await callback.answer()
        return

    _, app_id_str, new_status = parts
    app_id = int(app_id_str)

    app = await db.update_application_status(app_id, new_status)
    if not app:
        await callback.answer("Ariza topilmadi!", show_alert=True)
        return

    status_name = STATUS_TEXTS.get(new_status, new_status)
    admin_name = callback.from_user.full_name

    # Admin xabarini tahrirlash
    old_text = callback.message.html_text
    # "Holat:" qismini yangilash
    if "Holat:" in old_text:
        base_text = old_text.split("Holat:")[0].strip()
        new_text = f"{base_text}\n\n<b>Holat:</b> {status_name} <i>(O'zgartirdi: {admin_name})</i>"
    else:
        new_text = f"{old_text}\n\n<b>Holat:</b> {status_name} <i>(O'zgartirdi: {admin_name})</i>"

    try:
        await callback.message.edit_text(
            text=new_text,
            reply_markup=keyboards.get_admin_status_inline(app_id),
            parse_mode="HTML"
        )
    except TelegramAPIError:
        pass

    await callback.answer(f"Holat o'zgartirildi: {status_name}")

    # Foydalanuvchiga status o'zgargani haqida xabar (Standart 13 & 17)
    user_id = app["user_id"]
    course_name = app["course_name"]

    user_msg = None
    if new_status == "boglanildi":
        user_msg = (
            f"✅ <b>Assalomu alaykum!</b>\n\n"
            f"<b>{course_name}</b> kursi bo'yicha arizangiz IT LIVE menejeri tomonidan qabul qilindi. "
            f"Darslar va guruhlar bo'yicha siz bilan tez orada telefon orqali to'liq ma'lumot beriladi."
        )
    elif new_status == "bekor_qilindi":
        user_msg = (
            f"ℹ️ <b>Hurmatli o'quvchi!</b>\n\n"
            f"<b>{course_name}</b> kursi bo'yicha arizangiz bekor qilindi. "
            f"Savollaringiz bo'lsa, @itlive_uz orqali bog'lanishingiz mumkin."
        )

    if user_msg:
        try:
            await callback.bot.send_message(
                chat_id=user_id,
                text=user_msg,
                parse_mode="HTML"
            )
        except TelegramForbiddenError:
            # Foydalanuvchi botni bloklagan bo'lsa ham adminga xatolik bermaydi (Standart 17)
            pass
        except TelegramAPIError:
            pass
