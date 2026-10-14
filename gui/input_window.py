import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Прогноз сдачи сессии")

frame = ttk.Frame(root, padding=16)
frame.grid()

hours_var = tk.StringVar(value="3")

ttk.Label(frame, text="Часы подготовки в день").grid(row=0, column=0, sticky="w", padx=(0, 12))
ttk.Entry(frame, textvariable=hours_var, width=10).grid(row=0, column=1)


def on_click():
    print("Введено:", hours_var.get())


ttk.Button(frame, text="Рассчитать", command=on_click).grid(row=1, column=0, columnspan=2, pady=(12, 0))

root.mainloop()