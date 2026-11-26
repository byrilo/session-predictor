from tkinter import messagebox

from gui.input_window import InputWindow


def handle_input(params, recommendations_text=""):
    # замените на вызов симуляции, когда она будет готова
    lines = []
    for key, value in params.items():
        lines.append(f"{key}: {value}")

    text = "\n".join(lines)
    if recommendations_text:
        text += "\n\n" + recommendations_text

    messagebox.showinfo("Данные приняты", text)


# Точка входа в программу
if __name__ == "__main__":
    window = InputWindow(on_submit=handle_input)
    window.run()
