import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from models import add_expense, get_expense_by_date

def xarajat_oynasi(root, font_style):
    window = tk.Toplevel(root)
    window.title("💸 Xarajatlar")
    window.geometry("800x600")
    window.configure(bg="#f8f9fa")

    canvas = tk.Canvas(window, bg="#f8f9fa")
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f8f9fa")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    tk.Label(scroll_frame, text="💸 Xarajatlar bo‘limi", font=font_style, bg="#f8f9fa").pack(pady=10)

    tk.Button(scroll_frame, text="➕ Xarajat qo‘shish", font=font_style, bg="yellow",
              command=lambda: xarajat_qoshish_formasi(scroll_frame, font_style)).pack(pady=5)

    tk.Button(scroll_frame, text="📋 Xarajatlar jadvali", font=font_style, bg="yellow",
              command=lambda: xarajat_jadvali_oynasi(scroll_frame, font_style)).pack(pady=5)

    tk.Button(scroll_frame, text="⬅️ Bosh menyu", font=font_style, bg="red",
              command=window.destroy).pack(pady=20)

def xarajat_qoshish_formasi(parent, font_style):
    form = tk.Toplevel(parent)
    form.title("➕ Xarajat qo‘shish")
    form.geometry("600x400")
    form.configure(bg="#f8f9fa")

    tk.Label(form, text="Xarajat qo‘shish", font=font_style, bg="#f8f9fa").pack(pady=10)

    date_entry = tk.Entry(form, font=font_style)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
    tk.Label(form, text="Sana:", font=font_style, bg="#f8f9fa").pack()
    date_entry.pack()

    amount_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Summa:", font=font_style, bg="#f8f9fa").pack()
    amount_entry.pack()

    categories = [
        "kommunal", "ijara", "kontrakt", "oziq_ovqat",
        "aloqa", "internet_tv", "jamgarma", "boshqalar", "qarz_tolash"
    ]
    category_combo = ttk.Combobox(form, values=categories, font=font_style, state="readonly")
    tk.Label(form, text="Kategoriya:", font=font_style, bg="#f8f9fa").pack()
    category_combo.pack()

    note_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Izoh:", font=font_style, bg="#f8f9fa").pack()
    note_entry.pack()

    status_label = tk.Label(form, text="", font=font_style, bg="#f8f9fa")
    status_label.pack()

    def submit_expense():
        try:
            date = date_entry.get()
            amount = float(amount_entry.get())
            category = category_combo.get()
            note = note_entry.get() or None

            add_expense(date, amount, category, note)
            status_label.config(text="✅ Qo‘shildi!", fg="green")

            amount_entry.delete(0, tk.END)
            note_entry.delete(0, tk.END)
            category_combo.set("")
        except Exception as e:
            status_label.config(text=f"Xatolik: {e}", fg="red")

    tk.Button(form, text="Qo‘shish", command=submit_expense, font=font_style, bg="green").pack(pady=10)
    tk.Button(form, text="⬅️ Orqaga", command=form.destroy, font=font_style, bg="red").pack()

def xarajat_jadvali_oynasi(parent, font_style):
    jadval = tk.Toplevel(parent)
    jadval.title("📋 Xarajatlar jadvali")
    jadval.geometry("800x500")
    jadval.configure(bg="#f8f9fa")

    tk.Label(jadval, text="📋 Xarajatlar", font=font_style, bg="#f8f9fa").pack(pady=10)

    today = datetime.today().strftime("%Y-%m-%d")
    week_ago = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")
    records = get_expense_by_date(week_ago, today)

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
