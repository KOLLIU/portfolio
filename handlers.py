from aiogram import types, Dispatcher
from sqlalchemy import select

from db import CityDB
from keyboards import get_cities_keyboard, city_callback
from parsing import parse_url, City


async def start_help(message: types.Message):
    text = """Тестовое задание
/parse - парсинг сайта и обновление (добавление) городов в базе данных
При отправке других сообщений бот попытается найти города с таким названием (частью названия)"""
    await message.answer(text)


async def parse(message: types.Message):
    db_session = message.bot.get("db")

    await message.answer("Идёт парсинг, это может занять некоторое время")

    cities = parse_url(url="https://ru.wikipedia.org/wiki/Городские_населённые_пункты_Московской_области")
    await cities.update_cities(db_session)

    await message.answer(cities, disable_web_page_preview=True)


async def search(message: types.Message):
    db_session = message.bot.get("db")

    keyboard = await get_cities_keyboard(db_session=db_session, title=message.text)

    await message.answer(text="Найденные города", reply_markup=keyboard)


async def city_message(call: types.CallbackQuery, callback_data: dict):
    number = int(callback_data["number"])

    async with call.bot.get("db")() as session:
        city_row = (await session.execute(select(CityDB).where(CityDB.number == number))).fetchone()
        city = City(db_row=city_row)

        await call.message.answer(str(city))
        await call.message.delete()


def register_commands(dp: Dispatcher):
    dp.register_message_handler(start_help, commands=["start", "help"])
    dp.register_message_handler(parse, commands="parse")
    dp.register_message_handler(search)
    dp.register_callback_query_handler(city_message, city_callback.filter())
