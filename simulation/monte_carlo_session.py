import numpy as np

# импорт файлов
from model.base_score import base_score 
from model.ticket import calculate_p_ticket
from model.luck import random_luck

WEIGHT_BASE = 0.6        # Вес базового балла (знания)
WEIGHT_TICKET = 0.3      # Вес вероятности вытянуть билет
WEIGHT_LUCK = 0.1        # Вес удачи
PASSING_THRESHOLD = 0.5  # Порог сдачи (проходной балл)

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
        
        # 5) сдал или нет (порог 0.5)
        if final_score >= PASSING_THRESHOLD:
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
    
    # 2) симулируем всю сессию целиком 10 000 раз
    session_results = []
    for _ in range(10000):
        passed_all = True 
        
        # Проходимся по каждому экзамену
        for prob in exam_probabilities:
            # если случайное число больше вероятности => экзамен завален
            if np.random.random() > prob:
                passed_all = False
                break # Если один экзамен не сдан => сессия уже не сдана(метод Монте-Карло)
                
        if passed_all:
            session_results.append(1) #сдал все 5
        else:
            session_results.append(0) #не сдал хотя бы один
            
    # 3) Считаем итоговую вероятность сдачи сессии
    session_probability = sum(session_results) / len(session_results)
    return session_probability