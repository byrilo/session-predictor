# visualization.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные
df = pd.read_csv("analytics_data.csv")
print(f"✅ Данные загружены! Строк: {len(df)}")

fig = plt.figure(figsize=(12, 10))
fig.suptitle("Прогнозирование успешной сдачи сессии\n", fontsize=16, fontweight="bold", y=0.98)

# Слева сверху - гистограмма. Справа сверху - зависимость
# Снизу - большая карта на две колонки
ax1 = plt.subplot2grid((2, 2), (0, 0))
ax2 = plt.subplot2grid((2, 2), (0, 1))
ax3 = plt.subplot2grid((2, 2), (1, 0), colspan=2)


# Гистограмма

main_prob = df["success_probability"].mean()
ax1.hist(df["success_probability"], bins=20, color="skyblue", edgecolor="black", alpha=0.8)
ax1.axvline(main_prob, color="red", linestyle="--", linewidth=2, label=f"Средняя = {main_prob:.2f}")
ax1.set_title("Гистограмма успехов", fontsize=13, pad=10)
ax1.set_xlabel("Вероятность успеха")
ax1.set_ylabel("Кол-во студентов")
ax1.legend()
ax1.grid(axis="y", alpha=0.5)

# Зависимость от часов

ax2.scatter(df["hours_studied"], df["success_probability"], alpha=0.5, color="teal", s=25)
ax2.set_title("Зависимость вероятности от часов", fontsize=13, pad=10)
ax2.set_xlabel("Часы подготовки")
ax2.set_ylabel("Вероятность успеха")
ax2.set_ylim(0, 1.02)
ax2.grid(alpha=0.5)

# ГРАФИК 3: Тепловая карта

sc = ax3.scatter(
    df["hours_studied"],
    df["tickets_learned"],
    c=df["success_probability"],
    cmap="RdYlGn",
    s=60, # Точки покрупнее
    alpha=0.9,
    vmin=0, vmax=1,
    edgecolors='black',
)
ax3.set_title("Тепловая карта: Часы подготовки vs Выученные билеты", fontsize=13, pad=10)
ax3.set_xlabel("Часы подготовки", fontsize=12)
ax3.set_ylabel("Выученные билеты", fontsize=12)

cbar = plt.colorbar(sc, ax=ax3, pad=0.02)
cbar.set_label("Вероятность успеха", fontsize=12)

# настройка отступов

plt.tight_layout()
plt.subplots_adjust(top=0.88, hspace=0.5, wspace=0.25)

fig.savefig("report.png", dpi=150, bbox_inches="tight")
print("✅ Графики успешно сохранены в файл 'report.png'!")

plt.show()