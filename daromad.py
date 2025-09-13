import tkinter as tk
from tkinter import ttk
from datetime import datetime

def daromad_oynasi(root, font_style):
    daromad_window = tk.Toplevel(root)
    daromad_window.title("💰 Daromadlar")
    daromad_window.geometry("800x600")
    daromad_window.configure(bg="#f8f9fa")

    canvas = tk.Canvas(daromad_window, bg="#f8f9fa")
    scrollbar = tk.Scrollbar(daromad_window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f8f9fa")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scroll_frame, text="💰 Daromadlar bo‘limi", font=font_style, bg="#f8f9fa").pack(pady=10)

    # 1️⃣ Daromad qo‘shish tugmasi
    tk.Button(scroll_frame, text="➕ Daromad qo‘shish", font=font_style, bg="yellow",
              command=lambda: daromad_qoshish_formasi(scroll_frame, font_style)).pack(pady=5)

    # 2️⃣ Daromadlar jadvali tugmasi
    tk.Button(scroll_frame, text="📋 Daromadlar jadvali", font=font_style, bg="yellow",
              command=lambda: daromad_jadvali_oynasi(scroll_frame, font_style)).pack(pady=5)

    # 3️⃣ Bosh menyuga qaytish
    tk.Button(scroll_frame, text="⬅️ Bosh menyu", font=font_style, bg="red",
              command=daromad_window.destroy).pack(pady=20)

# 🔹 Daromad qo‘shish formasi
def daromad_qoshish_formasi(parent, font_style):
    form = tk.Toplevel(parent)
    form.title("➕ Daromad qo‘shish")
    form.geometry("600x400")
    form.configure(bg="#f8f9fa")

    tk.Label(form, text="Daromad qo‘shish", font=font_style, bg="#f8f9fa").pack(pady=10)

    date_entry = tk.Entry(form, font=font_style)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
    tk.Label(form, text="Sana:", font=font_style, bg="#f8f9fa").pack()
    date_entry.pack()

    amount_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Summa:", font=font_style, bg="#f8f9fa").pack()
    amount_entry.pack()

    categories = ["oylik", "avans", "premya", "moddiy_yordam", "qo'shimcha_ishhaqqi", "dividendi", "boshqalar", "arz_olish"]
    category_combo = ttk.Combobox(form, values=categories, font=font_style, state="readonly")
    tk.Label(form, text="Kategoriya:", font=font_style, bg="#f8f9fa").pack()
    category_combo.pack()

    note_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Izoh:", font=font_style, bg="#f8f9fa").pack()
    note_entry.pack()

    status_label = tk.Label(form, text="", font=font_style, bg="#f8f9fa")
    status_label.pack()
    from models import add_income
    def submit_income():
        try:
            date = date_entry.get()
            amount = float(amount_entry.get())
            category = category_combo.get()
            note = note_entry.get() or None

            add_income(date, amount, category, note)  # ✅ Bazaga yozish
            status_label.config(text="✅ Qo‘shildi!", fg="green")

            amount_entry.delete(0, tk.END)
            note_entry.delete(0, tk.END)
            category_combo.set("")
        except Exception as e:
            status_label.config(text=f"Xatolik: {e}", fg="red")
    tk.Button(form, text="Qo‘shish", command=submit_income, font=font_style, bg="green").pack(pady=10)
    tk.Button(form, text="⬅️ Orqaga", command=form.destroy, font=font_style, bg="red").pack()

# 🔹 Daromadlar jadvali oynasi
from models import get_income_by_date
from datetime import datetime, timedelta

def daromad_jadvali_oynasi(parent, font_style):
    jadval = tk.Toplevel(parent)
    jadval.title("📋 Daromadlar jadvali")
    jadval.geometry("800x500")
    jadval.configure(bg="#f8f9fa")

    tk.Label(jadval, text="📋 Daromadlar", font=font_style, bg="#f8f9fa").pack(pady=10)

    # Ma’lumotlarni olish
    today = datetime.today().strftime("%Y-%m-%d")
    week_ago = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    records = get_income_by_date(week_ago, today)

    for rec in records:
        date, amount, category, note = rec[1], rec[2], rec[3], rec[4]
        row = tk.Frame(jadval, bg="#f8f9fa")
        row.pack(fill="x", padx=20, pady=2)

        tk.Label(row, text=date, font=font_style, bg="#f8f9fa", width=12).pack(side="left")
        tk.Label(row, text=f"{amount} so‘m", font=font_style, bg="#f8f9fa", width=12).pack(side="left")
        tk.Label(row, text=category, font=font_style, bg="#f8f9fa", width=15).pack(side="left")
        tk.Label(row, text=note or "—", font=font_style, bg="#f8f9fa", width=20).pack(side="left")
        tk.Button(row, text="✏️", font=("Arial", 14, "bold"), bg="red").pack(side="right")

    tk.Button(jadval, text="⬅️ Orqaga", command=jadval.destroy, font=font_style, bg="red").pack(pady=20)
