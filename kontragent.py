import tkinter as tk
from tkinter import ttk
import tkinter as tk
from models import get_all_persons

def kontragentlar_jadvali_oynasi(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("📇 Kontragentlar jadvali")
    window.geometry("800x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="📇 Barcha kontragentlar", font=font_style, bg="#f8f9fa").pack(pady=10)

    canvas = tk.Canvas(window, bg="#f8f9fa")
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f8f9fa")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Jadval sarlavhalari
    header = tk.Frame(scroll_frame, bg="#f8f9fa")
    header.pack(fill="x", padx=10)
    for i, title in enumerate(["Nomi", "Telefon", "Izoh"]):
        tk.Label(header, text=title, font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=i)

    # Ma’lumotlar
    persons = get_all_persons()
    for i, person in enumerate(persons):
        name, phone, note = person
        row = tk.Frame(scroll_frame, bg="#f8f9fa")
        row.pack(fill="x", padx=10, pady=2)

        tk.Label(row, text=name, font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=0)
        tk.Label(row, text=phone or "—", font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=1)
        tk.Label(row, text=note or "—", font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=2)

    # Orqaga tugmasi
    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=20)
