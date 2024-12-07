from dataclasses import dataclass
from itertools import combinations

from scripts.utils import AbstractPuzzleSolver


class PuzzleSolver(AbstractPuzzleSolver):
    # Input data
    page_ordering_rules: set[tuple[int, int]]

    # Computed data
    valid_pages: list["PageList"]
    invalid_pages: list["PageList"]

    ###########################
    # DAY 05 - Common Part
    ###########################

    def solve(self) -> tuple[int, int]:
        """Common part includes pages retrieval and separation into valid/invalid"""

        # Retrieve input data
        self.page_ordering_rules, pages_to_produce = self._retrieve_pages_data()

        # Separate valid pages and invalid pages
        self._compute_pages_validity(pages_to_produce)

        # Solve both parts
        return super().solve()

    def _retrieve_pages_data(self) -> list["PageList"]:
        lines_iter = iter(self.lines)
        page_ordering_rules, pages_to_produce = set(), []

        # First part of input contains page ordering rules, ends with empty line
        while (current_line := next(lines_iter)) != "":
            page_ordering_rules.add(tuple(map(int, current_line.split("|"))))

        # Last part contains the pages to produce
        try:
            while current_line := next(lines_iter):
                pages_to_produce.append(PageList.from_line(line=current_line))
        except StopIteration:
            pass

        return page_ordering_rules, pages_to_produce

    def _compute_pages_validity(self, pages_to_produce: list["PageList"]) -> None:
        """Compute pages validity only once for both parts of the puzzle"""
        self.valid_pages, self.invalid_pages = [], []
        for page_list in pages_to_produce:
            choosen_list = (
                self.valid_pages
                if page_list.is_order_valid(ordering_rules=self.page_ordering_rules)
                else self.invalid_pages
            )
            choosen_list.append(page_list)

    ###########################
    # DAY 05 - First Part
    ###########################

    def _solve_first_part(self) -> int:
        """Just return the sum of middle pages of valid pages"""
        return sum(page_list.middle_page for page_list in self.valid_pages)

    ###########################
    # DAY 05 - Second Part
    ###########################

    def _solve_second_part(self) -> int:
        return sum(
            valid_page_list.middle_page
            for page_list in self.invalid_pages
            if (valid_page_list := self._get_valid_page_ordering(page_list))
        )

    def _get_valid_page_ordering(self, page_list: "PageList") -> "PageList":
        """Find out valid page ordering of a given page"""

        # Iterate over the combinations and invert number from first one
        # until there is no more invalid combination remaining
        while invalid_combinations := page_list.invalid_combinations(
            self.page_ordering_rules
        ):
            # Retrieve the next combination
            combination = next(iter(invalid_combinations))

            # Get indexes of both values
            first, second = (
                page_list.index(combination[0]),
                page_list.index(combination[1]),
            )

            # Invert both elements
            page_list[first], page_list[second] = page_list[second], page_list[first]

        return page_list


@dataclass
class PageList:
    pages: list[int]

    @classmethod
    def from_line(cls, line: str) -> "PageList":
        return cls(pages=list(map(int, line.split(","))))

    @property
    def middle_page(self) -> int:
        middle_indice = int(len(self.pages) / 2)
        return self[middle_indice]

    @property
    def orders_combinations(self) -> set[tuple[int, int]]:
        return set(combinations(self.pages, 2))

    def invalid_combinations(
        self, ordering_rules: set[tuple[int, int]]
    ) -> set[tuple[int, int]]:
        return self.orders_combinations - ordering_rules

    def is_order_valid(self, ordering_rules: set[tuple[int, int]]) -> bool:
        return self.invalid_combinations(ordering_rules) == set()

    def index(self, index: int) -> int:
        return self.pages.index(index)

    def __getitem__(self, index: int) -> int:
        return self.pages[index]

    def __setitem__(self, index: int, element: int) -> None:
        self.pages[index] = element
