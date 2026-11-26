import numpy as np

from .monte_carlo import monte_carlo

def get_exam_probability(params):
    """
    Вызывает симуляцию Монте-Карло и возвращает float результат по экзамену
    """
    _, binary_results, _ = monte_carlo(
        subject=params["subject"],
        has_debts=params["has_debts"],
        hours_per_day=params["hours_per_day"],
        missed_lectures=params["missed_lectures"],
        total_tickets=params["total_tickets"],
        learned_tickets=params["learned_tickets"],
        simulations=10000
    )

    return float(np.mean(binary_results))

def calculate_session_probability(session_params_list):
    """
    Вычисляет вероятность сдачи сессии: вызывает get_exam_probability
    для каждого экзамена и перемножает результаты. В конце возвращает
    float вероятность сдачи сессии и словарь {subject_name: exam_probability}
    """
    # ЗАЩИТА! (от пустого списка)
    if not session_params_list:
        return 0.0, {} 

    exam_probabilities = {}
    session_probability = 1.0

    for params in session_params_list:
        subject_name = params["subject"]
        prob = get_exam_probability(params)
        exam_probabilities[subject_name] = prob
        session_probability *= prob

    return float(session_probability), exam_probabilities

# Блок для теста
if __name__ == "__main__":
    session_list = []
    
    print("ВВОД ДАННЫХ ДЛЯ 5 ЭКЗАМЕНОВ")
    
    for i in range(5):
        print(f"\nЭкзамен {i+1} из 5")
        
        subject = input("Введите название предмета (например, Математика): ")
        has_debts = input("Есть ли хвосты? (да/нет): ").lower() == "да"
        hours = float(input("Сколько часов в день учил?: "))
        missed = int(input("Сколько занятий пропустил?: "))
        luck = int(input("Везучесть от 1 до 10: "))
        total = int(input("Всего билетов: "))
        learned = int(input("Сколько билетов выучил: "))
        
        rank = int(input("Сложность предмета (1-5): "))
        exam_type = input("Тип экзамена (Экзамен/Зачет/Зачет с оценкой): ")

        exam_params = {
            "subject": subject,
            "has_debts": has_debts,
            "hours_per_day": hours,
            "missed_lectures": missed,
            "luck": luck,
            "total_tickets": total,
            "learned_tickets": learned,
            "subject_rank": rank,
            "exam_type": exam_type
        }
        
        session_list.append(exam_params)

    print("\nЗАПУСК СИМУЛЯЦИИ")
    
    result, exam_probabilities = calculate_session_probability(session_list)
    
    print(f"\nИТОГОВАЯ ВЕРОЯТНОСТЬ СДАТЬ СЕССИЮ: {result * 100:.1f}%")
    for i in range(len(session_list)):
        subject_name = session_list[i]["subject"]
        prob = exam_probabilities[subject_name]
        print(f"Вероятность сдать {subject_name}: {prob * 100:.1f}%")
