import os
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone, timedelta
import aiosqlite

UZB_TZ = timezone(timedelta(hours=5))

def get_now_uzb_str() -> str:
    """O'zbekiston vaqti bilan joriy vaqt satri."""
    return datetime.now(UZB_TZ).strftime("%Y-%m-%d %H:%M:%S")

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path

    async def init(self) -> None:
        """Baza papkasini va jadvallarni avtomatik yaratadi."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

        async with aiosqlite.connect(self.db_path) as db:
            # Users jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    full_name TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    district TEXT,
                    created_at TEXT NOT NULL
                );
            """)

            # Applications jadvali
            await db.execute("""
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    course_name TEXT NOT NULL,
                    study_format TEXT NOT NULL,
                    preferred_time TEXT NOT NULL,
                    district TEXT NOT NULL,
                    status TEXT DEFAULT 'yangi',
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                );
            """)
            await db.commit()

    async def save_user(
        self,
        user_id: int,
        username: Optional[str],
        full_name: str,
        phone_number: str,
        district: Optional[str] = None
    ) -> None:
        """Foydalanuvchini saqlaydi yoki yangilaydi."""
        now = get_now_uzb_str()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (user_id, username, full_name, phone_number, district, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    username = excluded.username,
                    full_name = excluded.full_name,
                    phone_number = excluded.phone_number,
                    district = excluded.district;
            """, (user_id, username, full_name, phone_number, district, now))
            await db.commit()

    async def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Foydalanuvchi ma'lumotlarini ID bo'yicha oladi."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def check_recent_application(self, user_id: int, course_name: str) -> bool:
        """Shu kursga yangi yoki ko'rilayotgan ariza bor-yo'qligini tekshiradi."""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("""
                SELECT 1 FROM applications 
                WHERE user_id = ? AND course_name = ? AND status IN ('yangi', 'oylamoqda')
                LIMIT 1;
            """, (user_id, course_name)) as cursor:
                row = await cursor.fetchone()
                return row is not None

    async def create_application(
        self,
        user_id: int,
        course_name: str,
        study_format: str,
        preferred_time: str,
        district: str
    ) -> int:
        """Yangi ariza yaratadi va uning ID sini qaytaradi."""
        now = get_now_uzb_str()
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO applications (user_id, course_name, study_format, preferred_time, district, status, created_at)
                VALUES (?, ?, ?, ?, ?, 'yangi', ?)
            """, (user_id, course_name, study_format, preferred_time, district, now))
            await db.commit()
            return cursor.lastrowid

    async def get_application(self, app_id: int) -> Optional[Dict[str, Any]]:
        """Arizani to'liq ma'lumotlari bilan olish (user ma'lumotlari bilan)."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT a.*, u.full_name, u.phone_number, u.username
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                WHERE a.id = ?;
            """, (app_id,)) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def update_application_status(self, app_id: int, new_status: str) -> Optional[Dict[str, Any]]:
        """Ariza holatini yangilaydi va yangilangan ma'lumotni qaytaradi."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            await db.execute("""
                UPDATE applications SET status = ? WHERE id = ?;
            """, (new_status, app_id))
            await db.commit()

        return await self.get_application(app_id)

    async def get_stats(self) -> Dict[str, Any]:
        """Statistika ma'lumotlarini hisoblaydi."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Jami arizalar
            async with db.execute("SELECT COUNT(*) as count FROM applications;") as c:
                row = await c.fetchone()
                total_apps = row["count"] if row else 0

            # Kurslar kesimida
            async with db.execute("""
                SELECT course_name, COUNT(*) as count 
                FROM applications 
                GROUP BY course_name;
            """) as c:
                course_stats = [dict(r) for r in await c.fetchall()]

            # Statuslar kesimida
            async with db.execute("""
                SELECT status, COUNT(*) as count 
                FROM applications 
                GROUP BY status;
            """) as c:
                status_stats = [dict(r) for r in await c.fetchall()]

            return {
                "total_apps": total_apps,
                "courses": course_stats,
                "statuses": status_stats
            }

    async def export_applications(self) -> List[Dict[str, Any]]:
        """Barcha arizalarni eksport uchun ro'yxat shaklida oladi."""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT a.id, a.created_at, u.full_name, u.phone_number, u.username,
                       a.course_name, a.study_format, a.preferred_time, a.district, a.status
                FROM applications a
                JOIN users u ON a.user_id = u.user_id
                ORDER BY a.id DESC;
            """) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]
