import numpy as np

# импорт файлов
from model.base_score import base_score 
from model.ticket import calculate_p_ticket
from model.luck import random_luck

WEIGHT_BASE = 0.6        # Вес базового балла (знания)
WEIGHT_TICKET = 0.3      # Вес вероятности вытянуть билет
WEIGHT_LUCK = 0.1        # Вес удачи

def get_exam_probability(params):
    """
    Считает вероятность сдать 1 экзамен и возвращает число от 0.0 до 1.0
    """
    results = []
    
    # цикл на 10 000 итераций для одного экзамена
    for _ in range(10000):
        # 1) базовый балл
        base = base_score(
            subject=params["subject"],
            has_debts=params["has_debts"],
            hours_per_day=params["hours_per_day"],
            missed_lectures=params["missed_lectures"],
            luck=params["luck"],
            total_tickets=params["total_tickets"],
            learned_tickets=params["learned_tickets"]
        )
        
        # 2) вероятность вытянуть билет
        p_ticket = calculate_p_ticket(
            learned=params["learned_tickets"],
            total=params["total_tickets"],
            exam_type=params["exam_type"],
            rank=params["subject_rank"],
            luck=params["luck"]
        )
        
        # 3) генератор случайностей
        luck_factor = random_luck() 
        luck_normalized = luck_factor / 10.0

        # 4) итоговый балл (60% база, 30% билет, 10% удача)
        final_score = (base * WEIGHT_BASE) + (p_ticket * WEIGHT_TICKET) + (luck_normalized * WEIGHT_LUCK)
        
        if np.random.random() < final_score:
            results.append(1)
        else:
            results.append(0)
            
    # Возвращаем вероятность сдачи этого одного экзамена
    return sum(results) / len(results)


def calculate_session_probability(session_params_list):
    """
    Главная функция для расчета вероятности сдачи ВСЕЙ сессии
    Принимает список параметров для каждого из 5 экзаменов и возвращает общую вероятность сдать сессию
    """
    # ЗАЩИТА! (от пустого списка)
    if not session_params_list:
        return 0.0 
    
    # 1) Получаем вероятность сдать каждый экзамен по отдельности
    exam_probabilities = []
    for params in session_params_list:
        prob = get_exam_probability(params)
        exam_probabilities.append(prob)
        print(f"  - Экзамен по предмету '{params['subject']}': {prob * 100:.1f}%")
    
    # 2) Считаем итоговую вероятность перемножением 
    session_probability = 1.0
    for prob in exam_probabilities:
        session_probability *= prob
            
    # 3) Возвращаем итоговую вероятность
    return session_probability

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
    
    result = calculate_session_probability(session_list)
    
    print(f"\nИТОГОВАЯ ВЕРОЯТНОСТЬ СДАТЬ СЕССИЮ: {result * 100:.1f}%")