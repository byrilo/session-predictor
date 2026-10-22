import numpy as np
SUBJECTS = {
    "Программирование": (4, "Экзамен"),
    "Математика": (5, "Экзамен"),
    "Дискретная математика": (4, "Экзамен"),
    "Объектно-ориентированное программирование (ООП)": (5, "Экзамен"),
    "Основы российской государственности (ОРГ)": (2, "Зачет"),
    "Деловые коммуникации": (2, "Зачет"),
    "Физическая культура и спорт": (1, "Зачет"),
    "Информатика": (3, "Зачет с оценкой"),
    "История России": (3, "Зачет с оценкой"),
    "Алгоритмы и структуры данных": (4, "Зачет с оценкой")
}
EXAM_TYPE_FACTOR = {
    "Экзамен": 1.0,
    "Зачет с оценкой": 1.1,
    "Зачет": 1.25
}
def base_score(
        subject: str,
        has_debts: bool,
        hours_per_day: float,
        missed_lectures: int,
        luck: int,
        total_tickets: int,
        learned_tickets: int
) -> float:
    difficulty, exam_type = SUBJECTS.get(subject, (3, "Экзамен"))

    if exam_type == "Зачет" and missed_lectures <= 6:
        return 0.95 
    attendance = 1.0 - min(missed_lectures / 30.0, 1.0)
    tickets = learned_tickets / max(total_tickets, 1)
    hours = min(hours_per_day / 6.0, 1.0)
    luck_n = max(0.0, min((luck - 1) / 9.0, 1.0))
    diff_n = (difficulty - 1) / 4.0

    raw_score = (
            0.35 * tickets
            + 0.30 * attendance
            + 0.20 * hours
            + 0.15 * luck_n
    )
    raw_score -= 0.15 * diff_n
    if has_debts:
        raw_score -= 0.20
    raw_score *= EXAM_TYPE_FACTOR.get(exam_type, 1.0)
    return float(np.clip(raw_score, 0.05, 0.95))
