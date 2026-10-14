# IT LIVE — Telegram Ro'yxatdan O'tish Boti (@SAR_DOR_G_BOT)

IT LIVE o'quv markazi uchun kurslarga arizalarni qabul qilish va boshqarishni to'liq avtomatlashtiruvchi Telegram bot.

---

## 🛠 Texnologiyalar
* **Til:** Python 3.12
* **Asosiy freymvork:** aiogram 3.31.0 (eng so'nggi 3.x)
* **Ma'lumotlar bazasi:** SQLite + aiosqlite (to'liq asinxron)
* **Konfiguratsiya:** python-dotenv (barcha sirlar faqat `.env` da)
* **Rejim:** Polling (Railway worker orqali)

---

## 📁 Loyiha tuzilmasi
```text
c:\DARS\
├── main.py                  # Botni ishga tushirish nuqtasi, global error handler
├── requirements.txt         # Qotirilgan versiyalar bilan kutubxonalar
├── Procfile                 # Railway worker konfiguratsiyasi
├── .env.example             # Muhit o'zgaruvchilari shabloni
├── .env                     # Haqiqiy maxfiy kalitlar (Git'ga yuklanmaydi)
├── .gitignore               # Versiya nazoratidan chetlatilgan fayllar
├── .python-version          # Python 3.12
├── README.md                # Qo'llanma va hujjatlar
├── data/                    # SQLite ma'lumotlar bazasi papkasi (avtomatik yaratiladi)
│   └── bot.db
└── app/
    ├── config.py            # .env sozlamalarini yuklash
    ├── db.py                # Asinxron SQLite operatsiyalari, statistikalar va eksport
    ├── texts.py             # Barcha xabarlar va o'zbekcha matnlar
    ├── keyboards.py         # Reply va Inline tugmalar
    ├── states.py            # FSM holatlari
    └── handlers/            # Har bir funksiya alohida routerda
        ├── __init__.py      # Routerlarni birlashtiruvchi va fallback handler
        ├── common.py        # /start, /help, /cancel, kurslar va manzil
        ├── application.py   # Kursga yozilish (FSM, tekshiruvlar, tasdiqlash)
        └── admin.py         # /stats, /export, arizalar statusini boshqarish
```

---

## 🚀 Lokal muhitda ishga tushirish

1. **Repozitoriyani klonlash yoki papkani ochish:**
   ```bash
   cd c:\DARS
   ```

2. **Virtual muhit yaratish va faollashtirish:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   ```

3. **Kutubxonalarni o'rnatish:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Muhit o'zgaruvchilarini sozlash:**
   `.env.example` faylidan nusxa olib `.env` yarating:
   ```env
   BOT_TOKEN=123456789:AA...
   ADMIN_IDS=123456789,987654321
   ADMIN_CHAT_ID=123456789
   DB_PATH=data/bot.db
   ```
   * `BOT_TOKEN`: @BotFather orqali olingan token.
   * `ADMIN_IDS`: Bot adminlarining shaxsiy Telegram ID raqamlari (vergul bilan).
   * `ADMIN_CHAT_ID`: Yangi arizalar boradigan guruh yoki admin ID raqami.

5. **Botni ishga tushirish:**
   ```bash
   python main.py
   ```

---

## 🚂 Railway platformasiga Deploy qilish (GitHub orqali)

1. Loyihani o'zingizning GitHub akkauntingizga yuklang:
   ```bash
   git add .
   git commit -m "IT LIVE registration bot ready"
   git push origin main
   ```
   *(Eslatma: `.env` va `.venv` `.gitignore` orqali GitHub'ga chiqmaydi!)*

2. [Railway.app](https://railway.app) ga kiring va **New Project** -> **Deploy from GitHub repo** ni tanlang.
3. Repozitoriyangizni tanlang.
4. **Variables** bo'limiga o'ting va quyidagi o'zgaruvchilarni kiriting:
   * `BOT_TOKEN` = sizning bot tokeningiz
   * `ADMIN_IDS` = sizning telegram ID raqamingiz
   * `ADMIN_CHAT_ID` = arizalar tushadigan guruh yoki admin ID raqami
   * `DB_PATH` = `data/bot.db`
5. **Settings** bo'limida Deploy command yoki `Procfile` mavjudligini tekshiring (`worker: python main.py`).
6. Railway avtomatik ravishda build qiladi va bot 24/7 rejimida uzluksiz ishlay boshlaydi!

---

## 👮‍♂️ Admin imkoniyatlari
* **Bildirishnomalar:** Yangi ariza kelib tushganda darhol to'liq ma'lumot va inline tugmalar bilan keladi.
* **Status boshqaruvi:** Tugmani bosish orqali arizani `Bog'lanildi`, `O'ylayapti` yoki `Bekor qilindi` holatiga o'tkazish mumkin. O'quvchiga avtomatik bildirishnoma boradi.
* `/stats` — Kurslar va holatlar kesimida aniq statistika.
* `/export` — Barcha arizalarni Excel'da o'qiladigan `UTF-8-SIG` formatidagi CSV fayl ko'rinishida yuklab olish.
