import logging
import time
import asyncio
from get_location import get_loc
from typing import Final
from telegram import Bot, Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN: Final = "6857877317:AAE6GJNZJGAlce7Wm86RxWX0hPxkgazV74w"
BOT_USERNAME: Final = '@totrembot'

bot = Bot(token = TOKEN)

#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello Sir, how can i help you?')

async def send_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = get_loc()
    lis = location.get_device_location()
    await update.message.reply_text(f"City: {lis[0]}, region: {lis[1]}, country: {lis[2]}, lattitude: {lis[3]}, longitude: {lis[4]}")

async def check_and_send_location(check_pass: bool):
    if check_pass:
        await send_location(update=None, context=None)

async def periodic_check():
    while True:
        condition_result = check_pass()

        await check_and_send_location(condition_result)

        await asyncio.sleep(60)

#error return
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


if __name__ == '__main__':
    for i in range(3):
        print(f'program starting in {3-i}')
        time.sleep(1)
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('send_loc', send_location))

    asyncio.create_task(periodic_check())

    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)