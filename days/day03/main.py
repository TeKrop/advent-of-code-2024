import re

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    first_mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
    second_mul_pattern = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|don\'t\(\)|do\(\)")

    ###########################
    # DAY 03 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(
            int(result[0]) * int(result[1])
            for line in self.lines
            for result in re.findall(self.first_mul_pattern, line)
        )

    ###########################
    # DAY 03 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        total_sum = 0
        instructions_enabled = True

        for line in self.lines:
            line_sum = 0

            for match in self.second_mul_pattern.finditer(line):
                if (
                    instructions_enabled
                    and (x := match.group(1))
                    and (y := match.group(2))
                ):
                    line_sum += int(x) * int(y)
                elif match.group(0) == "don't()":
                    instructions_enabled = False
                elif match.group(0) == "do()":
                    instructions_enabled = True

            total_sum += line_sum

        return total_sum
