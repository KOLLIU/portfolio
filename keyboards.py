from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from sqlalchemy import select

from db import CityDB

city_callback = CallbackData("city", "number")


async def get_cities_keyboard(db_session, title):
    title = title.lower()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[]])
    async with db_session() as session:
        rows = (await session.execute(select(CityDB).where(CityDB.title.like(f'%{title}%')))).fetchall()
        for row in rows:
            keyboard.insert(InlineKeyboardButton(text=f"{row[0].number}) {row[0].title.capitalize()}",
                                                 callback_data=city_callback.new(number=row[0].number)))
            keyboard.row()

    return keyboard
