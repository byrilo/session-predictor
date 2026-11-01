def create_file(self):
    with open("read file.txt", "w", encoding="utf-8") as file:
        file.write("\nПредмет:           " + self.subject_var.get())
        file.write("\nЧасы подготовки:   " + self.hours_var.get())
        file.write("\nПропущено занятий: " + self.missed_var.get())
        file.write("\nВезучесть:         " + self.luck_var.get())
        file.write("\nВыученно билетов:  " + self.learned_var.get())
        file.write("\nВсего билетов:     " + self.total_var.get())
        file.write("\nРезультат:         ")
