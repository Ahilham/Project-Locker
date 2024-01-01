from tkinter import *
import hashlib

root = Tk()

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
count = 0
PASSWORD = None

root.title("PROJECT LOCKER")

# root.attributes("-fullscreen", True)




e =Entry(root, width=50)
e.place(width=200, height=50, x=width/2-75, y=height/2-25)
e.insert(0, "Enter password")

#functions for create password window
def open_create_password_wind():
    

    create_wind = Toplevel(root)
    create_wind.title("Create Password")

    new_pass_entry = Entry(create_wind, width=50).pack()

    def new_pass():
        global PASSWORD
        PASSWORD = hash_password(new_pass_entry.get())
        create_wind.destroy()

    enterPassButton = Button(create_wind, text="Enter new password", command=new_pass)
    enterPassButton.pack()







#functions for main_window


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
        count +=1



enterButton = Button(root, text="Enter", command=lambda: check_password(PASSWORD) ).place(x=width/2, y=height/2+25)
if not PASSWORD:
    createButton = Button(root, text="Create Password", command=open_create_password_wind).place(x=width/2, y=height/2+50)

root.mainloop()