import matplotlib.pyplot as plt
import numpy as np


def analyze_base_score(
    base_scores: np.ndarray,
    binary_results: np.ndarray,
    save_path: str | None = "base_score_hist.png",
    show_plot: bool = False,
):
    """
    Вычисляет коэффициент Пирсона и строит гистограмму base_score

    - Если save_path не None, сохраняет гистограмму в указанный путь
    - Если show_plot True, отображает гистограмму
    
    В конце всегда возвращает коэффициент Пирсона между base_scores и binary_results,
    а также объект фигуры (гистограммы)

    Пример использования: analyze_base_score(base_scores, binary_results, save_path="hist.png", show_plot=True)
    """

    # Вычисление коэффициента
    if np.std(base_scores) == 0 or np.std(binary_results) == 0:
        pearson_r = 0.0
    else:
        pearson_r = float(np.corrcoef(base_scores, binary_results)[0, 1])

    # Построение гистограммы
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(
        base_scores, bins=25, color="steelblue", edgecolor="black", alpha=0.8
    )
    ax.set_title(
        f"Распределение base_score\nКоэффициент Пирсона r = {pearson_r:.3f}"
    )
    ax.set_xlabel("Значение base_score")
    ax.set_ylabel("Частота (количество симуляций)")
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    # Сохранение в файл, если указан путь
    if save_path:
        fig.savefig(save_path, bbox_inches="tight")

    # Отображение графика
    if show_plot:
        plt.show()
    else:
        plt.close(fig)

    return pearson_r, fig

# БЛОК ДЛЯ ТЕСТА
if __name__ == "__main__":
    from simulation.monte_carlo import monte_carlo

    print("Запускаем тестовую симуляцию для предмета 'Математика'...")
    
    prob, results, scores = monte_carlo(
        subject="Математика",
        has_debts=False,
        hours_per_day=3.5,
        missed_lectures=4,
        total_tickets=30,
        learned_tickets=18,
        simulations=10000
    )

    print(f"Итоговая вероятность сдачи: {prob:.2f}%")

    r_coef, _ = analyze_base_score(
        base_scores=scores,
        binary_results=results,
        save_path="test_base_score_hist.png",
        show_plot=True
    )

    print(f"Коэффициент корреляции Пирсона: {r_coef:.4f}")
