import tkinter as tk
from daromad import daromad_oynasi
from xarajat import xarajat_oynasi
from kreditor import kreditor_oynasi
from debitor import debitor_oynasi
from kontragent import kontragentlar_jadvali_oynasi
from muallif import muallif_oynasi
from tahlil import tahlil_oynasi
from db import init_db

init_db()

def main_menu():
    root = tk.Tk()
    root.title("Hisobchi Dasturi")
    root.state("zoomed")
    root.configure(bg="#f8f9fa")
    font_style = ("Arial", 16, "bold")

    tk.Label(root, text="📊 Bosh menyu", font=font_style, bg="#f8f9fa").pack(pady=20)

    tk.Button(root, text="💰 Daromadlar", command=lambda: daromad_oynasi(root, font_style), font=font_style, bg="yellow").pack(pady=10)
    tk.Button(root, text="💸 Xarajatlar", command=lambda: xarajat_oynasi(root, font_style), font=font_style, bg="yellow").pack(pady=10)
    tk.Button(root, text="📥 Kreditor qarzlari", command=lambda: kreditor_oynasi(root, font_style), font=font_style, bg="yellow").pack(pady=10)
    tk.Button(root, text="📤 Debitor qarzlari", command=lambda: debitor_oynasi(root, font_style), font=font_style, bg="yellow").pack(pady=10)
    tk.Button(root, text="📇 Kontragentlar jadvali", command=lambda: kontragentlar_jadvali_oynasi(root, font_style), font=font_style, bg="yellow").pack(pady=10)
    tk.Button(root, text="📊 Tahlillar", command=lambda: tahlil_oynasi(root,font_style),font=font_style, bg="lightblue").pack(pady=10)
    tk.Button(root, text="👤 Muallif", command=lambda: muallif_oynasi(root,font_style),font=font_style, bg="lightgray").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
