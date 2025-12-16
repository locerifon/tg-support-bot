import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 1435566238 # твой Telegram ID (ЧИСЛО)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------- /start ----------
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Привет!\n\n"
        "Ты можешь написать сюда любое сообщение — "
        "оно будет отправлено в поддержку.\n\n"
        "Мы обязательно ответим 🙂"
    )

# ---------- сообщения от пользователя ----------
@dp.message()
async def handle_messages(message: Message):
    # если пишет админ — обрабатываем отдельно
    if message.from_user.id == ADMIN_ID:
        # админ должен отвечать reply
        if not message.reply_to_message:
            await message.answer(
                "❗ Чтобы ответить пользователю, "
                "нужно ответить (reply) на его сообщение."
            )
            return

        # пытаемся вытащить ID пользователя из текста
        original = message.reply_to_message.text

        if not original.startswith("📩 Сообщение от"):
            await message.answer("❌ Это не сообщение от пользователя.")
            return

        try:
            user_id = int(original.split("ID:")[1].split("\n")[0].strip())
        except:
            await message.answer("❌ Не удалось определить пользователя.")
            return

        await bot.send_message(
            user_id,
            f"💬 Ответ от поддержки:\n\n{message.text}"
        )

        await message.answer("✅ Ответ отправлен")
        return

    # ---------- обычный пользователь ----------
    text_to_admin = (
        "📩 Сообщение от пользователя\n"
        f"ID: {message.from_user.id}\n\n"
        f"{message.text}"
    )

    await bot.send_message(ADMIN_ID, text_to_admin)
    await message.answer("✅ Сообщение отправлено в поддержку")

# ---------- запуск ----------
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
