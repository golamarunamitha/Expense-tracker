import customtkinter as ctk

from loginpage import first_page

app = ctk.CTk()
ctk.set_default_color_theme("green")
app.geometry("3200x2000")
app._fg_color = "#F5F5F5"

first_page(app)

app.mainloop()