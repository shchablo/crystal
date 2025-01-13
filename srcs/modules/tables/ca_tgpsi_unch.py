from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np
from scipy.interpolate import RegularGridInterpolator


@dataclass
class CaTgPsiUnChCoefficientTable:
    """
    Data class to hold base tables for water reserve, area, tg values, and coefficients.
    """
    water_reserve: List[float] = field(default_factory=lambda: [100, 200, 300, 400, 500, 600])
    area_values: List[float] = field(default_factory=lambda: [1, 2, 5, 10, 20, 30, 40, 50, 100])
    tg_values: List[float] = field(default_factory=lambda: [25, 30, 35, 40])
    coefficients: np.ndarray = field(default_factory=lambda: np.array([
        [
            [0.424, 0.505, 0.587, 0.668],
            [0.420, 0.501, 0.583, 0.664],
            [0.409, 0.491, 0.572, 0.654],
            [0.395, 0.476, 0.558, 0.639],
            [0.372, 0.454, 0.535, 0.617],
            [0.358, 0.439, 0.521, 0.602],
            [0.348, 0.429, 0.511, 0.592],
            [0.344, 0.425, 0.507, 0.588],
            [0.329, 0.411, 0.492, 0.574],
        ],
        [
            [0.389, 0.464, 0.539, 0.614],
            [0.384, 0.459, 0.534, 0.609],
            [0.369, 0.444, 0.519, 0.594],
            [0.349, 0.424, 0.499, 0.574],
            [0.321, 0.396, 0.471, 0.546],
            [0.303, 0.378, 0.453, 0.528],
            [0.293, 0.368, 0.443, 0.518],
            [0.286, 0.361, 0.436, 0.511],
            [0.276, 0.351, 0.426, 0.501],
        ],
        [
            [0.379, 0.454, 0.529, 0.604],
            [0.373, 0.448, 0.523, 0.598],
            [0.358, 0.433, 0.508, 0.583],
            [0.337, 0.412, 0.487, 0.562],
            [0.308, 0.383, 0.458, 0.533],
            [0.291, 0.366, 0.441, 0.516],
            [0.281, 0.356, 0.431, 0.506],
            [0.274, 0.349, 0.424, 0.499],
            [0.266, 0.341, 0.416, 0.491],
        ],
        [
            [0.353, 0.423, 0.493, 0.563],
            [0.347, 0.417, 0.487, 0.557],
            [0.330, 0.400, 0.470, 0.540],
            [0.307, 0.377, 0.447, 0.517],
            [0.275, 0.345, 0.415, 0.485],
            [0.257, 0.327, 0.397, 0.467],
            [0.246, 0.316, 0.386, 0.456],
            [0.239, 0.309, 0.379, 0.449],
            [0.231, 0.301, 0.371, 0.441],
        ],
        [
            [0.343, 0.413, 0.483, 0.553],
            [0.337, 0.407, 0.477, 0.547],
            [0.319, 0.389, 0.459, 0.529],
            [0.296, 0.366, 0.436, 0.506],
            [0.264, 0.334, 0.404, 0.474],
            [0.246, 0.316, 0.386, 0.456],
            [0.235, 0.305, 0.375, 0.445],
            [0.229, 0.299, 0.369, 0.439],
            [0.221, 0.291, 0.361, 0.431],
        ],
        [
            [0.343, 0.413, 0.483, 0.553],
            [0.336, 0.406, 0.476, 0.546],
            [0.319, 0.389, 0.459, 0.529],
            [0.295, 0.365, 0.435, 0.505],
            [0.263, 0.333, 0.403, 0.473],
            [0.245, 0.315, 0.385, 0.455],
            [0.234, 0.304, 0.374, 0.444],
            [0.228, 0.298, 0.368, 0.438],
            [0.221, 0.291, 0.361, 0.431],
        ],
    ]))


class CaTgPsiUnCh:
    """
    Class to calculate coefficients based on water reserve, area, and tg values using interpolation.
    """

    def __init__(self):
        self.table = CaTgPsiUnChCoefficientTable()
        self.interpolator = RegularGridInterpolator(
            (self.table.water_reserve, self.table.area_values, self.table.tg_values),
            self.table.coefficients,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )

    def get_coefficient(self, water: float, area: float, tg: float) -> float:
        """
        Fetch the interpolated coefficient for the given water reserve, area, and tg.
        
        :param water: Water reserve value.
        :param area: Area value.
        :param tg: tg value.
        
        :return: Interpolated coefficient.
        """
        if water is None or area is None or tg is None:
            raise ValueError("All parameters (water, area, tg) must be provided.")
        return float(self.interpolator((water, area, tg)))

    def generate_table(
        self, waters: List[float], areas: List[float], tgs: List[float]
    ) -> List[Tuple[float, float, float, float]]:
        """
        Generate a table of water reserve, area, tg values, and corresponding coefficients.
        
        :param waters: List of water reserve values.
        :param areas: List of area values.
        :param tgs: List of tg values.
        
        :return: List of tuples (water_reserve, area, tg, coefficient).
        """
        return [
            (water, area, tg, self.get_coefficient(water, area, tg))
            for water in waters
            for area in areas
            for tg in tgs
        ]
    
    def print(self, w: float = None, a: float = None, tg: float = None) -> None:
        """
        Print the interpolated coefficient for the given water reserve, area, and tg.
        
        :param w: Water reserve value.
        :param a: Area value.
        :param tg: tg value.
        """
        print(self.get_coefficient(w, a, tg))