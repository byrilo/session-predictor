def to_int(text):
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        return None
    
print(to_int("5"))
print(to_int("  12 "))
print(to_int("много"))
print(to_int("2.5"))

def to_float(text):
    text = text.strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return None
    
print(to_float("2.5"))
print(to_float("2,5"))
print(to_float(" 3 "))
print(to_float("пять"))