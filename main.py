import tkinter as tk
from tkinter import messagebox

def on_button_click():
    testo = entry.get()
    messagebox.showinfo("Messaggio", f"Hai scritto: {testo}")

finestra = tk.Tk()
finestra.title("QR generator")
finestra.geometry("300x150")

entry = tk.Entry(finestra, width=30)
entry.pack(pady=20)

bottone = tk.Button(finestra, text="Genera", command=on_button_click)
bottone.pack()

finestra.mainloop()
