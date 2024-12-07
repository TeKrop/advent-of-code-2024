from enum import StrEnum, auto
from functools import cache, cached_property
from itertools import cycle
from typing import Generator

from scripts.utils import AbstractPuzzleSolver


class Direction(StrEnum):
    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 04 - Common Part
    ###########################
    direction_vectors: dict[Direction, tuple[int, int]] = {
        Direction.UP: (-1, 0),
        Direction.RIGHT: (0, 1),
        Direction.DOWN: (1, 0),
        Direction.LEFT: (0, -1),
    }

    def solve(self) -> tuple[int, int]:
        self.grid = Grid(self.lines)
        self.grid_nb_lines = self.grid.nb_lines
        self.grid_nb_chars = self.grid.nb_chars

        self.initial_guard_pos = self.grid.get_guard_pos()

        return super().solve()

    def get_visited_positions(self, grid: "Grid") -> set[tuple[int, int]]:
        guard = Guard(pos=self.initial_guard_pos)
        visited_positions = {guard.pos}

        # Iterate over guard positions
        while True:
            # Check next position, if it's outside the grid then stop
            if not (next_pos := self._get_next_pos(guard)):
                break

            # If it's an obstruction, just change the direction
            if grid[next_pos] == Cell.OBSTRUCTION:
                guard.turn_right()
                continue

            # Else it's a valid move, update guard pos and counter
            guard.pos = next_pos
            visited_positions.add(guard.pos)

        return visited_positions

    def _get_next_pos(self, guard: "Guard") -> tuple[int, int]:
        return self._compute_next_pos(guard.pos, guard.direction)

    @cache
    def _compute_next_pos(
        self, pos: tuple[int, int], direction: "Direction"
    ) -> tuple[int, int]:
        direction_vector = self.direction_vectors[direction]
        next_pos = (
            pos[0] + direction_vector[0],
            pos[1] + direction_vector[1],
        )
        return (
            next_pos
            if 0 <= next_pos[0] < self.grid_nb_lines
            and 0 <= next_pos[1] < self.grid_nb_chars
            else None
        )

    ###########################
    # DAY 06 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return len(self.get_visited_positions(self.grid))

    ###########################
    # DAY 06 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return sum(
            self.is_guard_stuck_in_loop(possible_grid)
            for possible_grid in self.get_grid_combinations(self.grid)
        )

    def get_grid_combinations(self, grid: "Grid") -> Generator["Grid", None, None]:
        """Use positions computed in part 1 to iterate"""
        for empty_pos in self.get_visited_positions(grid):
            grid[empty_pos] = Cell.OBSTRUCTION
            yield grid
            grid[empty_pos] = Cell.EMPTY

    def is_guard_stuck_in_loop(self, grid: "Grid") -> int:
        guard = Guard(pos=self.initial_guard_pos)
        visited_positions: set[tuple[tuple[int, int], Direction]] = {
            guard.pos,
            guard.direction,
        }

        # Iterate over guard positions
        while True:
            # Check next position, if it's outside the grid then stop
            if not (next_pos := self._get_next_pos(guard)):
                break

            # If next pos has already been visited in the same direction,
            # guard is in a loop, we can stop here
            if (next_pos, guard.direction) in visited_positions:
                return True

            # If it's an obstruction, just change the direction
            if grid[next_pos] == Cell.OBSTRUCTION:
                guard.turn_right()
                continue

            # Else it's a valid move, update guard pos and counter
            guard.pos = next_pos
            visited_positions.add((guard.pos, guard.direction))

        # Guard is now outside, he's not stuck in a loop
        return False


class Cell(StrEnum):
    EMPTY = "."
    OBSTRUCTION = "#"
    GUARD = "^"


class Grid:
    data: list[list[Cell]]

    def __init__(self, lines: list[str]):
        self.data = [[char for char in line] for line in lines]

    def __getitem__(self, index: tuple[int, int]) -> Cell | None:
        return self.data[index[0]][index[1]]

    def __setitem__(self, index: tuple[int, int], element: Cell) -> None:
        self.data[index[0]][index[1]] = element

    @cached_property
    def nb_lines(self) -> int:
        return len(self.data)

    @cached_property
    def nb_chars(self) -> int:
        return len(self.data[0])

    def get_guard_pos(self) -> tuple[int, int]:
        return next(
            (i, j)
            for i, line in enumerate(self.data)
            for j, char in enumerate(line)
            if char == Cell.GUARD
        )


class Guard:
    directions_cycle: Generator[Direction, None, None]
    direction: Direction
    pos: tuple[int, int]

    def __init__(self, pos: tuple[int, int]):
        self.pos = pos
        self.directions_cycle = cycle(
            [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        )
        self.direction = next(self.directions_cycle)

    def turn_right(self) -> None:
        self.direction = next(self.directions_cycle)
