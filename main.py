from tkinter import messagebox

from gui.input_window import InputWindow


def handle_input(params):
    # замените на вызов симуляции, когда она будет готова
    lines = []
    for key, value in params.items():
        lines.append(f"{key}: {value}")

    messagebox.showinfo("Данные приняты", "\n".join(lines))


# Точка входа в программу
if __name__ == "__main__":
    window = InputWindow(on_submit=handle_input)
    window.run()