from collections import Counter
from typing import Iterable

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    ###########################
    # DAY 01 - Common Part
    ###########################

    def _process_input_lists(self) -> tuple[Iterable[int], Iterable[int]]:
        return zip(*(map(int, line.split("   ")) for line in self.lines))

    ###########################
    # DAY 01 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        first_list, second_list = self._process_input_lists()

        first_list = sorted(first_list)
        second_list = sorted(second_list)

        return sum(
            abs(second_location_id - first_location_id)
            for first_location_id, second_location_id in zip(first_list, second_list)
        )

    ###########################
    # DAY 01 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        first_list, second_list = self._process_input_lists()
        first_dict, second_dict = Counter(first_list), Counter(second_list)

        return sum(
            location_id * first_dict_nb * second_dict[location_id]
            for location_id, first_dict_nb in first_dict.items()
        )
