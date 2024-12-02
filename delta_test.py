def delta_debug(current_str, function):
    n = 2  # Начальное количество фрагментов
    original_result = function(current_str)  # Оригинальный результат для исходной строки

    while n <= len(current_str):
        # Разбиваем строку на `n` фрагментов
        chunks = [current_str[i:i + len(current_str) // n] for i in range(0, len(current_str), len(current_str) // n)]
        if len(chunks) > n:  # Если осталось меньше символов, добавим их в последний фрагмент
            chunks[-2] += chunks[-1]
            chunks.pop()

        reduced = False
        for i in range(len(chunks)):
            # Пробуем исключить фрагмент
            without_chunk = ''.join(chunks[:i] + chunks[i + 1:])

            if function(without_chunk) == original_result:
                # Если исключение фрагмента не изменило результат S, "усекаем" строку
                current_str = without_chunk
                n = max(n - 1, 2)  # Уменьшаем количество фрагментов
                reduced = True
                break

        if not reduced:  # Если не удалось упростить данные, увеличиваем количество фрагментов
            if n == len(current_str):
                break

            n = min(n * 2, len(current_str))

    return current_str


# Пример использования
def example_function(input_string):
    return "error" in input_string


if __name__ == "__main__":
    # Исходная строка
    original_string = "abcdefghijklmnopqrsterroruvwxerroryz"

    # Минимизация
    minimized_string = delta_debug(original_string, example_function)

    print("Изначальная строка:", original_string)
    print("Минимизированная строка:", minimized_string)