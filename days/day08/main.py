from collections import defaultdict
from dataclasses import dataclass
from functools import cache, cached_property
from itertools import combinations

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 08 - Common Part
    ###########################

    def solve(self) -> tuple[int, int]:
        self.grid = Grid(self.lines)
        self.grid_nb_lines = self.grid.nb_lines
        self.grid_nb_chars = self.grid.nb_chars
        return super().solve()

    def _get_antinodes(
        self, antennas: set["Position"], in_line: bool = False
    ) -> set["Position"]:
        antennas_combinations = combinations(antennas, 2)
        return {
            antinode
            for positions in antennas_combinations
            for antinode in self._get_antinodes_positions(positions, in_line=in_line)
        }

    def _get_antinodes_positions(
        self, positions: tuple["Position", "Position"], in_line: bool = False
    ) -> set["Position"]:
        antinode_positions: set["Position"] = set()
        update_vectors: tuple["Position", "Position"] = (
            positions[1] - positions[0],
            positions[0] - positions[1],
        )

        previous_positions = positions

        # Generate the antinodes until limit is reached in both ways or
        # stop after first iteration if we're not generating an entire line
        while True:
            # Calculate new position
            new_positions = (
                previous_positions[0] + update_vectors[0],
                previous_positions[1] + update_vectors[1],
            )

            # Compute valid positions and update antinode_positions
            valid_positions = {pos for pos in new_positions if self._is_in_grid(pos)}
            antinode_positions |= valid_positions

            # Stop if there is no valid position or if we should stop after first iteration
            if len(valid_positions) == 0 or not in_line:
                break

            # Update for next iteration
            previous_positions = new_positions

        return antinode_positions

    @cache
    def _is_in_grid(self, position: "Position") -> bool:
        return (
            0 <= position.x < self.grid_nb_lines
            and 0 <= position.y < self.grid_nb_chars
        )

    ###########################
    # DAY 08 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        return len(
            {
                antinode
                for antennas in self.grid.antennas_positions.values()
                for antinode in self._get_antinodes(antennas)
            }
        )

    ###########################
    # DAY 08 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return len(
            {
                antinode
                for antennas in self.grid.antennas_positions.values()
                for antinode in self._get_antinodes(antennas, in_line=True)
            }
        )


@dataclass
class Position:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: "Position"):
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Position") -> "Position":
        return Position(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: "Position") -> "Position":
        return Position(x=self.x - other.x, y=self.y - other.y)


class Grid:
    data: list[list[str]]

    def __init__(self, lines: list[str]):
        self.data = [[char for char in line] for line in lines]

    @cached_property
    def nb_lines(self) -> int:
        return len(self.data)

    @cached_property
    def nb_chars(self) -> int:
        return len(self.data[0])

    @cached_property
    def antennas_positions(self) -> dict[str, set[Position]]:
        antennas = defaultdict(set)
        for i, line in enumerate(self.data):
            for j, char in enumerate(line):
                if char != ".":
                    antennas[char].add(Position(x=i, y=j))
        return dict(antennas)
