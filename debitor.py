import tkinter as tk
from tkinter import ttk

def debitor_oynasi(root, font_style):
    window = tk.Toplevel(root)
    window.title("📤 Debitor qarzlari")
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

    tk.Label(scroll_frame, text="📤 Debitorlar bo‘limi", font=font_style, bg="#f8f9fa").pack(pady=10)

    # 1️⃣ Yangi debitor qo‘shish
    tk.Button(scroll_frame, text="➕ Yangi debitor qo‘shish", font=font_style, bg="yellow",
              command=lambda: yangi_debitor_formasi(scroll_frame, font_style)).pack(pady=5)

    # 2️⃣ Qarz berish
    tk.Button(scroll_frame, text="💳 Qarz berish", font=font_style, bg="yellow",
              command=lambda: qarz_berish_formasi(scroll_frame, font_style)).pack(pady=5)

    # 3️⃣ Qarz undirish
    tk.Button(scroll_frame, text="💸 Qarz undirish", font=font_style, bg="yellow",
              command=lambda: qarz_undirish_formasi(scroll_frame, font_style)).pack(pady=5)

    # 4️⃣ Debitorlar jadvali
    tk.Button(scroll_frame, text="📋 Debitorlar jadvali", font=font_style, bg="yellow",
              command=lambda: debitor_jadvali_oynasi(scroll_frame, font_style)).pack(pady=5)

    # 5️⃣ Qolgan haqlar jadvali
    tk.Button(scroll_frame, text="📊 Qolgan haqlar jadvali", font=font_style, bg="yellow",
              command=lambda: qolgan_haqlar_jadvali(scroll_frame, font_style)).pack(pady=5)

    # 6️⃣ Bosh menyu
    tk.Button(scroll_frame, text="⬅️ Bosh menyu", font=font_style, bg="red",
              command=window.destroy).pack(pady=20)


# 🔹 Yangi debitor qo‘shish formasi
def yangi_debitor_formasi(parent, font_style):
    form = tk.Toplevel(parent)
    form.title("➕ Yangi debitor qo‘shish")
    form.geometry("600x400")
    form.configure(bg="#f8f9fa")

    tk.Label(form, text="Yangi debitor qo‘shish", font=font_style, bg="#f8f9fa").pack(pady=10)

    name_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Nomi:", font=font_style, bg="#f8f9fa").pack()
    name_entry.pack()

    phone_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Telefon raqami:", font=font_style, bg="#f8f9fa").pack()
    phone_entry.pack()

    note_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Izoh:", font=font_style, bg="#f8f9fa").pack()
    note_entry.pack()

    status_label = tk.Label(form, text="", font=font_style, bg="#f8f9fa")
    status_label.pack()

    from models import add_kreditor  # Fayl boshida import qilishni unutmang

    def submit_debitor():
        try:
            name = name_entry.get()
            phone = phone_entry.get()
            note = note_entry.get() or None

            if not name.strip():
                status_label.config(text="❌ Ism kiritilmadi", fg="red")
                return

            add_kreditor(name, phone, note)
            status_label.config(text="✅ Qo‘shildi!", fg="green")
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            note_entry.delete(0, tk.END)
        except Exception as e:
            status_label.config(text=f"Xatolik: {e}", fg="red")


    tk.Button(form, text="Qo‘shish", command=submit_debitor, font=font_style, bg="green").pack(pady=10)
    tk.Button(form, text="⬅️ Orqaga", command=form.destroy, font=font_style, bg="red").pack()
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from models import get_kreditor_list, add_debitor_debt  # personlar bir xil jadvalda

def qarz_berish_formasi(parent, font_style):
    form = tk.Toplevel(parent)
    form.title("💳 Qarz berish")
    form.geometry("600x500")
    form.configure(bg="#f8f9fa")

    tk.Label(form, text="💳 Qarz berish formasi", font=font_style, bg="#f8f9fa").pack(pady=10)

    # Sana
    date_entry = tk.Entry(form, font=font_style)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
    tk.Label(form, text="Sana:", font=font_style, bg="#f8f9fa").pack()
    date_entry.pack()

    # Kimga (Combobox)
    debitorlar = get_kreditor_list()  # person jadvali umumiy
    options = [f"{p[1]} (ID:{p[0]})" for p in debitorlar]
    debitor_combo = ttk.Combobox(form, values=options, font=font_style, state="readonly")
    tk.Label(form, text="Kimga:", font=font_style, bg="#f8f9fa").pack()
    debitor_combo.pack()

    # Summa
    amount_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Summa:", font=font_style, bg="#f8f9fa").pack()
    amount_entry.pack()

    # Qaytarish muddati (optional)
    due_date_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Qaytarish muddati (ixtiyoriy):", font=font_style, bg="#f8f9fa").pack()
    due_date_entry.pack()

    # Izoh
    note_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Izoh:", font=font_style, bg="#f8f9fa").pack()
    note_entry.pack()

    # Status xabari
    status_label = tk.Label(form, text="", font=font_style, bg="#f8f9fa")
    status_label.pack()

    def submit_debt():
        try:
            selected = debitor_combo.get()
            if not selected:
                status_label.config(text="❌ Debitor tanlanmadi", fg="red")
                return
            person_id = int(selected.split("ID:")[1].replace(")", ""))
            date = date_entry.get()
            amount = float(amount_entry.get())
            due_date = due_date_entry.get() or None
            note = note_entry.get() or None

            add_debitor_debt(person_id, amount, date, due_date, note)
            status_label.config(text="✅ Qarz berildi!", fg="green")
            amount_entry.delete(0, tk.END)
            note_entry.delete(0, tk.END)
        except Exception as e:
            status_label.config(text=f"Xatolik: {e}", fg="red")

    tk.Button(form, text="Qarz berish", command=submit_debt, font=font_style, bg="green").pack(pady=10)
    tk.Button(form, text="⬅️ Orqaga", command=form.destroy, font=font_style, bg="red").pack()
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from models import get_kreditor_list, add_debitor_payment  # person jadvali umumiy

def qarz_undirish_formasi(parent, font_style):
    form = tk.Toplevel(parent)
    form.title("💸 Qarz undirish")
    form.geometry("600x500")
    form.configure(bg="#f8f9fa")

    tk.Label(form, text="💸 Qarz undirish formasi", font=font_style, bg="#f8f9fa").pack(pady=10)

    # Sana
    date_entry = tk.Entry(form, font=font_style)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
    tk.Label(form, text="Sana:", font=font_style, bg="#f8f9fa").pack()
    date_entry.pack()

    # Kimdan (Combobox)
    debitorlar = get_kreditor_list()  # person jadvali umumiy
    options = [f"{p[1]} (ID:{p[0]})" for p in debitorlar]
    debitor_combo = ttk.Combobox(form, values=options, font=font_style, state="readonly")
    tk.Label(form, text="Kimdan:", font=font_style, bg="#f8f9fa").pack()
    debitor_combo.pack()

    # Summa
    amount_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Undirilgan summa:", font=font_style, bg="#f8f9fa").pack()
    amount_entry.pack()

    # Izoh
    note_entry = tk.Entry(form, font=font_style)
    tk.Label(form, text="Izoh:", font=font_style, bg="#f8f9fa").pack()
    note_entry.pack()

    # Status xabari
    status_label = tk.Label(form, text="", font=font_style, bg="#f8f9fa")
    status_label.pack()

    def submit_payment():
        try:
            selected = debitor_combo.get()
            if not selected:
                status_label.config(text="❌ Debitor tanlanmadi", fg="red")
                return
            person_id = int(selected.split("ID:")[1].replace(")", ""))
            date = date_entry.get()
            amount = float(amount_entry.get())
            note = note_entry.get() or None

            add_debitor_payment(person_id, amount, date, note)
            status_label.config(text="✅ Qarz undirildi!", fg="green")
            amount_entry.delete(0, tk.END)
            note_entry.delete(0, tk.END)
        except Exception as e:
            status_label.config(text=f"Xatolik: {e}", fg="red")

    tk.Button(form, text="Qarz undirish", command=submit_payment, font=font_style, bg="green").pack(pady=10)
    tk.Button(form, text="⬅️ Orqaga", command=form.destroy, font=font_style, bg="red").pack()
import tkinter as tk
from models import get_debitor_transactions

def debitor_jadvali_oynasi(parent, font_style):
    jadval = tk.Toplevel(parent)
    jadval.title("📋 Debitorlar jadvali")
    jadval.geometry("900x600")
    jadval.configure(bg="#f8f9fa")

    tk.Label(jadval, text="📋 Debitorlar harakati", font=font_style, bg="#f8f9fa").pack(pady=10)

    canvas = tk.Canvas(jadval, bg="#f8f9fa")
    scrollbar = tk.Scrollbar(jadval, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="#f8f9fa")

    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Jadval sarlavhalari
    header = tk.Frame(scroll_frame, bg="#f8f9fa")
    header.pack(fill="x", padx=10)
    for i, title in enumerate(["Sana", "Kimga/Kimdan", "Summa", "Izoh", "Muddat", "Tahrirlash"]):
        tk.Label(header, text=title, font=font_style, bg="#f8f9fa", width=15).grid(row=0, column=i)

    # Ma’lumotlar
    transactions = get_debitor_transactions()
    for i, tx in enumerate(transactions):
        date, person, amount, note, due_date, tx_type, tx_id = tx
        row = tk.Frame(scroll_frame, bg="#f8f9fa")
        row.pack(fill="x", padx=10, pady=2)

        tk.Label(row, text=date, font=font_style, bg="#f8f9fa", width=15).grid(row=0, column=0)
        tk.Label(row, text=person, font=font_style, bg="#f8f9fa", width=15).grid(row=0, column=1)
        tk.Label(row, text=f"{amount} so‘m", font=font_style, bg="#f8f9fa", width=15).grid(row=0, column=2)
        tk.Label(row, text=note or "—", font=font_style, bg="#f8f9fa", width=15).grid(row=0, column=3)
        tk.Label(row, text=due_date or "—", font=font_style, bg="#f8f9fa", width=15).grid(row=0, column=4)

        tk.Button(row, text="✏️ Tahrirlash", font=("Arial", 14, "bold"), bg="red",
                  command=lambda tx_id=tx_id, tx_type=tx_type: print(f"Tahrirlash: {tx_type} ID={tx_id}")
        ).grid(row=0, column=5)

    # Orqaga tugmasi
    tk.Button(jadval, text="⬅️ Orqaga", command=jadval.destroy, font=font_style, bg="red").pack(pady=20)
import tkinter as tk
from models import get_debitor_balances

def qolgan_haqlar_jadvali(parent, font_style):
    window = tk.Toplevel(parent)
    window.title("📊 Qolgan haqlar jadvali")
    window.geometry("800x600")
    window.configure(bg="#f8f9fa")

    tk.Label(window, text="📊 Qolgan haqlar jadvali", font=font_style, bg="#f8f9fa").pack(pady=10)

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
    for i, title in enumerate(["Debitor", "Berilgan qarz", "Undirilgan", "Qolgan haqlar"]):
        tk.Label(header, text=title, font=font_style, bg="#f8f9fa", width=20).grid(row=0, column=i)

    # Ma’lumotlar
    balances = get_debitor_balances()
    for i, row in enumerate(balances):
        name, total_debt, total_paid, remaining = row
        line = tk.Frame(scroll_frame, bg="#f8f9fa")
        line.pack(fill="x", padx=10, pady=2)

        tk.Label(line, text=name, font=font_style, bg="#f8f9fa", width=20).grid(row=0, column=0)
        tk.Label(line, text=f"{total_debt} so‘m", font=font_style, bg="#f8f9fa", width=20).grid(row=0, column=1)
        tk.Label(line, text=f"{total_paid} so‘m", font=font_style, bg="#f8f9fa", width=20).grid(row=0, column=2)
        tk.Label(line, text=f"{remaining} so‘m", font=font_style, bg="#f8f9fa", width=20).grid(row=0, column=3)

    # Orqaga tugmasi
    tk.Button(window, text="⬅️ Orqaga", command=window.destroy, font=font_style, bg="red").pack(pady=20)
