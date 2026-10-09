# Пока что как затычка, нужна бд
SUBJECTS = ["Матан", "Прога", "История", "Физ-ра"]
EXAM_FORMS = ["Устный", "Письменный", "Тест"]

# Функция преобразования строки в целое
# Принимат текст введённый пользователем
# Возвращает целое число или None
def to_int(text):
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        return None

# Функция преобразования строки в дробное число 
# Принимат текст введённый пользователем
# Возвращает дробное число или None
def to_float(text):
    text = text.strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None

# Функция которая проверяет, что введённое число находится в заданном диапазоне
# value - проверяемое число
# low - минимально допустимое значение
# high - максимально допустимое значение
# name - название поля для текста ошибки
def check_range(value, low, high, name):
    if value is None:
        return f"«{name}»: нужно ввести число"
    if value < low or value > high:
        return f"«{name}»: допустимо от {low} до {high}"
    return None

# Функция которая проверяет параметры введённые пользователем
# Принимает raw - словарь значений 
# Возвращает params и errors
def validate(raw):
    errors = []

    subject = raw["subject"]
    if subject not in SUBJECTS:
        errors.append("Выберите предмет из списка")

    exam_form = raw["exam_form"]
    if exam_form not in EXAM_FORMS:
        errors.append("Выберите форму экзамена из списка")

    has_debts = bool(raw["has_debts"])

    hours = to_float(raw["hours_per_day"])
    error = check_range(hours, 0, 12, "Часы подготовки в день")
    if error is not None:
        errors.append(error)

    missed = to_int(raw["missed_lectures"])
    error = check_range(missed, 0, 30, "Пропущено занятий")
    if error is not None:
        errors.append(error)

    luck = to_int(raw["luck"])
    error = check_range(luck, 1, 10, "Везучесть")
    if error is not None:
        errors.append(error)

    total = to_int(raw["total_tickets"])
    error = check_range(total, 10, 50, "Всего билетов")
    if error is not None:
        errors.append(error)

    learned = to_int(raw["learned_tickets"])
    error = check_range(learned, 0, 50, "Выучено билетов")
    if error is not None:
        errors.append(error)

    if total is not None and learned is not None and learned > total:
        errors.append("Выученных билетов не может быть больше, чем всего билетов")

    if errors:
        return None, errors

    params = {
        "hours_per_day": hours,
        "missed_lectures": missed,
        "luck": luck,                 
        "total_tickets": total,       
        "learned_tickets": learned,   
        "subject": subject,
        "exam_form": exam_form,
        "has_debts": has_debts,
    }
    return params, []


if __name__ == "__main__":
    good = {"subject": "Матан", "exam_form": "Устный", "has_debts": False,
           "hours_per_day": "3", "missed_lectures": "2", "luck": "7",
           "total_tickets": "25", "learned_tickets": "18"}
    bad = {"subject": "Химия", "exam_form": "Устный", "has_debts": True,
          "hours_per_day": "3", "missed_lectures": "2", "luck": "0",
          "total_tickets": "20", "learned_tickets": "25"}
    

    print(validate(good))
    print(validate(bad))