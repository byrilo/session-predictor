import tkinter as tk
from tkinter import ttk, messagebox

from data.subjects import SUBJECTS, SUBJECTS_DATA
from gui.validation import validate

from simulation.monte_carlo_session import calculate_session_probability

HIGH_CHANCE_THRESHOLD = 0.75

# Значения полей по умолчанию (подставляются при открытии и после добавления экзамена)
DEFAULTS = {
    "has_debts": False,
    "hours": "3",
    "missed": "0",
    "luck": "5",
    "total": "25",
    "learned": "15",
}


def _prob_to_percent(value):
    return value * 100 if value <= 1.0 else value


# Считает вероятность сдачи сессии по списку параметров всех добавленных экзаменов
# Вынесено в отдельную функцию, чтобы при смене сигнатуры
# calculate_session_probability правка была в одном месте
def calculate_probability(session_params_list):
    print(session_params_list)
    return calculate_session_probability(session_params_list)


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
# session_params_list - список параметров по каждому экзамену
# session_probability - вероятность сдачи всей сессии
# recommendations_text - готовый текст рекомендаций (может быть пустым)
def handle_input(session_params_list, session_probability, recommendations_text=""):
    lines = [f"Вероятность сдачи сессии: {_prob_to_percent(session_probability):.1f}%", ""]

    for p in session_params_list:
        debts = "да" if p["has_debts"] else "нет"
        lines.append(
            f"{p['subject']} ({p['exam_type']}, сложность {p['subject_rank']}): "
            f"билеты {p['learned_tickets']}/{p['total_tickets']}, "
            f"{p['hours_per_day']} ч/день, пропусков {p['missed_lectures']}, "
            f"везучесть {p['luck']}, хвосты: {debts}"
        )

    text = "\n".join(lines)
    if recommendations_text:
        text += "\n\n" + recommendations_text

    messagebox.showinfo("Результат", text)


# Окно ввода параметров студента
# Позволяет добавить несколько экзаменов, проверяет введённые данные
# и передаёт их дальше списком
class InputWindow:

    # Создаёт окно и переменные для полей
    # on_submit - функция, которая получит (список_параметров, вероятность, текст_рекомендаций)
    def __init__(self, on_submit):
        self.on_submit = on_submit

        # Добавленные в этом запуске экзамены (словари после validate)
        self.exams = []

        self.root = tk.Tk()
        self.root.title("Прогноз сдачи сессии")
        self.root.resizable(False, False)

        # Переменные связаны с полями окна и хранят введённые значения
        self.subject_var = tk.StringVar()
        self.has_debts_var = tk.BooleanVar(value=DEFAULTS["has_debts"])
        self.hours_var = tk.StringVar(value=DEFAULTS["hours"])
        self.missed_var = tk.StringVar(value=DEFAULTS["missed"])
        self.luck_var = tk.StringVar(value=DEFAULTS["luck"])
        self.total_var = tk.StringVar(value=DEFAULTS["total"])
        self.learned_var = tk.StringVar(value=DEFAULTS["learned"])
        self.exam_type_var = tk.StringVar()

        self._build()
        self._refresh_subjects()

    # Размещает подписи, поля, таблицу и кнопки в окне
    def _build(self):
        frame = ttk.Frame(self.root, padding=16)
        frame.grid()

        ttk.Label(frame, text="Предмет").grid(row=0, column=0, sticky="w", padx=(0, 12), pady=4)
        self.subject_box = ttk.Combobox(frame, textvariable=self.subject_var, values=[],
                                        state="readonly", width=50)
        self.subject_box.grid(row=0, column=1, sticky="w")
        # При выборе предмета обновляем тип сдачи
        self.subject_box.bind("<<ComboboxSelected>>", self._on_subject_change)

        ttk.Label(frame, text="Тип сдачи").grid(row=1, column=0, sticky="w", padx=(0, 12), pady=4)
        ttk.Label(frame, textvariable=self.exam_type_var).grid(row=1, column=1, sticky="w")

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

        self.add_button = ttk.Button(frame, text="Добавить экзамен", command=self._on_add)
        self.add_button.grid(row=8, column=0, columnspan=2, pady=(12, 8))

        # Таблица уже добавленных экзаменов
        ttk.Label(frame, text="Добавленные экзамены").grid(row=9, column=0, columnspan=2, sticky="w")

        columns = ("subject", "exam_type", "has_debts", "hours_per_day","missed_lectures","luck", "tickets", "hours")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=6,
                                 selectmode="browse")
        self.tree.heading("subject", text="Предмет")
        self.tree.heading("exam_type", text="Тип сдачи")
        self.tree.heading("has_debts", text="Долги")
        self.tree.heading("hours_per_day", text="Часы подготовки")
        self.tree.heading("missed_lectures", text="Пропущено занятий")
        self.tree.heading("luck", text="Удача")
        self.tree.heading("tickets", text="Билеты")
        self.tree.heading("hours", text="Ч/день")

        self.tree.column("subject", width=320)
        self.tree.column("exam_type", width=150)
        self.tree.column("has_debts", width=70, anchor="center")
        self.tree.column("hours_per_day", width=110, anchor="center")
        self.tree.column("missed_lectures", width=140, anchor="center")
        self.tree.column("luck", width=70, anchor="center")
        self.tree.column("tickets", width=70, anchor="center")
        self.tree.column("hours", width=70, anchor="center")
        self.tree.grid(row=10, column=0, columnspan=2, sticky="ew", pady=(4, 0))

        buttons = ttk.Frame(frame)
        buttons.grid(row=11, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(buttons, text="Удалить выбранный", command=self._on_remove).grid(
            row=0, column=0, padx=(0, 8))
        ttk.Button(buttons, text="Рассчитать", command=self._on_calculate).grid(
            row=0, column=1)

    # Предметы, для которых данные уже добавлены
    def _used_subjects(self):
        return {p["subject"] for p in self.exams}

    # Обновляет список предметов: убирает уже добавленные
    def _refresh_subjects(self):
        used = self._used_subjects()
        free = [s for s in SUBJECTS if s not in used]

        self.subject_box["values"] = free
        if free:
            self.subject_var.set(free[0])
            self.subject_box.state(["!disabled", "readonly"])
            self.add_button.state(["!disabled"])
        else:
            # Все предметы уже добавлены
            self.subject_var.set("")
            self.subject_box.state(["disabled"])
            self.add_button.state(["disabled"])

        self._on_subject_change()

    # Показывает тип сдачи и сложность выбранного предмета
    # event - событие от списка, при ручном вызове не нужно
    def _on_subject_change(self, event=None):
        subject = self.subject_var.get()
        if subject in SUBJECTS_DATA:
            info = SUBJECTS_DATA[subject]
            self.exam_type_var.set(f"{info['exam_type']} (сложность {info['rank']} из 5)")
        else:
            self.exam_type_var.set("")

    # Возвращает поля ввода к значениям по умолчанию
    def _reset_fields(self):
        self.has_debts_var.set(DEFAULTS["has_debts"])
        self.hours_var.set(DEFAULTS["hours"])
        self.missed_var.set(DEFAULTS["missed"])
        self.luck_var.set(DEFAULTS["luck"])
        self.total_var.set(DEFAULTS["total"])
        self.learned_var.set(DEFAULTS["learned"])

    # Собирает данные из полей, проверяет их
    # При ошибках показывает сообщение, иначе добавляет экзамен в список
    def _on_add(self):
        raw = {
            "subject": self.subject_var.get(),
            "has_debts": self.has_debts_var.get(),
            "hours_per_day": self.hours_var.get(),
            "missed_lectures": self.missed_var.get(),
            "luck": self.luck_var.get(),
            "total_tickets": self.total_var.get(),
            "learned_tickets": self.learned_var.get(),
        }

        params, errors = validate(raw, used_subjects=self._used_subjects())

        if errors:
            messagebox.showerror("Проверьте ввод", "\n".join(errors))
            return

        self.exams.append(params)
        # Название предмета используем как идентификатор строки (оно уникально)
        self.tree.insert("", "end", iid=params["subject"], values=(
            params["subject"],
            params["exam_type"],
            params["has_debts"],
            params["hours_per_day"],
            params["missed_lectures"],
            params["luck"],
            f"{params['learned_tickets']}/{params['total_tickets']}",
            params["hours_per_day"],
        ))

        self._reset_fields()
        self._refresh_subjects()

    # Удаляет выбранный в таблице экзамен, предмет снова становится доступен
    def _on_remove(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Удаление", "Выберите экзамен в таблице")
            return

        subject = selected[0]
        self.exams = [p for p in self.exams if p["subject"] != subject]
        self.tree.delete(subject)
        self._refresh_subjects()

    # Считает вероятность по всем добавленным экзаменам и передаёт результат в on_submit
    def _on_calculate(self):
        if not self.exams:
            messagebox.showerror("Нет данных", "Добавьте хотя бы один экзамен")
            return

        session_params_list = list(self.exams)
        session_probability = calculate_probability(session_params_list)

        recommendations = build_recommendations(session_params_list, session_probability)
        text = format_recommendations(recommendations)

        self.on_submit(session_params_list, session_probability, text)


    # Открывает окно и ждёт действий пользователя
    def run(self):
        self.root.mainloop()


# Запуск окна для проверки
if __name__ == "__main__":
    window = InputWindow(on_submit=handle_input)
    window.run()
