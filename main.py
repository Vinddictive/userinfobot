from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command

import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Send or forward a message, media or file to this bot to retrieve user info.")


# Handler for all messages
@router.message()
async def handle_media(message: types.Message):
    # Check if the message is forwarded from a user or a chat
    if message.forward_from:
        user = message.forward_from
    elif message.forward_from_chat:
        user = message.forward_from_chat
    else:
        user = message.from_user

    # If the user is a chat (group, supergroup, or channel)
    if isinstance(user, types.Chat):
        if user.type in ('group', 'supergroup', 'channel'):
            member_count = await bot.get_chat_member_count(user.id)
            await message.answer(text=f"<b>ID:</b>  <code>{user.id}</code>\n"
                                      f"<b>Name:</b>  {user.title}\n"
                                      f"<b>Username:</b>  @{user.username if user.username else 'UNAVAILABLE'}\n"
                                      f"<b>Participants:</b>  {member_count if user.username else 'UNAVAILABLE'}")
    else:
        # For individual users, display their ID, full name, username, and a link to their profile
        await message.answer(text=f"<b>ID:</b>  <code>{user.id}</code>\n"
                                  f"<b>Name:</b>  {user.full_name}\n"
                                  f"<b>Username:</b>  @{user.username}\n"
                                  f"<b>Link:</b>  <a href='tg://user?id={user.id}'>🔗 {user.full_name}</a>")


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
