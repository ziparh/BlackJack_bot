import logging

import aiosqlite
import asyncio

from option import DB_URL

class DataBase:
    def __init__(self):
        self.conn = None

    async def __aenter__(self):
        """Асинхронное контекстное управление: автоматическое подключение."""
        self.conn = await aiosqlite.connect(DB_URL)
        await self.conn.execute("PRAGMA foreign_keys = ON;")
        await self.conn.commit()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрытие соединения при выходе из контекста."""
        await self.conn.close()

    async def create_db(self):
        await self.conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name TEXT NOT NULL,
                    balance INTEGER NOT NULL DEFAULT 100
                )
                ''')
        await self.conn.commit()

    async def add_user(self, user_id, name):
        try:
            await self.conn.execute('''
                INSERT INTO users (user_id, name)
                VALUES (?, ?)
                ''', (user_id, name))
            await self.conn.commit()
        except Exception as e:
            logging.error(f'Ошибка при добавлении пользователя: {e}')

    async def get_user(self, user_id):
        try:
            query = await self.conn.execute('''
                SELECT * FROM users
                where user_id = ?
                LIMIT 1
                ''', (user_id,))
            result = await query.fetchone()
            return result
        except Exception as e:
            logging.error(f'Ошибка при получения пользователя: {e}')



