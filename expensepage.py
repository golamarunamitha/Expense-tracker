import tkinter as tk
import customtkinter as ctk
from datetime import datetime, timedelta
from PIL import ImageTk, Image
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk

from db import db
from view_data import show_view_data
from view_analysis import show_view_analysis
from add_expense import show_add_expense 

def second_page(frame1, userid, app):
    def show_frame(frame):
        frame.tkraise()

    def show_view_data_frame():
        show_frame(view_data_frame) 
        show_view_data(view_data_frame, userid) 

    def show_analyze_data():
        show_frame(analyze_data_frame)
        show_view_analysis(analyze_data_frame, userid)

    from datetime import datetime

    def load_user_summary():
        now = datetime.now()
        current_year = now.year
        current_month = now.month

        expenses = list(db.expense.find({"userid": userid}))
        if not expenses:
            income = total_expense = 0
        else:
            df = pd.DataFrame(expenses)

            df['date'] = pd.to_datetime(df['date'])

            monthly_data = df[(df['date'].dt.year == current_year) & (df['date'].dt.month == current_month)]

            income = monthly_data[monthly_data['expense_type'] == 'Income']['amount'].sum()
            total_expense = monthly_data[monthly_data['expense_type'] != 'Income']['amount'].sum()

        income_label.configure(text=f"Income: ${income}")
        expense_label.configure(text=f"Total Expense: ${total_expense}")

    frame1.destroy()
    app.geometry(f"{app.winfo_screenwidth()}x{app.winfo_screenheight()}")

    main_frame = ctk.CTkFrame(app, width=app.winfo_screenwidth(), height=app.winfo_screenheight())
    main_frame.pack(fill="both", expand=True)

    nav_bar = ctk.CTkFrame(main_frame, height=60, fg_color="#333")
    nav_bar.pack(side="top", fill="x")

    add_expense_btn = ctk.CTkButton(nav_bar, text="Add Expense", command=lambda: show_add_expense(add_expense_frame, userid), fg_color="#6600FF", width=150)
    add_expense_btn.pack(side="left", padx=20, pady=10)

    view_data_btn = ctk.CTkButton(nav_bar, text="View Data", command=show_view_data_frame, fg_color="#6600FF", width=150)
    view_data_btn.pack(side="left", padx=20, pady=10)

    analyze_data_btn = ctk.CTkButton(nav_bar, text="Analyze Data", command=show_analyze_data, fg_color="#6600FF", width=150)
    analyze_data_btn.pack(side="left", padx=20, pady=10)

    add_expense_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5F5")
    view_data_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5F5")
    analyze_data_frame = ctk.CTkFrame(main_frame, fg_color="#F5F5F5")

    for frame in (add_expense_frame, view_data_frame, analyze_data_frame):
        frame.place(x=0, y=60, relwidth=1, relheight=1)

    income_label = ctk.CTkLabel(add_expense_frame, text="", font=("Ubuntu", 16), text_color="#fff")
    income_label.place(relx=0.4, y=100)
    
    expense_label = ctk.CTkLabel(add_expense_frame, text="", font=("Ubuntu", 16), text_color="#fff")
    expense_label.place(relx=0.5, y=100)
    
    user_label = ctk.CTkLabel(add_expense_frame, text=f"Welcome {userid}", font=("Ubuntu", 40), text_color="#fff")
    user_label.place(relx=0.58, y=20, anchor="ne")

    txt_box = ctk.CTkTextbox(view_data_frame, border_width=5, height=500, width=600, fg_color="#F5F5F5", font=("Ubuntu", 12), text_color="#fff")
    txt_box.pack(pady=20, padx=20)
    txt_box.configure(state="disabled")

    load_user_summary()
    show_add_expense(add_expense_frame, userid)