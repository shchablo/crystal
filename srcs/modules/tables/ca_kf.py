from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class CaKfCoefficientTable:
    """
    Data class to hold ranges and coefficients for avalanche types.
    """
    height_zero_ranges: List[Tuple[float, float]] = field(default_factory=lambda: [
        (-float("inf"), 0.2),
        (0.2, 0.4),
        (0.4, 0.6),
        (0.6, 1.0),
        (1.0, 1.5),
        (1.5, 2.0),
        (2.0, float("inf")),
    ])
    area_ranges: List[Tuple[float, float]] = field(default_factory=lambda: [
        (-float("inf"), 5),
        (5, 10),
        (10, 20),
        (20, 40),
        (40, float("inf")),
    ])
    coefficients: dict = field(default_factory=lambda: {
        "dry": [
            [0.15, 0.12, 0.10, 0.07, 0.05],
            [0.30, 0.25, 0.20, 0.15, 0.10],
            [0.40, 0.35, 0.30, 0.20, 0.15],
            [0.60, 0.50, 0.40, 0.30, 0.20],
            [0.70, 0.60, 0.50, 0.40, 0.30],
            [0.80, 0.70, 0.60, 0.50, 0.40],
            [0.80, 0.70, 0.60, 0.50, 0.50],
        ],
        "wet": [
            [0.15, 0.12, 0.10, 0.07, 0.05],
            [0.30, 0.25, 0.20, 0.15, 0.10],
            [0.40, 0.35, 0.30, 0.17, 0.12],
            [0.50, 0.40, 0.30, 0.20, 0.15],
            [0.60, 0.50, 0.40, 0.30, 0.20],
            [0.70, 0.60, 0.50, 0.40, 0.30],
            [0.70, 0.60, 0.50, 0.40, 0.40],
        ]
    })


class CaKf:
    """
    Class to calculate and manage kF coefficients based on snow height zero, area and avalanche area.
    """

    def __init__(self):
        self.table = CaKfCoefficientTable()

    def _get_range_index(self, value: float, ranges: List[Tuple[float, float]]) -> int:
        """
        Get the index of the range to which the value belongs.
        """
        for i, (low, high) in enumerate(ranges):
            if low <= value < high:
                return i
        raise ValueError(f"Value {value} out of range.")

    def get_coefficient(self, height_zero: float, area: float, avalanche_type: str) -> float:
        """

        Fetch kF coefficient for a specific height and area.

        :param height_zero: Snow height zero in meters.
        :param area: Avalanche area in hectares.
        :param avalanche_type: Avalanche type ('dry' or 'wet').

        :return: Corresponding kF coefficient for the given height and area.

        """
        if avalanche_type not in self.table.coefficients:
            raise ValueError("Invalid avalanche type. Use 'dry' or 'wet'.")

        height_index = self._get_range_index(height_zero, self.table.height_zero_ranges)
        area_index = self._get_range_index(area, self.table.area_ranges)
        return self.table.coefficients[avalanche_type][height_index][area_index]

    def generate_table(self, heights_zero: List[float], areas: List[float], avalanche_type: str = "dry") -> List[Tuple[float, float, float]]:
        """

        Generates a table of heights, areas, and corresponding kF coefficients.

        :param heights_zero: List of snow heights zero in meters.
        :param areas: List of avalanche areas in hectares.
        :param avalanche_type: Avalanche type ('dry' or 'wet'). default: dry.

        :return: List of tuples (height, area, kF coefficient).

        """
        return [
            (h, area, self.get_coefficient(h, area, avalanche_type))
            for h in heights_zero
            for area in areas
        ]

    def print(self, h0: float = None, a: float = None, atype: str = "dry") -> None:
        """
        Display the coefficient for a given height, area, and avalanche type.

          This command calculates and prints the coefficient based on the provided snow height, avalanche area, and type.

          Options:
            --h0    | FLOAT | Snow height zero in meters (default: None).
            --a     | FLOAT | Avalanche area in hectares (default: None).
            --atype | TEXT  | Avalanche type 'dry' or 'wet' (default: 'dry').

          Example:
            crystal [cmd] --h0 3.5 --a 15
            crystal [cmd] --h0 2.0 --a 10 --atype wet

        """
        print(self.get_coefficient(h0, a, atype))