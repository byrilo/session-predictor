import numpy as np


def random_luck(mu: float = 5.0, sigma: float = 1.5) -> int:
    """
    Генерирует уровень везучести студента (целое число от 0 до 10).
    Использует нормальное распределение из библиотеки numpy.

    :param mu: Математическое ожидание (среднее значение). По умолчанию 5.
    :param sigma: Стандартное отклонение (разброс). По умолчанию 1.5.
    :return: Целое число от 0 до 10.
    """
    if sigma <= 0:
        raise ValueError("Стандартное отклонение (sigma) должно быть больше нуля.")

    # 1. Генерируем число из нормального распределения через numpy
    # np.random.normal(среднее, отклонение) выдает float
    raw_luck = np.random.normal(loc=mu, scale=sigma)

    # 2. Округляем до целого и загоняем в рамки 0-10
    # np.clip обрезает значения: всё, что меньше 0, станет 0; больше 10 станет 10
    final_luck = np.clip(round(raw_luck), 0, 10)

    return int(final_luck)