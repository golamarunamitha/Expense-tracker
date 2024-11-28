import tkinter as tk
import customtkinter as ctk

from expensepage import second_page
from signuppage import signUp_page
from db import db

def first_page(app):  
    def submit(): 
        get_userid = entry1.get()
        get_password = entry2.get()
        if get_userid == "" or get_password == "":
            tk.messagebox.showerror("Login info", "All fields are required.")
            return

        user = db.userinfo.find_one({"userid": get_userid, "password": get_password})

        if user:
            second_page(frame1, get_userid, app)
        else:
            tk.messagebox.showerror("Login info", "Invalid credentials.")

    def signUp_page_call():
        signUp_page(frame1, app)

    frame1 = ctk.CTkFrame(app, width=3200, height=2000, fg_color="#222222")
    frame1.pack()

    main_label = ctk.CTkLabel(
        master=frame1,
        text="Take control of your expenses, unlock financial freedom",
        font=("Comic Sans MS", 50),
        text_color="#fff",
    )
    main_label.place(relx=0.1, rely=0.1)

    frame2 = ctk.CTkFrame(
        frame1,
        width=320,
        height=350,
        corner_radius=20,
        fg_color="#333",
        border_width=5,
    )

    frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    l2 = ctk.CTkLabel(
        master=frame2, text="Log in", font=("Ubuntu", 30), text_color="#fff"
    )
    l2.place(x=120, y=40)
    l3 = ctk.CTkLabel(
        master=frame2,
        text="Username",
        font=("Century Gothic", 15, 'bold'),
        text_color="#fff",
    )
    l3.place(x=55, y=85)
    entry1 = ctk.CTkEntry(
        master=frame2, width=220, placeholder_text="Username", corner_radius=26
    )

    entry1.place(x=50, y=110)
    l4 = ctk.CTkLabel(
        master=frame2,
        text="Password",
        font=("Century Gothic", 15, 'bold'),
        text_color="#fff",
    )
    l4.place(x=55, y=140)

    entry2 = ctk.CTkEntry(
        master=frame2,
        width=220,
        placeholder_text="Password",
        show="*",
        corner_radius=26,
    )
    entry2.place(x=50, y=165)

    button1 = ctk.CTkButton(
        master=frame2,
        width=220,
        text="Login",
        corner_radius=6,
        fg_color="#6600FF",
        command=submit,
    )
    button1.pack()
    button1.place(x=50, y=240)

    button2 = ctk.CTkButton(
        master=frame2,
        width=220,
        text="New User ",
        corner_radius=6,
        fg_color="#6600FF",
        command=signUp_page_call,
    )
    button2.pack()
    button2.place(x=50, y=300)