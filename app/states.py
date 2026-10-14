from aiogram.fsm.state import State, StatesGroup

class ApplicationStates(StatesGroup):
    course = State()         # Kursni tanlash
    full_name = State()      # F.I.Sh. kiritish
    phone_number = State()   # Telefon raqam
    study_format = State()   # Oflayn / Onlayn
    preferred_time = State() # Dars vaqti
    district = State()       # Yashash tumani
    confirm = State()        # Ma'lumotlarni tasdiqlash
