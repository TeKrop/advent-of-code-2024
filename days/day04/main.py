from functools import cache, cached_property

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    xmas = "XMAS"

    ###########################
    # DAY 04 - Common Part
    ###########################

    def solve(self) -> tuple[int, int]:
        self.grid = Grid(self.lines)
        self.xmas_length = len(self.xmas)
        return super().solve()

    ###########################
    # DAY 04 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return sum(
            self._count_xmas_from(i, j)
            for i, line in enumerate(self.lines)
            for j, char in enumerate(line)
            if char == "X"
        )

    def _count_xmas_from(self, i_pos: int, j_pos: int) -> int:
        return sum(
            self._is_xmas(i_pos, j_pos, i_delta, j_delta)
            for i_delta in (-1, 0, 1)
            for j_delta in (-1, 0, 1)
            if not (i_delta == 0 and j_delta == 0)
        )

    def _is_xmas(self, i_pos: int, j_pos: int, i_delta: int, j_delta: int) -> bool:
        return all(
            self.xmas[i] == self.grid[i_pos + (i_delta * i)][j_pos + (j_delta * i)]
            for i in range(0, self.xmas_length)
        )

    ###########################
    # DAY 04 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return sum(
            self._is_xmas_cross(i, j)
            for i, line in enumerate(self.lines)
            for j, char in enumerate(line)
            if char == "A"
        )

    def _is_xmas_cross(self, i_pos: int, j_pos: int) -> bool:
        first_diagonal_is_ok = {
            self.grid[i_pos - 1][j_pos - 1],
            self.grid[i_pos + 1][j_pos + 1],
        } == {"M", "S"}

        second_diagonal_is_ok = {
            self.grid[i_pos - 1][j_pos + 1],
            self.grid[i_pos + 1][j_pos - 1],
        } == {"M", "S"}

        return first_diagonal_is_ok and second_diagonal_is_ok


class Line:
    def __init__(self, line: str | None):
        self.line = line

    @cached_property
    def nb_chars(self) -> int:
        return len(self.line)

    @cache
    def __getitem__(self, j_pos: int) -> str | None:
        return self.line[j_pos] if self.line and (0 <= j_pos < self.nb_chars) else None


class Grid:
    def __init__(self, lines: list[str]):
        self.lines: list[Line] = [Line(line) for line in lines]

    @cached_property
    def nb_lines(self) -> int:
        return len(self.lines)

    @cache
    def __getitem__(self, i_pos: int) -> Line:
        return self.lines[i_pos] if (0 <= i_pos < self.nb_lines) else Line(None)
