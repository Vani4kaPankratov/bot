import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from yt_dlp import YoutubeDL

TOKEN = "8564487065:AAEAhefvbVI0XgTPidMRppCBGfylPdpJqcc"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("👋 Привіт! Встав посилання на YouTube-відео 🎥")

@dp.message()
async def download_video(message: types.Message):
    url = message.text
    msg = await message.answer("⏳ Конвертую, зачекай...")

    ydl_opts = {
        "format": "mp4",
        "outtmpl": "%(id)s.%(ext)s"
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await msg.edit_text("✅ Готово! Надсилаю файл 📤")

        await message.answer_document(
            types.FSInputFile(filename)
        )

        os.remove(filename)

    except Exception as e:
        await msg.edit_text(f"❌ Помилка: {e}")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
