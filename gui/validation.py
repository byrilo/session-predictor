def to_int(text):
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        return None

    
def to_float(text):
    text = text.strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None

    
def check_range(value, low, high, name):
    if value is None:
        return f"«{name}»: нужно ввести число"
    if value < low or value > high:
        return f"«{name}»: допустимо от {low} до {high}"
    return None


def validate(raw):
    errors = []

    hours = to_float(raw["hours_per_day"])
    error = check_range(hours, 0, 12, "Часы подготовки в день")
    if error is not None:
        errors.append(error)

    missed = to_int(raw["missed_lectures"])
    error = check_range(missed, 0, 30, "Пропущено занятий")
    if error is not None:
        errors.append(error)

    if errors:
        return None, errors

    params = {
        "hours_per_day": hours,
        "missed_lectures": missed,
    }
    return params, []


if __name__ == "__main__":

    good = {"hours_per_day": "3", "missed_lectures": "2"}
    bad = {"hours_per_day": "15", "missed_lectures": "abc"}

    print(validate(good))
    print(validate(bad))


