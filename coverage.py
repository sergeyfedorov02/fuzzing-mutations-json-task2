from typing import Self, Callable, Any
from trace import Trace
from inspect import getsourcelines, getfile


class CoverageTracker:
    def __init__(
            self: Self,
            function: Callable[..., Any],
            *args,
            **kwargs,
    ) -> None:
        self.function = function

        self.functions_coverage = {}
        self.total_lines_per_function = {}
        self.covered_lines_per_function = {}

    def reset(self: Self) -> None:
        self.functions_coverage.clear()
        self.total_lines_per_function.clear()
        self.covered_lines_per_function.clear()

    def extract_function_info(self: Self, results_counts) -> None:

        correct_file = getfile(self.function)

        # Проходим по всем файлам и строкам
        for filename, lineno in results_counts:
            if filename != correct_file:
                continue
            try:
                with open(filename, 'r') as file:
                    source_lines = file.readlines()
                    # Ищем функцию, в которой находится текущая строка
                    current_func = None
                    start_line = 0

                    # Ищем функцию, в которой находится текущая строка
                    for i in range(lineno - 1, -1, -1):
                        line = source_lines[i].strip()
                        if line.startswith('def '):
                            current_func = line.split('def ')[1].split('(')[0]
                            start_line = i
                            break

                    if current_func:
                        # Поиск конца функции
                        func_end_line = len(source_lines)
                        for i in range(start_line + 1, len(source_lines)):
                            if source_lines[i].strip().startswith('def '):
                                func_end_line = i
                                break

                    # Подсчет общего количества строк для функции
                    total_lines = func_end_line - start_line - 3

                    if (filename, current_func) not in self.functions_coverage:
                        self.functions_coverage[(filename, current_func)] = 0
                        self.total_lines_per_function[(filename, current_func)] = total_lines
                        self.covered_lines_per_function[
                            (filename, current_func)] = set()  # Инициализация набора для покрытых строк

                    self.functions_coverage[(filename, current_func)] += 1
                    self.covered_lines_per_function[(filename, current_func)].add(lineno)  # Добавляем покрытую строку

            except FileNotFoundError:
                continue

    def __call__(self: Self, trace: Trace) -> None:
        self.reset()
        tracer_results = trace.results()
        self.extract_function_info(tracer_results.counts)