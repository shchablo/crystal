from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np
from scipy.interpolate import RegularGridInterpolator



class CaTopTgPsiUnCh:


    def __init__(self, tgPsiUnCh):
        """
        Initializes the top-level class with entry points for various actions.
        :param tgPsiUnCh (CaTopTgPsiUnCh): An instance of the core manager.
        """

        self.tgPsiUnCh = tgPsiUnCh


    def print(self, water: float = None, slope: float = None) -> None:
        """
        Display the interpolated tgPsi of a unchanneled avalanche for given water reserve and slope.

          The function ensures that the input parameters are within the predefined ranges:
            - If the water value exceeds the maximum or minimum in water_reserve, it is clamped to the nearest boundary.
            - If the slope value exceeds the maximum or minimum in slope_values, it is clamped to the nearest boundary.

          This command calculates and prints the interpolated tgPsi based on the provided tg and water reserve values.

          Options:
            --water | FLOAT | Water reserve value (default: None).
            --slope | FLOAT | slope value (default: None).

          Example:
            crystal [cmd] --slope 0.7 --water 100.0
        """

        print(self.tgPsiUnCh.get_angle(water, slope))



@dataclass
class CaTgPsiUnChCoefficientTable:
    """
    Data class to hold base tables for tg, water reserve, and coefficients.
    """

    water_reserve: List[float] = field(default_factory=lambda: [100, 200, 300, 400, 500, 600])

    slope_values: List[float] = field(default_factory=lambda: [25, 30, 35, 40])

    coefficients: List[List[float]] = field(default_factory=lambda: [
        [0.456, 0.571, 0.686, 0.801],
        [0.456, 0.571, 0.686, 0.801],
        [0.431, 0.541, 0.651, 0.761],
        [0.406, 0.511, 0.616, 0.721],
        [0.381, 0.481, 0.581, 0.681],
        [0.356, 0.451, 0.546, 0.641],
    ])



class CaTgPsiUnCh:
    """
    Class to calculate coefficients based on tg and water reserve values using interpolation.
    """


    def __init__(self):
        self.table = CaTgPsiUnChCoefficientTable()
        self.interpolator = RegularGridInterpolator(
            (self.table.water_reserve, self.table.slope_values),
            self.table.coefficients,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )


    def get_angle(self, water: float, slope: float) -> float:
        """
        Fetch the interpolated angle for the given tg and water reserve.

        The function ensures that the input parameters are within the predefined ranges:
        - If the water value exceeds the maximum or minimum in water_reserve, it is clamped to the nearest boundary.
        - If the slope value exceeds the maximum or minimum in slope_values, it is clamped to the nearest boundary.

        :param water: Water reserve value to be used in the interpolation.
        :param slope: Angle value to be used in the interpolation (slope).

        :return: Interpolated coefficient for the given slope and water reserve.
        """

        if slope is None or water is None:
            raise ValueError("Both 'slope' and 'water' must be provided.")

        # Clamp values to the nearest range
        water = max(min(water, max(self.table.water_reserve)), min(self.table.water_reserve))
        slope = max(min(slope, max(self.table.slope_values)), min(self.table.slope_values))

        return float(self.interpolator((water, slope)))