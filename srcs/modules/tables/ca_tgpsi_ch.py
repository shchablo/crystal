
from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np
from scipy.interpolate import RegularGridInterpolator


@dataclass
class CaTgPsiChCoefficientTable:
    """
    Data class to hold base tables for tg, water reserve, and coefficients.
    """
    water_reserve: List[float] = field(default_factory=lambda: [100, 200, 300, 400, 500, 600])
    tg_values: List[float] = field(default_factory=lambda: [25, 30, 35, 40])
    coefficients: List[List[float]] = field(default_factory=lambda: [
        [0.456, 0.571, 0.686, 0.801],
        [0.456, 0.571, 0.686, 0.801],
        [0.431, 0.541, 0.651, 0.761],
        [0.406, 0.511, 0.616, 0.721],
        [0.381, 0.481, 0.581, 0.681],
        [0.356, 0.451, 0.546, 0.641],
    ])


class CaTgPsiCh:
    """
    Class to calculate coefficients based on tg and water reserve values using interpolation.
    """

    def __init__(self):
        self.table = CaTgPsiChCoefficientTable()
        self.interpolator = RegularGridInterpolator(
            (self.table.water_reserve, self.table.tg_values),
            self.table.coefficients,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )

    def get_coefficient(self, tg: float, water_reserve: float) -> float:
        """
        Fetch the interpolated coefficient for the given tg and water reserve.

        :param tg: tg value.
        :param water_reserve: Water reserve value.
        
        :return: Interpolated coefficient for the given tg and water reserve.
        """
        if tg is None or water_reserve is None:
            raise ValueError("Both 'tg' and 'water_reserve' must be provided.")
        return float(self.interpolator((water_reserve, tg)))

    def generate_table(self, tgs: List[float], waters: List[float]) -> List[Tuple[float, float, float]]:
        """
        Generate a table of tg, water reserve values, and corresponding coefficients.
        
        :param tgs: List of tg values.
        :param waters: List of water reserve values.
        
        :return: List of tuples (tg, water_reserve, coefficient).
        """
        return [
            (tg, water, self.get_coefficient(tg, water))
            for water in waters
            for tg in tgs
        ]

    def print(self, tg: float = None, w: float = None) -> None:
        """
        Print the interpolated coefficient for the given tg and water reserve.
        
        :param tg: tg value.
        :param w: Water reserve value.
        """
        print(self.get_coefficient(tg, w))