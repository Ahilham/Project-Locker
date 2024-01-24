import logging
from get_location import get_loc
from typing import Final
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
import socket
import threading
import requests
import time


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


TOKEN: Final = "yur bot token" # bot token
BOT_USERNAME: Final = 'your bot username' # bot username
base_url = f"https://api.telegram.org/bot{TOKEN}"
update_url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
chat_id = None
send_msg_url = None

location = get_loc()
lis = location.get_device_location()
IP_device = f"City: {lis[0]}, region: {lis[1]}, country: {lis[2]}, lattitude: {lis[4]}, longitude: {lis[5]}"




HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
USER_WARNING = "WARNING!"
DISCONNECT_MSG = "disconnect"



bot = Bot(token = TOKEN)



#commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello Sir/Miss, how can i help you?")

    global send_msg_url
    global chat_id
    global IP_device

    time.sleep(5)

    response = requests.get(update_url)

    if response.status_code == 200:
        json_data = response.json()

        chat_id = json_data["result"][0]["message"]["chat"]["id"]

    send_msg_url = base_url+f"/sendMessage?chat_id={chat_id}&text={IP_device}"



async def send_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(IP_device)

async def send_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if chat_id:
        await update.message.reply_text(chat_id) 
    else:
        await update.message.reply_text("ERROR: No chat id is present.")

#socket server
def handle_client(conn, addr):
    global send_msg_url

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
    app.add_handler(CommandHandler('send_chat_id', send_chat_id))
    app.add_handler(CommandHandler('start', start_command))
    app.add_error_handler(error)

    print("Polling...")
    app.run_polling(poll_interval=3)

    
    

    
    
