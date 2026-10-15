import tkinter as tk
from tkinter import ttk, messagebox

from gui.validation import SUBJECTS, EXAM_FORMS, validate

root = tk.Tk()
root.title("Прогноз сдачи сессии")
root.resizable(False, False)

frame = ttk.Frame(root, padding=16)
frame.grid()

subject_var = tk.StringVar(value=SUBJECTS[0])
exam_form_var = tk.StringVar(value=EXAM_FORMS[0])
has_debts_var = tk.BooleanVar(value=False)
hours_var = tk.StringVar(value="3")
missed_var = tk.StringVar(value="0")
luck_var = tk.StringVar(value="5")
total_var = tk.StringVar(value="25")
learned_var = tk.StringVar(value="15")

ttk.Label(frame, text="Предмет").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Combobox(frame, textvariable=subject_var, values=SUBJECTS,
             state="readonly", width=15).grid(row=0, column=1, sticky="w")

ttk.Label(frame, text="Форма экзамена").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Combobox(frame, textvariable=exam_form_var, values=EXAM_FORMS,
             state="readonly", width=15).grid(row=1, column=1, sticky="w")

ttk.Label(frame, text="Есть хвосты").grid(row=2, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Checkbutton(frame, variable=has_debts_var).grid(row=2, column=1, sticky="w")

ttk.Label(frame, text="Часы подготовки в день (0–12)").grid(row=3, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Spinbox(frame, textvariable=hours_var, from_=0, to=12,
            increment=0.5, width=8).grid(row=3, column=1, sticky="w")

ttk.Label(frame, text="Пропущено занятий (0–30)").grid(row=4, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Spinbox(frame, textvariable=missed_var, from_=0, to=30,
            width=8).grid(row=4, column=1, sticky="w")

ttk.Label(frame, text="Везучесть (1–10)").grid(row=5, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Spinbox(frame, textvariable=luck_var, from_=1, to=10,
            width=8).grid(row=5, column=1, sticky="w")

ttk.Label(frame, text="Всего билетов (10–50)").grid(row=6, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Spinbox(frame, textvariable=total_var, from_=10, to=50,
            width=8).grid(row=6, column=1, sticky="w")

ttk.Label(frame, text="Выучено билетов").grid(row=7, column=0, sticky="w", padx=(0, 12), pady=4)
ttk.Spinbox(frame, textvariable=learned_var, from_=0, to=50,
            width=8).grid(row=7, column=1, sticky="w")


def on_click():
    raw = {
        "subject": subject_var.get(),
        "exam_form": exam_form_var.get(),
        "has_debts": has_debts_var.get(),
        "hours_per_day": hours_var.get(),
        "missed_lectures": missed_var.get(),
        "luck": luck_var.get(),
        "total_tickets": total_var.get(),
        "learned_tickets": learned_var.get(),
    }

    params, errors = validate(raw)

    if errors:
        messagebox.showerror("Проверьте ввод", "\n".join(errors))
        return

    print(params)


ttk.Button(frame, text="Рассчитать", command=on_click).grid(row=8, column=0, columnspan=2, pady=(12, 0))

root.mainloop()