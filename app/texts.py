# Bot matnlari (O'zbek lotin tilida)

WELCOME_TEXT = (
    "👋 <b>Assalomu alaykum!</b>\n\n"
    "<b>IT LIVE</b> akademiyasining rasmiy botiga xush kelibsiz.\n"
    "Quyidagi menyudan kerakli bo'limni tanlang:"
)

HELP_TEXT = (
    "ℹ️ <b>Yordam bo'limi:</b>\n\n"
    "Ushbu bot orqali siz IT LIVE kurslari haqida to'liq ma'lumot olishingiz "
    "va kurslarga ro'yxatdan o'tishingiz mumkin.\n\n"
    "<b>Mavjud buyruqlar:</b>\n"
    "/start — Botni boshidan ishga tushirish\n"
    "/help — Yordam ma'lumotlarini ko'rish\n"
    "/cancel — Joriy amalni bekor qilish"
)

ABOUT_TEXT = (
    "📍 <b>IT LIVE akademiyasi haqida:</b>\n\n"
    "Biz zamonaviy IT kasblarini amaliyotga asoslangan holda o'rgatamiz.\n\n"
    "🏢 <b>Manzil:</b> Toshkent shahri, Chilonzor tumani, Bunyodkor ko'chasi 15-uy\n"
    "🎯 <b>Mo'ljal:</b> Mirzo Ulug'bek metrosi yonida\n"
    "📞 <b>Telefon:</b> +998 71 200 00 00 / +998 90 123 45 67\n"
    "⏰ <b>Ish vaqti:</b> Dushanba - Shanba, 09:00 - 20:00\n"
    "🌐 <b>Ijtimoiy tarmoqlar:</b> @itlive_uz"
)

COURSES_INTRO = (
    "📚 <b>IT LIVE kurslari ro'yxati:</b>\n\n"
    "O'zingizga qiziq bo'lgan kursni tanlang:"
)

COURSE_PYTHON = (
    "🐍 <b>Python Backend kursi</b>\n\n"
    "⏳ <b>Davomiyligi:</b> 6 oy\n"
    "💰 <b>Narxi:</b> 1 200 000 so'm / oy\n"
    "📅 <b>Dars kunlari:</b> Dushanba - Chorshanba - Juma\n"
    "📌 <b>Dastur:</b> Python asoslari, OOP, PostgreSQL, Django, Django REST Framework, Docker, Git"
)

COURSE_FRONTEND = (
    "💻 <b>Frontend kursi</b>\n\n"
    "⏳ <b>Davomiyligi:</b> 5 oy\n"
    "💰 <b>Narxi:</b> 1 100 000 so'm / oy\n"
    "📅 <b>Dars kunlari:</b> Seshanba - Payshanba - Shanba\n"
    "📌 <b>Dastur:</b> HTML5, CSS3/Sass, JavaScript (ES6+), React.js, Redux Toolkit, TailwindCSS"
)

COURSE_FOUNDATION = (
    "🧱 <b>Foundation (Dasturlashga kirish) kursi</b>\n\n"
    "⏳ <b>Davomiyligi:</b> 2 oy\n"
    "💰 <b>Narxi:</b> 800 000 so'm / oy\n"
    "📅 <b>Dars kunlari:</b> Dushanba - Chorshanba - Juma\n"
    "📌 <b>Dastur:</b> Kompyuter savodxonligi, mantiqiy fikrlash, algoritmlar, dasturlash asoslari (C / Python)"
)

CANCEL_SUCCESS = (
    "❌ Joriy jarayon bekor qilindi.\n"
    "Bosh menyudasiz:"
)

NOT_UNDERSTOOD = (
    "🤔 Kechirasiz, bu buyruqni tushunmadim.\n"
    "Iltimos, quyidagi menyu tugmalaridan birini tanlang:"
)

# FSM matnlari (M2 uchun ham tayyorlab qo'yilgan)
ASK_FULL_NAME = (
    "👤 <b>To'liq ism va familiyangizni kiriting:</b>\n"
    "<i>(Masalan: Sardor Aliyev)</i>"
)

ASK_PHONE = (
    "📱 <b>Telefon raqamingizni yuboring:</b>\n\n"
    "Pastdagi <b>«📱 Raqamni yuborish»</b> tugmasini bosing yoki "
    "raqamingizni quyidagi formatda yozing:\n"
    "<code>+998901234567</code>"
)

ASK_FORMAT = "💻 <b>Ta'lim shaklini tanlang:</b>"
ASK_TIME = "⏰ <b>Darslarga qatnashish uchun sizga qaysi vaqt qulay?</b>"
ASK_DISTRICT = "📍 <b>Qaysi tuman yoki hududda istiqomat qilasiz?</b>\n<i>(Masalan: Chilonzor tumani)</i>"

CONFIRM_CARD = (
    "📋 <b>Arizangiz ma'lumotlarini tekshiring:</b>\n\n"
    "📚 <b>Kurs:</b> {course_name}\n"
    "👤 <b>Ism-familiya:</b> {full_name}\n"
    "📞 <b>Telefon:</b> {phone_number}\n"
    "💻 <b>Ta'lim shakli:</b> {study_format}\n"
    "⏰ <b>Qulay vaqt:</b> {preferred_time}\n"
    "📍 <b>Tuman:</b> {district}\n\n"
    "Ma'lumotlar to'g'rimi? Arizani tasdiqlaysizmi?"
)

APP_SUBMITTED = (
    "🎉 <b>Rahmat! Arizangiz muvaffaqiyatli qabul qilindi.</b>\n\n"
    "Menejerimiz tez orada siz bilan bog'lanadi."
)

APP_ALREADY_EXISTS = (
    "⚠️ Siz ushbu kursga yaqinda ariza topshirgansiz.\n"
    "Arizangiz ko'rib chiqilmoqda, menejerimiz tez orada bog'lanadi."
)

INVALID_NAME = (
    "⚠️ Ism-familiya noto'g'ri kiritildi.\n"
    "Kamida 2 ta so'z (ism va familiya) yozing. Masalan: <i>Sardor Aliyev</i>"
)

INVALID_PHONE = (
    "⚠️ Telefon raqami noto'g'ri ko'rinishda.\n"
    "Iltimos, pastdagi tugmani bosing yoki raqamni quyidagi ko'rinishda kiriting:\n"
    "<code>+998901234567</code>"
)

INVALID_OPTION = "⚠️ Iltimos, faqat taqdim etilgan tugmalardan birini tanlang."
ONLY_TEXT_ALLOWED = "⚠️ Iltimos, stiker yoki fayl emas, matn yuboring."

# Tugma matnlari
BTN_COURSES = "📚 Kurslar haqida ma'lumot"
BTN_REGISTER = "📝 Kursga yozilish"
BTN_ABOUT = "📍 Biz haqimizda va Manzil"
BTN_CANCEL = "❌ Bekor qilish"
BTN_BACK = "🔙 Orqaga"
BTN_SEND_PHONE = "📱 Raqamni yuborish"
BTN_FORMAT_OFFLINE = "🏢 Oflayn (markazda)"
BTN_FORMAT_ONLINE = "🌐 Onlayn"
BTN_TIME_MORNING = "🌅 09:00 - 12:00"
BTN_TIME_AFTERNOON = "☀️ 14:00 - 17:00"
BTN_TIME_EVENING = "🌙 18:30 - 21:00"
