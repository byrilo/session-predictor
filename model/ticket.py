def calculate_p_ticket(learned, total, exam_type, rank, luck):
    p_base = learned / total # базовая вероятность (бернулли)
    type_coef = {"Экзамен": 0.8, "Зачет с оценкой": 1.0, "Зачет": 1.2}.get(exam_type, 1.0)
    subject_coef = 1.2 - (rank / 5) * 0.5 # (0.7-1.2)
    luck_coef = 0.9 + (luck / 10) * 0.2 # везучесть(0.92 - 1.1)
    p_ticket = p_base * type_coef * subject_coef * luck_coef # часть формулы
    return max(0.0, min(1.0, p_ticket))
