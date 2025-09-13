import tkinter as tk
from tkinter import ttk
def tahlil_oynasi(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("📊 Tahlillar")
    window.geometry("800x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="📊 Tahlil bo‘limi", font=font_style, bg="#f8f9fa").pack(pady=10)

    tk.Button(window, text="📈 Debitor vs Kreditor grafikasi", font=font_style, bg="lightgreen",
              command=lambda: grafik_debitor_kreditor(window, font_style)).pack(pady=5)

    tk.Button(window, text="📊 Daromad vs Xarajat balansi", font=font_style, bg="lightyellow",
              command=lambda: grafik_daromad_xarajat(window, font_style)).pack(pady=5)

    tk.Button(window, text="📋 Faol kontragentlar", font=font_style, bg="lightgray",
              command=lambda: jadval_faol_kontragentlar(window, font_style)).pack(pady=5)

    tk.Button(window, text="🥧 Xarajat kategoriyalari", font=font_style, bg="orange",
              command=lambda: grafik_xarajat_kategoriyalari(window, font_style)).pack(pady=5)

    tk.Button(window, text="💰 Jamg‘arma salohiyati", font=font_style, bg="lightblue",
              command=lambda: grafik_jamgarma(window, font_style)).pack(pady=5)

    tk.Button(window, text="⬅️ Bosh menyu", font=font_style, bg="red",
              command=window.destroy).pack(pady=20)
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import get_daily_debitor_kreditor_balances

def grafik_debitor_kreditor(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("📈 Debitor vs Kreditor grafikasi")
    window.geometry("900x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="📈 Debitor vs Kreditor qoldiqlari", font=font_style, bg="#f8f9fa").pack(pady=10)

    # Ma’lumotlarni olish
    dates, debitor_values, kreditor_values = get_daily_debitor_kreditor_balances()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(dates, debitor_values, label="Debitorlar (Yashil)", color="green", linewidth=2)
    ax.plot(dates, kreditor_values, label="Kreditorlar (Qizil)", color="red", linewidth=2)
    ax.set_xlabel("Sana")
    ax.set_ylabel("Summa (so‘m)")
    ax.set_title("Debitor vs Kreditor qoldiqlari")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Koeffitsiyent va xulosa
    try:
        ratio = round(debitor_values[-1] / kreditor_values[-1], 2)
    except ZeroDivisionError:
        ratio = float('inf')

    if ratio < 0.5:
        xulosa = "❌ Qoniqarsiz: jiddiy qarz xavfi ostida"
    elif ratio < 0.86:
        xulosa = "⚠️ Qoniqarli: biroz qarz xavfi bor"
    elif ratio < 1.3:
        xulosa = "✅ Yaxshi: xavf ostida emas"
    else:
        xulosa = "🌟 A’lo: moliyaviy holat barqaror"

    tk.Label(window, text=f"Koeffitsiyent: {ratio}", font=font_style, bg="#f8f9fa", fg="blue").pack(pady=5)
    tk.Label(window, text=f"Xulosa: {xulosa}", font=font_style, bg="#f8f9fa").pack(pady=5)

    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=10)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import get_monthly_income_expense

def grafik_daromad_xarajat(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("📊 Daromad vs Xarajat balansi")
    window.geometry("900x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="📊 Daromad vs Xarajat balansi", font=font_style, bg="#f8f9fa").pack(pady=10)

    months, income_values, expense_values = get_monthly_income_expense()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(months, income_values, label="Daromad", color="green")
    ax.bar(months, expense_values, label="Xarajat", color="red", alpha=0.6)
    ax.set_xlabel("Oy")
    ax.set_ylabel("Summa (so‘m)")
    ax.set_title("Daromad va Xarajatlar solishtiruvchisi")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Oxirgi oy koeffitsiyenti
    try:
        ratio = round(income_values[-1] / expense_values[-1], 2)
    except ZeroDivisionError:
        ratio = float('inf')

    if ratio < 0.9:
        xulosa = "❌ Ogohlantirish: xarajatlar daromaddan ko‘p"
    elif ratio < 1.1:
        xulosa = "⚖️ Balansda: daromad va xarajat teng"
    else:
        xulosa = "✅ Jamg‘arma imkoniyati bor"

    tk.Label(window, text=f"Koeffitsiyent: {ratio}", font=font_style, bg="#f8f9fa", fg="blue").pack(pady=5)
    tk.Label(window, text=f"Xulosa: {xulosa}", font=font_style, bg="#f8f9fa").pack(pady=5)

    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=10)
import tkinter as tk
from models import get_active_persons_summary

def jadval_faol_kontragentlar(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("📋 Faol kontragentlar")
    window.geometry("800x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="📋 Oxirgi 30 kunda faol kontragentlar", font=font_style, bg="#f8f9fa").pack(pady=10)

    canvas = tk.Canvas(window, bg="#f8f9fa")
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f8f9fa")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Sarlavhalar
    header = tk.Frame(scroll_frame, bg="#f8f9fa")
    header.pack(fill="x", padx=10)
    for i, title in enumerate(["Ism", "Harakatlar soni", "Umumiy summa"]):
        tk.Label(header, text=title, font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=i)

    # Ma’lumotlar
    summary = get_active_persons_summary()
    for i, (name, (count, total)) in enumerate(summary):
        row = tk.Frame(scroll_frame, bg="#f8f9fa")
        row.pack(fill="x", padx=10, pady=2)

        tk.Label(row, text=name, font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=0)
        tk.Label(row, text=str(count), font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=1)
        tk.Label(row, text=f"{total} so‘m", font=font_style, bg="#f8f9fa", width=25).grid(row=0, column=2)

    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=20)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import get_expense_by_category

def grafik_xarajat_kategoriyalari(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("🥧 Xarajat kategoriyalari")
    window.geometry("900x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="🥧 Xarajatlar kategoriyalari bo‘yicha", font=font_style, bg="#f8f9fa").pack(pady=10)

    data = get_expense_by_category()
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.set_title("Xarajatlar taqsimoti")
    ax.axis('equal')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Xulosa: eng katta kategoriya
    if categories:
        eng_katta = categories[0]
        tk.Label(window, text=f"Eng ko‘p xarajat: {eng_katta}", font=font_style, bg="#f8f9fa", fg="blue").pack(pady=5)
    else:
        tk.Label(window, text="Ma’lumot topilmadi", font=font_style, bg="#f8f9fa", fg="red").pack(pady=5)

    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=10)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from models import get_monthly_savings

def grafik_jamgarma(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("💰 Jamg‘arma salohiyati")
    window.geometry("900x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="💰 Oy bo‘yicha jamg‘arma salohiyati", font=font_style, bg="#f8f9fa").pack(pady=10)

    months, savings = get_monthly_savings()

    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ["green" if s >= 0 else "red" for s in savings]
    ax.bar(months, savings, color=colors)
    ax.set_xlabel("Oy")
    ax.set_ylabel("Jamg‘arma (so‘m)")
    ax.set_title("Daromad - Xarajat - To‘lovlar")
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Oxirgi oy xulosasi
    last_saving = savings[-1]
    if last_saving < 0:
        xulosa = "❌ Salbiy jamg‘arma: xarajatlar va to‘lovlar daromaddan ko‘p"
    elif last_saving == 0:
        xulosa = "⚖️ Balansda: jamg‘arma yo‘q, lekin minusga tushmagan"
    else:
        xulosa = "✅ Ijobiy jamg‘arma: pul ortyapti"

    tk.Label(window, text=f"Oxirgi oy jamg‘arma: {last_saving} so‘m", font=font_style, bg="#f8f9fa", fg="blue").pack(pady=5)
    tk.Label(window, text=f"Xulosa: {xulosa}", font=font_style, bg="#f8f9fa").pack(pady=5)

    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=10)
