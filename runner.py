from typing import Callable, Self, Any
from trace import Trace
from enum import Enum

from coverage import CoverageTracker


class RunnerResult(Enum):
    PASS = 1
    FAIL = 2


class Runner:
    def __init__(
            self: Self,
            function: Callable[..., Any],
            *args,
            **kwargs,
    ) -> None:
        self.function = function
        self.coverage_tracker = CoverageTracker(self.function)
        self.result_status = None

    def run_function(self: Self, *args, **kwargs) -> Any:
        return self.function(*args, **kwargs)

    def run_coverage(self: Self, *args, **kwargs) -> Any:
        tracer = Trace(trace=False, count=True)
        try:
            result = tracer.runfunc(self.function, *args, **kwargs)
            return result
        except Exception as exception:
            raise Exception from exception
        finally:
            self.coverage_tracker(tracer)

    def run(self: Self, *args, **kwargs) -> tuple[Any, RunnerResult]:
        try:
            function_result = self.run_coverage(*args, **kwargs)
            test_result = RunnerResult.PASS
        except Exception:
            function_result = None
            test_result = RunnerResult.FAIL

        return function_result, test_result