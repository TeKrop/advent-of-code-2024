from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 02 - Common Part
    ###########################
    def solve(self) -> tuple[int, int]:
        self.reports: list["Report"] = [Report.from_line(line) for line in self.lines]
        return super().solve()

    ###########################
    # DAY 02 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(report.is_stable for report in self.reports)

    ###########################
    # DAY 02 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return sum(report.is_stable_by_tolerating_bad_level for report in self.reports)


class Report:
    def __init__(self, levels: list[int]):
        self.levels = levels

    @classmethod
    def from_line(cls, line: str) -> "Report":
        return cls(levels=[int(level) for level in line.split(" ")])

    @property
    def is_stable(self) -> bool:
        levels_iterator = iter(self.levels)
        previous_value: int = next(levels_iterator)
        is_increasing: bool | None = None

        for value in levels_iterator:
            difference = value - previous_value
            if not (1 <= abs(difference) <= 3):
                return False

            if is_increasing is None:
                is_increasing = difference > 0

            if (value > previous_value and not is_increasing) or (
                value < previous_value and is_increasing
            ):
                return False

            previous_value = value

        return True

    @property
    def is_stable_by_tolerating_bad_level(self) -> bool:
        if self.is_stable:
            return True

        nb_levels = len(self.levels)

        for i in range(nb_levels):
            levels_subset = self.levels[:i] + self.levels[i + 1 :]
            if Report(levels_subset).is_stable:
                return True

        return False
