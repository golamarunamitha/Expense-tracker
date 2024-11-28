import customtkinter as ctk
import tkinter as tk
from datetime import datetime, timedelta
from tkinter import ttk, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fpdf import FPDF
from db import db
import matplotlib.dates as mdates

global fig
global summary_frame

def show_view_analysis(frame, userid):
    global fig
    global summary_frame 
    summary_frame = None

    for widget in frame.winfo_children():
        widget.destroy()

    def fetch_filtered_data(filters=None):
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
                    print("Filtering by Date Range:", start_date, "to", end_date)
                except ValueError as e:
                    print("Date format error:", e)
        
        return list(db.expense.find(query))

    def apply_filters_and_visualize():
        global fig

        filters = {
            "category": category_combobox.get() if category_combobox.get() != "All" else None,
            "amount_min": int(min_amount_entry.get()) if min_amount_entry.get() else None,
            "amount_max": int(max_amount_entry.get()) if max_amount_entry.get() else None,
            "start_date": start_date_entry.get(),
            "end_date": end_date_entry.get(),
        }
        
        data = fetch_filtered_data(filters)
        if data:
            df = pd.DataFrame(data)
            df["date"] = pd.to_datetime(df["date"])
            fig = visualize_data(df, filters["category"]) 
            display_summary(df)
            return fig 
        else:
            print("No data to visualize.")
            return None

    def visualize_data(df, category_filter=None):
        global fig
        category_colors = {
            "Groceries": "#FF5733",          
            "Food & Dining": "#FFC300",     
            "Transportation": "#007ACC",   
            "Housing": "#29A745",            
            "Education": "#FF6F61",        
            "Utilities": "#9C27B0",         
            "Shopping": "#FF4081",       
            "Health": "#00BFA5",         
            "Entertainment": "#CD4500",     
            "Insurance": "#C2185B",      
            "Other": "#2196F3"            
        }
        fig, axes = plt.subplots(1, 2 if not category_filter else 1, figsize=(10, 5.5))
        fig.patch.set_facecolor("#333")

        if not category_filter:
            sns.barplot(data=df[df["expense_type"] != "Income"], x="expense_type", y="amount", ax=axes[0], estimator=sum, errorbar=None, palette=category_colors, hue="expense_type", dodge=False, legend=False)
            axes[0].set_title("Total Expenses by Category", pad=20, color="white", fontsize=12)
            axes[0].set_xlabel("Category", color='white')
            axes[0].set_ylabel("Amount", color='white')
            axes[0].tick_params(axis='x', rotation=45, colors='white')
            axes[0].tick_params(axis='y', colors='white')

            df_expense_only = df[df["expense_type"] != "Income"].groupby("expense_type")["amount"].sum()
            category_colors_pie = [category_colors[category] for category in df_expense_only.index]
            axes[1].pie(df_expense_only, labels=df_expense_only.index, autopct='%1.1f%%', colors=category_colors_pie, textprops={'color': "white"})
            axes[1].set_title("Expense Distribution by Category", color='white')
        else:
            df["date"] = pd.to_datetime(df["date"], errors='coerce')
            sns.lineplot(data=df, x="date", y="amount", ax=axes, color="blue")
            axes.set_title(f"Expenses Over Time for {category_filter}", pad=20, color="white", fontsize=12)
            axes.set_xlabel("Date", color='white')
            axes.set_ylabel("Amount", color='white')
            axes.tick_params(axis='x', rotation=45, colors='white')
            axes.tick_params(axis='y', colors='white')

            axes.grid(True, color='#444', linestyle='--', linewidth=0.5)

            axes.xaxis.set_major_locator(mdates.AutoDateLocator())
            axes.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))

            axes.scatter(df["date"], df["amount"], color="blue", s=50, zorder=5) 

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().place(x=frame.winfo_width()/2 - 950, y=250) 

        return fig

    def display_summary(df):
        global summary_frame

        if summary_frame:
            summary_frame.destroy()

        df["date"] = pd.to_datetime(df["date"])
        daily_totals = df.groupby("date")["amount"].sum()
        max_expense_date = daily_totals.idxmax()
        min_expense_date = daily_totals.idxmin()

        summary_frame = ctk.CTkFrame(frame, fg_color="#2d2d2d", corner_radius=15)
        summary_frame.place(relx=0.75, rely=0.52, anchor="center", relwidth=0.25)

        title_label = ctk.CTkLabel(
            summary_frame,
            text="Summary",
            text_color="#fff",
            font=("Inter", 16, "bold")
        )
        title_label.pack(pady=(15, 5))

        category_frame = ctk.CTkFrame(summary_frame, fg_color="#2d2d2d")
        category_frame.pack(pady=10, padx=105, fill="x")

        ctk.CTkLabel(
            category_frame,
            text="Category Totals",
            text_color="#fff",
            font=("Inter", 14, "bold")
        ).pack(anchor="w")

        for category, total in df.groupby('expense_type')['amount'].sum().items():
            ctk.CTkLabel(
                category_frame,
                text=f"{category}: ${total:,.2f}",
                text_color="#fff",
                font=("Inter", 12)
            ).pack(anchor="w", pady=2)

        stats_frame = ctk.CTkFrame(summary_frame, fg_color="#2d2d2d")
        stats_frame.pack(pady=10, padx=105, fill="x")

        ctk.CTkLabel(
            stats_frame,
            text="Statistics",
            text_color="#fff",
            font=("Inter", 14, "bold")
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            stats_frame,
            text=f"Highest Expense Day:\n{max_expense_date.strftime('%Y-%m-%d')}\n${daily_totals[max_expense_date]:,.2f}",
            text_color="#fff",
            font=("Inter", 12)
        ).pack(anchor="w", pady=5)

        ctk.CTkLabel(
            stats_frame,
            text=f"Lowest Expense Day:\n{min_expense_date.strftime('%Y-%m-%d')}\n${daily_totals[min_expense_date]:,.2f}",
            text_color="#fff",
            font=("Inter", 12)
        ).pack(anchor="w", pady=5)

    def export_chart(file_type="JPEG"):
        global fig
        file_path = filedialog.asksaveasfilename(defaultextension=file_type.lower(), filetypes=[(file_type, f"*.{file_type.lower()}")])
        if file_path:
            if file_type == "JPEG":
                fig.savefig(file_path, format="jpeg")
            elif file_type == "PDF":
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=16)
                pdf.cell(200, 10, txt="Expense Analysis", ln=True, align="C")
                temp_image_path = file_path.replace('.pdf', '.jpeg')
                fig.savefig(temp_image_path, format="jpeg")
                pdf.image(temp_image_path, x=10, y=30, w=180)
                pdf.output(file_path)
                import os
                os.remove(temp_image_path)

    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(4, weight=1)

    frame.configure(fg_color="#222222", bg_color="#222222")

    category_label = ctk.CTkLabel(frame, text="Category", text_color="#fff", font=("Arial", 12))
    category_label.grid(row=0, column=1, padx=10, pady=10)
    category_combobox = ctk.CTkComboBox(frame, values=["All", "Groceries", "Food & Dining", "Transportation", "Housing", "Education", "Utilities", "Shopping", "Health", "Entertainment", "Insurance" ,"Other", "Income"])
    category_combobox.grid(row=0, column=2, padx=10, pady=10)

    amount_label = ctk.CTkLabel(frame, text="Amount Range", text_color="#fff", font=("Arial", 12))
    amount_label.grid(row=1, column=1, padx=10, pady=10)
    min_amount_entry = ctk.CTkEntry(frame, placeholder_text="Min")
    min_amount_entry.grid(row=1, column=2, padx=5, pady=5)
    max_amount_entry = ctk.CTkEntry(frame, placeholder_text="Max")
    max_amount_entry.grid(row=1, column=3, padx=5, pady=5)

    date_label = ctk.CTkLabel(frame, text="Date Range", text_color="#fff", font=("Arial", 12))
    date_label.grid(row=2, column=1, padx=10, pady=10)
    start_date_entry = ctk.CTkEntry(frame, placeholder_text="Start Date (YYYY-MM-DD)")
    start_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
    start_date_entry.grid(row=2, column=2, padx=5, pady=5)
    end_date_entry = ctk.CTkEntry(frame, placeholder_text="End Date (YYYY-MM-DD)")
    end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
    end_date_entry.grid(row=2, column=3, padx=5, pady=5)

    apply_button = ctk.CTkButton(frame, text="Apply Filters", command=apply_filters_and_visualize, fg_color="#6600FF")
    apply_button.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    fig = apply_filters_and_visualize()
    pdf_button = ctk.CTkButton(frame, text="Export to PDF", command=lambda: export_chart("PDF"), fg_color="#009688")
    pdf_button.place(relx=0.4, rely=0.87)

    jpeg_button = ctk.CTkButton(frame, text="Export to JPEG", command=lambda: export_chart("JPEG"), fg_color="#3F51B5")
    jpeg_button.place(relx=0.5, rely=0.87)