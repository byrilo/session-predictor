import numpy as np

from ..model.luck import random_luck
from ..model.ticket import calculate_p_ticket as calculate_ticket
from ..model.base_score import base_score, SUBJECTS


def monte_carlo(
    subject: str,
    has_debts: bool,
    hours_per_day: float,
    missed_lectures: int,
    total_tickets: int,
    learned_tickets: int,
    simulations: int = 10000
):
    # Получаем параметры предмета
    difficulty, exam_type = SUBJECTS.get(subject, (3, "Экзамен"))

    # 1 — экзамен сдан, 0 — экзамен не сдан
    binary_results = []

    for _ in range(simulations):

        #Генерируем случайное значение удачи
        luck_value = random_luck(mu=5.0, sigma=1.5)

        #Рассчитываем вероятность вытянуть подготовленный билет
        p_ticket = calculate_ticket(
            learned=learned_tickets,
            total=total_tickets,
            exam_type=exam_type,
            rank=difficulty,
            luck=luck_value
        )

        #Передаём рассчитанную вероятность в базовую модель
        simulated_learned_tickets = p_ticket * total_tickets

        success_chance = base_score(
            subject=subject,
            has_debts=has_debts,
            hours_per_day=hours_per_day,
            missed_lectures=missed_lectures,
            luck=luck_value,
            total_tickets=total_tickets,
            learned_tickets=simulated_learned_tickets
        )

        #Результат экзамена
        if np.random.random() < success_chance:
            is_passed = 1
        else:
            is_passed = 0

        binary_results.append(is_passed)

    binary_results = np.array(binary_results)

    total_probability = np.mean(binary_results) * 100

    return float(total_probability), binary_results

