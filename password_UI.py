from tkinter import *
import socket
import hashlib
import keyboard



root = Tk()

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MSG = "disconnect"
USER_WARNING = "WARNING!"
SERVER = socket.gethostbyname(socket.gethostname()) #use pv4 if local, use public ip if connection beyond local is needed
ADDR = (SERVER, PORT)

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
count = 0
PASSWORD = None


root.title("PROJECT LOCKER")

root.attributes("-fullscreen", True)



e =Entry(root, width=50)
e.place(width=200, height=50, x=width/2-75, y=height/2-25)
e.insert(0, "Enter password")


#functions for create password window
def open_create_password_wind():
    

    create_wind = Toplevel(root)
    create_wind.title("Create Password")

    new_pass_entry = Entry(create_wind, width=50)
    new_pass_entry.pack()

    def new_pass():
        global PASSWORD
        PASSWORD = hash_password(new_pass_entry.get())
        create_wind.destroy()

    enterPassButton = Button(create_wind, text="Enter new password", command=new_pass)
    enterPassButton.pack()

#send warning to bot 

def send_to_message_server():
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)

        send(USER_WARNING, client)
        send(DISCONNECT_MSG, client)
    except (ConnectionRefusedError, ConnectionError, TimeoutError) as e:
        print(f"Error connecting to the server: {e}")

def send(mssg, clt):
    message = mssg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    clt.send(send_length)
    clt.send(message)
    



#functions for main_window
    
def on_closing():
    pass

def hash_password(password: str):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def check_password( stored_hashed_password: str):
    global count
    entered_password = e.get()
    entered_password_hashed = hash_password(entered_password)

    if entered_password_hashed == stored_hashed_password:
        root.destroy()
    else:
        count += 1
        if count > 2:
            send_to_message_server()





enterButton = Button(root, text="Enter", command=lambda: check_password(PASSWORD) )
enterButton.place(x=width/2, y=height/2+25)

root.protocol("WM_DELETE_WINDOW", on_closing)




label_button = "Create Password"
createButton = Button(root, text=label_button, command=open_create_password_wind)
createButton.place(x=width/2, y=height/2+50)

# update createButton text
def update_create_button():
    global label_button
    if PASSWORD is None:
        label_button = "Create Password"
    else:
        label_button = "Change Password"

    createButton.config(text=label_button)
    root.after(1000, update_create_button)

update_create_button()
    

if __name__ == "__main__":
    keyboard.block_key('tab')
    keyboard.block_key('alt')

    root.mainloop()

    

    