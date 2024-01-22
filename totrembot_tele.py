import logging
import asyncio
from get_location import get_loc
from typing import Final
from telegram import Bot, Update
from telegram.ext import Application, Updater, CommandHandler, MessageHandler, filters, ContextTypes, CallbackContext
import socket
import threading
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


TOKEN: Final = "6857877317:AAE6GJNZJGAlce7Wm86RxWX0hPxkgazV74w"
BOT_USERNAME: Final = '@totrembot'
base_url = f"https://api.telegram.org/bot{TOKEN}"
chat_id = None

location = get_loc()
lis = location.get_device_location()
IP_device = f"City: {lis[0]}, region: {lis[1]}, country: {lis[2]}, lattitude: {lis[3]}, longitude: {lis[4]}"

send_msg_url = base_url+f"/sendMessage?chat_id={chat_id}&text={IP_device}"


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
USER_WARNING = "WARNING!"
DISCONNECT_MSG = "disconnect"



bot = Bot(token = TOKEN)

#commands

async def send_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = get_loc()
    lis = location.get_device_location()
    await update.message.reply_text(IP_device)

#socket server
def handle_client(conn, addr):
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            if msg == USER_WARNING:
                requests.get(send_msg_url)
    conn.close()


#error return
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# async def run_bot():
#     app = Application.builder().token(TOKEN).build()

#     thread = threading.Thread(target=run_server)

#     app.add_handler(CommandHandler('send_loc', send_location))
#     app.add_error_handler(error)

#     print("Polling...")
#     app.run_polling(poll_interval=3)

def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print("listening...")
    

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)
    

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    thread = threading.Thread(target=run_server)
    thread.start()

    app.add_handler(CommandHandler('send_loc', send_location))
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)
    #set up an input for chat_id

    
    
