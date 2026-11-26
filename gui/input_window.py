import tkinter as tk
import tests.test_validation as tests
from tkinter import ttk, messagebox

from data.subjects import SUBJECTS_DATA
from gui.validation import SUBJECTS, validate


HIGH_CHANCE_THRESHOLD = 0.75


def _prob_to_percent(value):
    return value * 100 if value <= 1.0 else value


def build_recommendations(session_params_list, session_probability):
    prob_percent = _prob_to_percent(session_probability)

    if prob_percent >= HIGH_CHANCE_THRESHOLD * 100:
        return []

    recommendations = []

    low_tickets = []
    many_missed = []
    little_hours = []
    debts = []
    low_luck = []

    for params in session_params_list:
        subject = params["subject"]

        learned = params["learned_tickets"]
        total = params["total_tickets"]
        ratio = learned / total if total else 0
        if ratio < 0.6:
            low_tickets.append(f"{subject} (выучено {learned} из {total})")

        if params["missed_lectures"] > 10:
            many_missed.append(f"{subject} (пропущено {params['missed_lectures']})")

        if params["hours_per_day"] < 2:
            little_hours.append(subject)

        if params["has_debts"]:
            debts.append(subject)

        if params["luck"] <= 3:
            low_luck.append(subject)

    if low_tickets:
        recommendations.append(
            "Подтяни билеты по предметам: " + ", ".join(low_tickets) +
            ". Постарайся выучить хотя бы 70-80% билетов."
        )

    if many_missed:
        recommendations.append(
            "Слишком много пропусков: " + ", ".join(many_missed) +
            ". Постарайся посещать оставшиеся занятия и переписать пропущенное."
        )

    if little_hours:
        recommendations.append(
            "Увеличь часы подготовки (сейчас меньше 2 ч/день) по: " +
            ", ".join(little_hours) +
            ". Даже 1-2 дополнительных часа в день дают заметный прирост."
        )

    if debts:
        recommendations.append(
            "Есть задолженности по: " + ", ".join(debts) +
            ". Закрой хвосты до сессии — они сильно снижают шансы."
        )

    if low_luck and len(low_luck) == len(session_params_list):
        recommendations.append(
            "Везучесть ниже средней по всем предметам. Стоит подстраховаться "
            "и выучить больше билетов."
        )

    if not recommendations:
        recommendations.append(
            "Шанс сдачи ниже желаемого. Попробуй увеличить часы подготовки "
            "и долю выученных билетов — это даёт наибольший эффект."
        )

    return recommendations


def format_recommendations(recommendations):
    if not recommendations:
        return ""
    lines = ["Рекомендации для повышения шансов:"]
    for rec in recommendations:
        lines.append("- " + rec)
    return "\n".join(lines)


# Функция, которая показывает результат и рекомендации в одном окне
def handle_input(params, recommendations_text=""):
    lines = []
    for key, value in params.items():
        lines.append(f"{key}: {value}")

    text = "\n".join(lines)
    if recommendations_text:
        text += "\n\n" + recommendations_text

    messagebox.showinfo("Данные приняты", text)


# Окно ввода параметров студента
# Проверяет введённые данные и передаёт их дальше
class InputWindow:

    # Создаёт окно и переменные для полей
    # on_submit - функция, которая получит проверенные данные
    def __init__(self, on_submit):
        self.on_submit = on_submit

        self.root = tk.Tk()
        self.root.title("Прогноз сдачи сессии")
        self.root.resizable(False, False)

        # Переменные связаны с полями окна и хранят введённые значения
        self.subject_var = tk.StringVar(value=SUBJECTS[0])
        self.has_debts_var = tk.BooleanVar(value=False)
        self.hours_var = tk.StringVar(value="3")
        self.missed_var = tk.StringVar(value="0")
        self.luck_var = tk.StringVar(value="5")
        self.total_var = tk.StringVar(value="25")
        self.learned_var = tk.StringVar(value="15")
        self.exam_type_var = tk.StringVar()

        self._build()

    # Размещает подписи, поля и кнопку в окне
    def _build(self):
        frame = ttk.Frame(self.root, padding=16)
        frame.grid()

        ttk.Label(frame, text="Предмет").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=4)
        subject_box = ttk.Combobox(frame, textvariable=self.subject_var, values=SUBJECTS,
                                   state="readonly", width=50)
        subject_box.grid(row=0, column=1, sticky="w")
        # При выборе предмета обновляем тип сдачи
        subject_box.bind("<<ComboboxSelected>>", self._on_subject_change)

        ttk.Label(frame, text="Тип сдачи").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Label(frame, textvariable=self.exam_type_var).grid(row=1, column=1, sticky="w")

        # Заполняем тип сдачи сразу при открытии окна
        self._on_subject_change()

        ttk.Label(frame, text="Есть хвосты").grid(row=2, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Checkbutton(frame, variable=self.has_debts_var).grid(row=2, column=1, sticky="w")

        ttk.Label(frame, text="Часы подготовки в день (0-12)").grid(row=3, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Spinbox(frame, textvariable=self.hours_var, from_=0, to=12,
                    increment=0.5, width=8).grid(row=3, column=1, sticky="w")

        ttk.Label(frame, text="Пропущено занятий (0-30)").grid(row=4, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Spinbox(frame, textvariable=self.missed_var, from_=0, to=30,
                    width=8).grid(row=4, column=1, sticky="w")

        ttk.Label(frame, text="Везучесть (1-10)").grid(row=5, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Spinbox(frame, textvariable=self.luck_var, from_=1, to=10,
                    width=8).grid(row=5, column=1, sticky="w")

        ttk.Label(frame, text="Всего билетов (10-50)").grid(row=6, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Spinbox(frame, textvariable=self.total_var, from_=10, to=50,
                    width=8).grid(row=6, column=1, sticky="w")

        ttk.Label(frame, text="Выучено билетов").grid(row=7, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Spinbox(frame, textvariable=self.learned_var, from_=0, to=50,
                    width=8).grid(row=7, column=1, sticky="w")

        ttk.Button(frame, text="Рассчитать", command=self._on_click).grid(
            row=8, column=0, columnspan=2, pady=(12, 0))

    # Показывает тип сдачи и сложность выбранного предмета
    # event - событие от списка, при ручном вызове не нужно
    def _on_subject_change(self, event=None):
        info = SUBJECTS_DATA[self.subject_var.get()]
        self.exam_type_var.set(f"{info['exam_type']} (сложность {info['rank']} из 5)")

    # Собирает данные из полей, проверяет их
    # При ошибках показывает сообщение, иначе передаёт данные в on_submit
    def _on_click(self):
        raw = {
            "subject": self.subject_var.get(),
            "has_debts": self.has_debts_var.get(),
            "hours_per_day": self.hours_var.get(),
            "missed_lectures": self.missed_var.get(),
            "luck": self.luck_var.get(),
            "total_tickets": self.total_var.get(),
            "learned_tickets": self.learned_var.get(),
        }

        tests.create_file(self)
        params, errors = validate(raw)

        if errors:
            messagebox.showerror("Проверьте ввод", "\n".join(errors))
            return

        session_params_list = [params]
        session_probability = 0.55

        recommendations = build_recommendations(session_params_list, session_probability)
        text = format_recommendations(recommendations)

        self.on_submit(params, text)

    # Открывает окно и ждёт действий пользователя
    def run(self):
        self.root.mainloop()


# Запуск окна для проверки
if __name__ == "__main__":
    window = InputWindow(on_submit=handle_input)
    window.run()
