import customtkinter as ctk
from datetime import datetime
from db import db
import pandas as pd

def show_add_expense(frame, userid):
    frame.tkraise()
    
    def submit_expense():
        get_amount = amount_entry.get()
        get_expense_type = expense_type_combobox.get()
        get_date_str = date_entry.get()
        get_comments = comment_entry.get("1.0", ctk.END).strip()

        try:
            get_date = datetime.strptime(get_date_str, "%d/%m/%Y")
        except ValueError:
            print("Invalid date format. Please use dd/mm/yyyy.")
            return
        try:
            db.expense.insert_one({
                "userid": userid,
                "date": get_date,
                "expense_type": get_expense_type,
                "amount": int(get_amount),
                "comment": get_comments
            })
        except Exception as e:
            print("Error inserting expense:", e)

        amount_entry.delete(0, ctk.END)
        expense_type_combobox.set("Food & Dining") 
        date_entry.delete(0, ctk.END)
        date_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
        comment_entry.delete("1.0", ctk.END) 

    frame.configure(fg_color="#222222", bg_color="#222222")

    form_frame = ctk.CTkFrame(frame, width=600, height=500, fg_color="#333", border_width=5, corner_radius=20)
    form_frame.place(relx=0.5, rely=0.5, anchor="center")

    amount_label = ctk.CTkLabel(form_frame, text="Amount", font=("Ubuntu", 16, "bold"), text_color="#FFFFFF")
    amount_label.grid(row=0, column=0, padx=(20, 10), pady=(40, 20), sticky="e")
    amount_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter Amount", font=("Ubuntu", 16), corner_radius=10, fg_color="#444", text_color="#FFFFFF")
    amount_entry.grid(row=0, column=1, padx=(10, 20), pady=(40, 20), sticky="w")

    expense_type_label = ctk.CTkLabel(form_frame, text="Expense Type", font=("Ubuntu", 16, "bold"), text_color="#FFFFFF")
    expense_type_label.grid(row=1, column=0, padx=(20, 10), pady=(20, 20), sticky="e")
    expense_type_combobox = ctk.CTkComboBox(form_frame, values=["Groceries", "Food & Dining", "Transportation", "Housing", "Education", "Utilities", "Shopping", "Health", "Entertainment", "Insurance" ,"Other", "Income"], font=("Ubuntu", 16), width=300, fg_color="#444", text_color="#FFFFFF")
    expense_type_combobox.grid(row=1, column=1, padx=(10, 20), pady=(20, 20), sticky="w")

    date_label = ctk.CTkLabel(form_frame, text="Date (dd/mm/yyyy)", font=("Ubuntu", 16, "bold"), text_color="#FFFFFF")
    date_label.grid(row=2, column=0, padx=(20, 10), pady=(20, 20), sticky="e")
    date_entry = ctk.CTkEntry(form_frame, width=300, placeholder_text="Enter Date", font=("Ubuntu", 16), corner_radius=10, fg_color="#444", text_color="#FFFFFF")
    date_entry.insert(0, datetime.now().strftime('%d/%m/%Y'))
    date_entry.grid(row=2, column=1, padx=(10, 20), pady=(20, 20), sticky="w")

    comment_label = ctk.CTkLabel(form_frame, text="Comments", font=("Ubuntu", 16, "bold"), text_color="#FFFFFF")
    comment_label.grid(row=3, column=0, padx=(20, 10), pady=(20, 20), sticky="e")
    comment_entry = ctk.CTkTextbox(form_frame, width=300, height=100, font=("Ubuntu", 16),corner_radius=10, fg_color="#444", text_color="#FFFFFF")
    comment_entry.grid(row=3, column=1, padx=(10, 20), pady=(20, 20), sticky="w")

    submit_button = ctk.CTkButton(form_frame, width=300, text="Submit", corner_radius=10, fg_color="#6600FF", text_color="white", hover_color="#5200CC", font=("Ubuntu", 16, "bold"), command=submit_expense)
    submit_button.grid(row=4, column=0, columnspan=2, pady=(40, 20))