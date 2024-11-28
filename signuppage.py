import tkinter as tk
import customtkinter as ctk
from PIL import ImageTk, Image

from expensepage import second_page
from db import db

def signUp_page(frame1, app):
    frame1.destroy()
    # def go_first_page():
    #     first_page()
    def submit(): 
        get_userid = userid_entry.get()
        get_name = name_entry.get()
        get_password = password_entry.get()
        print(get_userid, get_name, get_password)
        if get_userid == "" or get_name == "" or get_password == "":
            tk.messagebox.showerror("Sign Up info", "All fields are required.")
            return

        if db.userinfo.find_one({"userid": get_userid}):
            tk.messagebox.showerror("Sign Up", "User ID is already taken.")
            return

        db.userinfo.insert_one({
            "userid": get_userid,
            "password": get_password,
            "user_name": get_name
        })
        second_page(frame1, get_userid, app)

    frame1 = ctk.CTkFrame(app, width=3200, height=2000, fg_color="#222")
    frame1.pack()
    # img1 = ImageTk.PhotoImage(Image.open("background.jpg").resize((3200, 2000)))
    # img1_place = ctk.CTkLabel(master=frame1, image=img1, text="")
    # img1_place.pack()

    # img2 = ImageTk.PhotoImage(Image.open("side.png").resize((800, 1200)))
    # img2_place = ctk.CTkLabel(master=frame1, image=img2, text="")
    # img2_place.place(x=30, y=370)

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
        height=450,
        corner_radius=20,
        fg_color="#333",
        border_width=5,
    )

    frame2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    l2 = ctk.CTkLabel(
        master=frame2, text="Sign Up", font=("Ubuntu", 30), text_color="#fff"
    )
    l2.place(x=120, y=40)
    username = ctk.CTkLabel(
        master=frame2,
        text="Username",
        font=("Century Gothic", 15, 'bold'),
        text_color="#fff",
    )
    username.place(x=55, y=85)
    userid_entry = ctk.CTkEntry(
        master=frame2, width=220, placeholder_text="Username", corner_radius=26
    )

    userid_entry.place(x=50, y=110)

    name = ctk.CTkLabel(
        master=frame2,
        text="Full Name",
        font=("Century Gothic", 15, 'bold'),
        text_color="#fff",
    )
    name.place(x=55, y=145)
    name_entry = ctk.CTkEntry(
        master=frame2, width=220, placeholder_text="Name", corner_radius=26
    )

    name_entry.place(x=50, y=180)
    password = ctk.CTkLabel(
        master=frame2,
        text="Password",
        font=("Century Gothic", 15, 'bold'),
        text_color="#fff",
    )
    password.place(x=50, y=215)

    password_entry = ctk.CTkEntry(
        master=frame2,
        width=220,
        placeholder_text="Password",
        show="*",
        corner_radius=26,
    )
    password_entry.place(x=50, y=250)
    button1 = ctk.CTkButton(
        master=frame2,
        width=220,
        text="Submit",
        corner_radius=6,
        fg_color="#6600FF",
        command=submit,
    )
    button1.pack()
    button1.place(x=50, y=295)

    button2 = ctk.CTkButton(
        master=frame2,
        width=220,
        text="Log In ",
        corner_radius=6,
        fg_color="#6600FF",
        # command=go_first_page,
    )
    button2.pack()
    button2.place(x=50, y=340)