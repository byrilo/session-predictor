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
