from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
import asyncio
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
form_router = Router()


@form_router.message(F.text.casefold() == "/start")
async def start(message: types.Message):
    await message.answer(f"Send or forward a message, media or file to this bot to retrieve user info.")


@form_router.message()
async def handle_media(message: types.Message):
    if message.forward_from:
        user = message.forward_from
    elif message.forward_from_chat:
        user = message.forward_from_chat
    else:
        user = message.from_user

    if isinstance(user, types.Chat):
        if user.type in ('group', 'supergroup', 'channel'):
            if user.username:
                member_count = await bot.get_chat_member_count(user.id)
                await message.answer(text=f"<b>ID:</b>  <code>{user.id}</code>\n"
                                          f"<b>Name:</b>  {user.title}\n"
                                          f"<b>Username:</b>  @{user.username}\n"
                                          f"<b>Participants:</b>  {member_count}", parse_mode=ParseMode.HTML)
            else:
                await message.answer(text=f"<b>ID:</b>  <code>{user.id}</code>\n"
                                          f"<b>Name:</b>  {user.title}\n"
                                          f"<b>Username:</b>  <i>UNAVAILABLE</i>\n"
                                          f"<b>Participants:</b>  <i>UNAVAILABLE</i>", parse_mode=ParseMode.HTML)
    else:
        await message.answer(text=f"<b>ID:</b>  <code>{user.id}</code>\n"
                                  f"<b>Name:</b>  {user.full_name}\n"
                                  f"<b>Username:</b>  @{user.username}\n"
                                  f"<b>Link:</b>  <a href='tg://user?id={user.id}'>🔗 {user.full_name}</a>", parse_mode=ParseMode.HTML)


async def main():
    dp = Dispatcher()
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
