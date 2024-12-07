import operator
from itertools import product
from typing import Callable, Generator

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 07 - Common Part
    ###########################

    def get_total_calibration_result(self, operators: list[Callable]) -> int:
        return sum(
            Equation(line).get_nb_possibilities(operators) for line in self.lines
        )

    ###########################
    # DAY 07 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return self.get_total_calibration_result([operator.add, operator.mul])

    ###########################
    # DAY 07 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return self.get_total_calibration_result(
            [operator.add, operator.mul, self.concat]
        )

    @staticmethod
    def concat(first_number: int, second_number: int) -> int:
        """Concatenate two integers as is they were strings"""

        # First find out the number of digits of second number
        digits = 1
        while second_number // 10**digits > 0:
            digits += 1

        # Then multiply by power of ten and add the second number
        return first_number * 10**digits + second_number


class Equation:
    test_value: int
    numbers: list[int]

    def __init__(self, line: str):
        test_value_str, numbers_str = line.split(":")
        self.test_value = int(test_value_str)
        self.numbers = [int(number) for number in numbers_str.split()]

    def __repr__(self) -> str:
        return f"<Equation {self.test_value} -> {self.numbers}>"

    def get_nb_possibilities(self, operators: list[Callable]) -> int:
        operators_possibilities = product(operators, repeat=len(self.numbers) - 1)

        return (
            self.test_value
            if any(
                self._are_valid_operators(operators)
                for operators in operators_possibilities
            )
            else 0
        )

    def _are_valid_operators(self, operators: Generator[Callable, None, None]) -> bool:
        """Loop over operators and apply operations. As we only have operators
        that will increase the value, we'll stop early if the value is already
        too high.
        """
        computed_value = self.numbers[0]

        for i, oper in enumerate(operators):
            computed_value = oper(computed_value, self.numbers[i + 1])
            if computed_value > self.test_value:
                return False

        return computed_value == self.test_value
