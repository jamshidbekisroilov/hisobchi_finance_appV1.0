import tkinter as tk
from tkinter import ttk
def muallif_oynasi(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("👤 Muallif")
    window.geometry("600x400")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="👤 Dastur muallifi", font=font_style, bg="#f8f9fa").pack(pady=10)

    info = (
        "Ism: Jamshidbek Isroilov\n"
        "Hudud: Andijon viloyati, O‘zbekiston\n"
        "Mutaxassislik: Python GUI, Tkinter, ma’lumotlar tahlili\n"
        "Django, Flask, SQL, Desktop ilovalar, Web saytar,Telegram bot \n"
        "Loyiha: Oddiy foydalanuvchilar uchun moliyaviy boshqaruv ilovasi\n"
        "Maqsad: Tushunarli, chiroyli, va ishonchli ilova yaratish\n"
        "Aloqa:t.me/jamshidbekisroilov2000\n"
        "GitHub: https://github.com/jamshidbekisroilov\n"
        "LinkedIn: https://www.linkedin.com/in/jamshidbek-isroilov-accountant\n"
        "Telegram: https://t.me/jamshidbekisroilov2000\n"
        "Email:jisroilov45@gamil.com\n"
        "Website: https://portfolio-site-cals.onrender.com"
    )

    tk.Label(window, text=info, font=font_style, bg="#f8f9fa", justify="left").pack(pady=10)

    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=20)
