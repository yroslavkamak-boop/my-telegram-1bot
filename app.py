import os
import threading
import asyncio
import aiohttp
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = "8767724431:AAGTvwRYED9dy-eJsph94lfh2mFPasqNm4Y"

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

async def start(update, context):
    await update.message.reply_text("Чего надо? Пиши давай.")

async def rude_ai(update, context):
    user_msg = update.message.text
    await update.message.reply_chat_action("typing")
    url = f"https://text.pollinations.ai/Отвечай грубо и кратко, 1-3 слова. Вопрос: {user_msg}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=30) as response:
                reply = await response.text() if response.status == 200 else "Ошибка"
                await update.message.reply_text(reply[:500])
    except:
        await update.message.reply_text("❌ Ошибка")

def run_bot():
    async def main():
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, rude_ai))
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        print("Бот запущен!")
        try:
            while True:
                await asyncio.sleep(1)
        finally:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
    asyncio.run(main())

if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
