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
        is_increasing: bool | None = None

        for previous, current in zip(self.levels, self.levels[1:]):
            difference = current - previous

            if not (1 <= abs(difference) <= 3):
                return False

            if is_increasing is None:
                is_increasing = difference > 0

            if (difference > 0 and not is_increasing) or (
                difference < 0 and is_increasing
            ):
                return False

        return True

    @property
    def is_stable_by_tolerating_bad_level(self) -> bool:
        return self.is_stable or any(
            Report(levels_subset).is_stable
            for i in range(len(self.levels))
            if (levels_subset := self.levels[:i] + self.levels[i + 1 :])
        )
