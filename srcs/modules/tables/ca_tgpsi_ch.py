from dataclasses import dataclass, field
from typing import List, Tuple
import numpy as np
from scipy.interpolate import RegularGridInterpolator



class CaTopTgPsiCh:


    def __init__(self, tgPsiCh):
        """
        Initializes the top-level class with entry points for various actions.
        
        :param tgPsiCh (CaTopTgPsiCh): An instance of the core manager.
        """
        
        self.tgPsiCh = tgPsiCh


    def print(self, w: float = None, tg: float = None, a: float = None) -> None:
        """
        Display the interpolated tgPsi of a channeled avalanche for given water reserve, area, and tg.

          The function ensures that the input parameters are within the predefined ranges:
            - If the water value exceeds the maximum or minimum in water_reserve, it is clamped to the nearest boundary.
            - If the area value exceeds the maximum or minimum in area_values, it is clamped to the nearest boundary.
            - If the slope tg value exceeds the maximum or minimum in tg_values, it is clamped to the nearest boundary.

          This command calculates and prints the interpolated tgPsi based on the provided water reserve, area, and tg values.

          Options:
            --w  | FLOAT | Water reserve value (default: None).
            --a  | FLOAT | Area value (default: None).
            --tg | FLOAT | slope tg value (default: None).

          Example:
            crystal [cmd] --w 150.0 --a 20.0 --tg 0.5
        """
        
        print(self.tgPsiCh.get_angle(w, tg, a))



@dataclass
class CaTgPsiChCoefficientTable:
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


class CaTgPsiCh:
    """
    Class to calculate coefficients based on water reserve, area, and tg values using interpolation.
    """


    def __init__(self):
        
        self.table = CaTgPsiChCoefficientTable()
        self.interpolator = RegularGridInterpolator(
            (self.table.water_reserve, self.table.area_values, self.table.tg_values),
            self.table.coefficients,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )


    def get_angle(self, water: float, tg: float, area: float) -> float:
        """
        Fetch the interpolated angle for the given water reserve, area, and tg values.

        The function ensures that the input parameters are within the predefined ranges:
        - If the water value exceeds the maximum or minimum in water_reserve, it is clamped to the nearest boundary.
        - If the area value exceeds the maximum or minimum in area_values, it is clamped to the nearest boundary.
        - If the tg value exceeds the maximum or minimum in tg_values, it is clamped to the nearest boundary.

        :param water: Water reserve value to be used in the interpolation.
        :param area: Area value to be used in the interpolation.
        :param tg: Slope angle value to be used in the interpolation.

        :return: Interpolated angle for the provided inputs.

        :raises ValueError: If any of the input parameters (water, area, or tg) is not provided.
        """

        if water is None or area is None or tg is None:
            raise ValueError("All parameters (water, area, tg) must be provided.")

        # Clamp values to the nearest range
        water = max(min(water, max(self.table.water_reserve)), min(self.table.water_reserve))
        area = max(min(area, max(self.table.area_values)), min(self.table.area_values))
        tg = max(min(tg, max(self.table.tg_values)), min(self.table.tg_values))

        return float(self.interpolator((water, area, tg)))