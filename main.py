import asyncio
from os import getenv

from aiogram import Bot, Dispatcher

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from handlers import register_commands

token = str(getenv("BOT_TOKEN"))

host = token = str(getenv("PG_HOST"))
pg_user = token = str(getenv("BOT_USER"))
db_name = token = str(getenv("BOT_NAME"))
password = token = str(getenv("BOT_PASSWORD"))


async def main():
    engine = create_async_engine(
        f"postgresql+asyncpg://{pg_user}:{password}@{host}/{db_name}",
        future=True
    )

    async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    bot = Bot(token, parse_mode="HTML")
    bot["db"] = async_sessionmaker
    dp = Dispatcher(bot)

    register_commands(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


asyncio.run(main())
