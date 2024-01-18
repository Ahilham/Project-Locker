import logging
import asyncio
from get_location import get_loc
from typing import Final
from telegram import Bot, Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import socket
import threading


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN: Final = "6857877317:AAE6GJNZJGAlce7Wm86RxWX0hPxkgazV74w"
BOT_USERNAME: Final = '@totrembot'
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
USER_WARNING = "WARNING!"
DISCONNECT_MSG = "!disconnect"



bot = Bot(token = TOKEN)

#commands

async def send_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = get_loc()
    lis = location.get_device_location()
    await update.message.reply_text(f"City: {lis[0]}, region: {lis[1]}, country: {lis[2]}, lattitude: {lis[3]}, longitude: {lis[4]}")

#socket server
async def handle_client(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            conn.send("MESSAGE RECEIVED").encode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            if msg == USER_WARNING:
                await send_location()
                connected = False


#error return
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def run_bot():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('send_loc', send_location))
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)

async def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("listening...")
    while True:
        conn, addr = server.accept()
        await handle_client(conn, addr)
        asyncio.create_task(handle_client(conn, addr))
    


if __name__ == '__main__':
        thread = threading.Thread(target=run_server)
        thread.start()

        run_bot()
    
    
