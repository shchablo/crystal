
from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class CaKhCoefficientTable:
    """
    Data class to hold ranges and coefficients for avalanche types.
    """
    height_ranges: List[Tuple[float, float]] = field(default_factory=lambda: [
        (-float("inf"), 0.3),
        (0.3, 0.4),
        (0.4, 0.6),
        (0.6, 0.8),
        (0.8, 1.0),
        (1.0, 1.5),
        (1.5, 2.0),
        (2.0, float("inf")),
    ])
    coefficients: dict = field(default_factory=lambda: {
        "dry": [0.6, 0.5, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4],
        "wet": [0.8, 0.7, 0.6, 0.6, 0.6, 0.6, 0.5, 0.4],
    })


class CaKh:
    """
    Class to calculate and manage kH coefficients based on snow height and avalanche type.
    """

    def __init__(self):
        self.table = CaKhCoefficientTable()

    def _is_valid_height(self, height: float) -> bool:
        """
        Check if the height is within a valid range.
        """
        return any(low <= height < high for low, high in self.table.height_ranges)

    def _get_range_index(self, height: float) -> int:
        """
        Get the index of the range to which the height belongs.
        """
        for i, (low, high) in enumerate(self.table.height_ranges):
            if low <= height < high:
                return i
        raise ValueError("Snow height out of range.")

    def get_coefficient(self, height: float, avalanche_type: str) -> float:
        """

        Fetch kH coefficient for a specific height and type.

        :param height: Snow height in meters.
        :param avalanche_type: Avalanche type ('dry' or 'wet').

        :return: Corresponding kH coefficient for the given height and type.

        """
        if avalanche_type not in self.table.coefficients:
            raise ValueError("Invalid type. Use 'dry' or 'wet'.")
        index = self._get_range_index(height)
        return self.table.coefficients[avalanche_type][index]

    def generate_table(self, heights: List[float], avalanche_type: str = "dry") -> List[Tuple[float, float]]:
        """

        Generates a table of heights and corresponding kH coefficients.

        :param heights: List of snow heights in meters.
        :param avalanche_type: Avalanche type ('dry' or 'wet').

        :return: List of tuples (height, kH coefficient).

        """
        return [
            (h, self.get_coefficient(h, avalanche_type))
            for h in heights
            if self._is_valid_height(h)
        ]

    def print(self, h: float = None, atype: str = "dry") -> None:
        """

        Print the oefficient for a given height and type.

        :param h: Snow height in meters.
        :param atype: Avalanche type ('dry' or 'wet').

        """
        print(self.get_coefficient(h, atype))