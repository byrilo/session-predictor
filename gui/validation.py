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

if __name__ == "__main__":

    print(to_int("5"))
    print(to_int("  12 "))

    print(to_float("2.5"))
    print(to_float("2,5"))

    print(check_range(to_float("5"), 0, 12, "Часы"))
    print(check_range(to_float("15"), 0, 12, "Часы"))


