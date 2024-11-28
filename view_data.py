import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, filedialog
from datetime import datetime, timedelta
from db import db
import csv
import json
from fpdf import FPDF

def show_view_data(frame, userid):
    for widget in frame.winfo_children():
        widget.destroy()

    frame.filtered_data = []
    frame.current_filters = {}

    def fetch_data(filters=None):
        query = {"userid": userid}

        if filters:
            if filters["category"]:
                query["expense_type"] = filters["category"]

            if filters["amount_min"] or filters["amount_max"]:
                query["amount"] = {}
                if filters["amount_min"]:
                    query["amount"]["$gte"] = filters["amount_min"]
                if filters["amount_max"]:
                    query["amount"]["$lte"] = filters["amount_max"]

            if filters["start_date"] and filters["end_date"]:
                try:
                    start_date = datetime.strptime(filters["start_date"], "%Y-%m-%d")
                    end_date = datetime.strptime(filters["end_date"], "%Y-%m-%d")
                    query["date"] = {"$gte": start_date, "$lte": end_date}
                except ValueError as e:
                    print("Date format error:", e)

        result = list(db.expense.find(query))
        return result

    def apply_filters():
        filters = {
            "category": category_combobox.get() if category_combobox.get() != "All" else None,
            "amount_min": int(min_amount_entry.get()) if min_amount_entry.get() else None,
            "amount_max": int(max_amount_entry.get()) if max_amount_entry.get() else None,
            "start_date": start_date_entry.get(),
            "end_date": end_date_entry.get(),
        }
        frame.filtered_data = fetch_data(filters)
        frame.current_filters = filters
        display_data(frame.filtered_data)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(4, weight=1)

    frame.configure(fg_color="#222222", bg_color="#222222")

    category_label = ctk.CTkLabel(frame, text="Category", text_color="#FFFFFF", font=("Arial", 12))
    category_label.grid(row=0, column=1, padx=10, pady=10)
    category_combobox = ctk.CTkComboBox(frame, values=["All", "Groceries", "Food & Dining", "Transportation", "Housing", "Education", "Utilities", "Shopping", "Health", "Entertainment", "Insurance" ,"Other", "Income"], text_color="#FFFFFF", bg_color="#333333", button_color="#444444", button_hover_color="#555555")
    category_combobox.grid(row=0, column=2, padx=10, pady=10)

    amount_label = ctk.CTkLabel(frame, text="Amount Range", text_color="#FFFFFF", font=("Arial", 12))
    amount_label.grid(row=1, column=1, padx=10, pady=10)
    min_amount_entry = ctk.CTkEntry(frame, placeholder_text="Min", text_color="#FFFFFF", bg_color="#333333")
    min_amount_entry.grid(row=1, column=2, padx=5, pady=5)
    max_amount_entry = ctk.CTkEntry(frame, placeholder_text="Max", text_color="#FFFFFF", bg_color="#333333")
    max_amount_entry.grid(row=1, column=3, padx=5, pady=5)

    date_label = ctk.CTkLabel(frame, text="Date Range", text_color="#FFFFFF", font=("Arial", 12))
    date_label.grid(row=2, column=1, padx=10, pady=10)
    start_date_entry = ctk.CTkEntry(frame, placeholder_text="Start Date (YYYY-MM-DD)", text_color="#FFFFFF", bg_color="#333333")
    start_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
    start_date_entry.grid(row=2, column=2, padx=5, pady=5)
    end_date_entry = ctk.CTkEntry(frame, placeholder_text="End Date (YYYY-MM-DD)", text_color="#FFFFFF", bg_color="#333333")
    end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    end_date_entry.grid(row=2, column=3, padx=5, pady=5)

    apply_button = ctk.CTkButton(frame, text="Apply Filters", command=apply_filters, fg_color="#6600FF", hover_color="#8C52FF")
    apply_button.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", 
                    font=("Arial", 14), 
                    background="#333333", 
                    fieldbackground="#333333", 
                    foreground="#FFFFFF",
                    rowheight=50, 
                    highlightthickness=0,
                    borderwidth=0)
    style.configure("Treeview.Heading", 
                    font=("Arial", 16, "bold"), 
                    background="#444444", 
                    foreground="#DDDDDD", 
                    borderwidth=0)
    style.map("Treeview", 
              background=[("selected", "#444444")], 
              foreground=[("selected", "#FFFFFF")])
    
    rounded_frame = ctk.CTkFrame(frame, corner_radius=10, fg_color="#444444")
    rounded_frame.grid(row=4, column=1, columnspan=3, padx=10, pady=20, sticky="nsew")

    tree = ttk.Treeview(rounded_frame, columns=("Date", "Category", "Description", "Amount"), 
                        show="headings", padding=10)
    tree.heading("Date", text="Date")
    tree.heading("Category", text="Category")
    tree.heading("Description", text="Description")
    tree.heading("Amount", text="Amount")
    tree.column("Date", width=150, anchor="center")
    tree.column("Category", width=150, anchor="center")
    tree.column("Description", width=250, anchor="center")
    tree.column("Amount", width=100, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def display_data(data):
        for row in tree.get_children():
            tree.delete(row)
        for expense in data:
            date_only = expense["date"].strftime("%Y-%m-%d")
            tree.insert("", "end", values=(date_only, expense["expense_type"], expense["comment"], expense["amount"]))

    apply_filters()

    button_frame = ctk.CTkFrame(frame, fg_color="#444444")
    button_frame.grid(row=5, column=1, columnspan=3, pady=(0, 10))

    def export_to_csv():
        folder = filedialog.askdirectory(title="Select Folder to Save CSV")
        if folder:
            with open(f"{folder}/expenses.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Description", "Amount"])
                for expense in frame.filtered_data:
                    date_only = expense["date"].strftime("%d/%m/%Y")
                    writer.writerow([date_only, expense["expense_type"], expense["comment"], expense["amount"]])

    def export_to_json():
        folder = filedialog.askdirectory(title="Select Folder to Save JSON")
        if folder:
            for expense in frame.filtered_data:
                if isinstance(expense["date"], str):
                    try:
                        expense["date"] = datetime.strptime(expense["date"], "%Y-%m-%d")
                    except ValueError:
                        print(f"Date format error for {expense['date']}")

            with open(f"{folder}/expenses.json", "w") as file:
                json.dump(frame.filtered_data, file, default=str, indent=4)

    def export_to_pdf():
        folder = filedialog.askdirectory(title="Select Folder to Save PDF")
        if folder:
            pdf = FPDF()
            pdf.add_page()
            
            pdf.set_font("Arial", size=16)
            pdf.cell(200, 10, txt="Expense Report", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt="Applied Filters:", ln=True)
            pdf.set_font("Arial", size=10)
            
            pdf.cell(200, 10, f"Category: {frame.current_filters['category'] if frame.current_filters['category'] else 'All'}", ln=True)
            pdf.cell(200, 10, f"Amount Range: {frame.current_filters['amount_min'] if frame.current_filters['amount_min'] else 'Min'} - {frame.current_filters['amount_max'] if frame.current_filters['amount_max'] else 'Max'}", ln=True)
            pdf.cell(200, 10, f"Date Range: {frame.current_filters['start_date'] if frame.current_filters['start_date'] else 'Start'} - {frame.current_filters['end_date'] if frame.current_filters['end_date'] else 'End'}", ln=True)
            pdf.ln(10)

            pdf.set_font("Arial", size=12)
            pdf.cell(40, 10, "Date", 1)
            pdf.cell(40, 10, "Category", 1)
            pdf.cell(60, 10, "Description", 1)
            pdf.cell(30, 10, "Amount", 1)
            pdf.ln()

            for expense in frame.filtered_data:
                date_only = expense["date"].strftime("%Y-%m-%d")
                pdf.cell(40, 10, date_only, 1)
                pdf.cell(40, 10, expense["expense_type"], 1)
                pdf.cell(60, 10, expense["comment"], 1)
                pdf.cell(30, 10, str(expense["amount"]), 1)
                pdf.ln()

            pdf.output(f"{folder}/filtered_expenses_report.pdf")

    pdf_button = ctk.CTkButton(button_frame, text="Export to PDF", command=export_to_pdf, fg_color="#009688", hover_color="#00C1A5")
    pdf_button.grid(row=0, column=0, padx=10, pady=10)

    csv_button = ctk.CTkButton(button_frame, text="Export to CSV", command=export_to_csv, fg_color="#3F51B5", hover_color="#5670D8")
    csv_button.grid(row=0, column=1, padx=10, pady=10)

    json_button = ctk.CTkButton(button_frame, text="Export to JSON", command=export_to_json, fg_color="#FF5722", hover_color="#FF784A")
    json_button.grid(row=0, column=2, padx=10, pady=10)