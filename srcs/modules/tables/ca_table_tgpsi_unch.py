import numpy as np
from scipy.interpolate import RegularGridInterpolator
import csv


class CaTableTgPsiUnCh:
    """
    Class to calculate coefficients based on water reserve, area, and tg using interpolation.
    """

    def init(self):
        self.init_base_table()

    def init_base_table(self):
        self.base_table_water_reserve = [100, 200, 300, 400, 500, 600]
        self.base_table_tg_values = [25, 30, 35, 40]
        self.base_table_area_values = [1, 2, 5, 10, 20, 30, 40, 50, 100]

        self.base_table_coefficients = np.array([
            [
                [0.424, 0.505, 0.587, 0.668],  
                [0.420, 0.501, 0.583, 0.664],  
                [0.409, 0.491, 0.572, 0.654],  
                [0.395, 0.476, 0.558, 0.639],  
                [0.372, 0.454, 0.535, 0.617],  
                [0.350, 0.431, 0.513, 0.594],  
                [0.330, 0.412, 0.493, 0.575],  
                [0.310, 0.392, 0.474, 0.556],  
                [0.290, 0.372, 0.454, 0.536],  
            ],
            [
                [0.456, 0.540, 0.623, 0.707],
                [0.452, 0.536, 0.619, 0.703],  
                [0.441, 0.524, 0.608, 0.691],  
                [0.427, 0.509, 0.592, 0.675],  
                [0.404, 0.487, 0.570, 0.653],  
                [0.382, 0.465, 0.548, 0.631],  
                [0.362, 0.445, 0.528, 0.611],  
                [0.342, 0.425, 0.508, 0.591],  
                [0.322, 0.405, 0.488, 0.571],  
            ],
        ])
        
        self.base_table_interpolator = RegularGridInterpolator(
            (self.base_table_water_reserve, self.base_table_area_values, self.base_table_tg_values),
            self.base_table_coefficients,
            method="linear",
        )

    def print(self, W: float = None, A: float = None, tg: float = None) -> None:
        """
        Prints the interpolated coefficient for given water reserve, area, and tg.
        :param W: Water reserve.
        :param A: Area.
        :param tg: tg value.
        """
        print(self.get(W, A, tg))

    def get(self, water: float = None, area: float = None, tg: float = None) -> float:
        """
        Gets the interpolated coefficient for given water reserve, area, and tg.
        :param water: Water reserve.
        :param area: Area.
        :param tg: tg value.
        :return: Interpolated coefficient.
        """
        if water is None or area is None or tg is None:
            raise ValueError("All parameters (water, area, tg) must be provided.")
        point = (water, area, tg)
        return float(self.base_table_interpolator(point))

    def save_to_csv(
        self,
        waters: list[float],
        areas: list[float],
        tgs: list[float],
        path: str,
        water_col: str = "water_reserve",
        area_col: str = "area",
        tg_col: str = "tg",
        coefficient_col: str = "coefficient",
        delimiter: str = ",",
    ) -> None:
        """
        Saves interpolated coefficients for given water reserves, areas, and tg values to a CSV file.
        :param waters: List of water reserve values.
        :param areas: List of area values.
        :param tgs: List of tg values.
        :param path: Path to save the CSV file.
        :param water_col: Name for the water reserve column.
        :param area_col: Name for the area column.
        :param tg_col: Name for the tg column.
        :param coefficient_col: Name for the coefficient column.
        :param delimiter: CSV delimiter (default is ',').
        """
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow([water_col, area_col, tg_col, coefficient_col])

            for water in waters:
                for area in areas:
                    for tg in tgs:
                        try:
                            writer.writerow([water, area, tg, self.get(water, area, tg)])
                        except ValueError:
                            continue

    def save_to_csv_with_steps(
            self,
            water0: float,
            step_water: float,
            n_water: int,
            area0: float,
            step_area: float,
            n_area: int,
            tg0: float,
            step_tg: float,
            n_tg: int,
            path: str,
            water_col: str = "water_reserve",
            area_col: str = "area",
            tg_col: str = "tg",
            coefficient_col: str = "coefficient",
            delimiter: str = ",",
        ) -> None:
            """
            Generates water reserves, areas, and tg values with steps and saves interpolated coefficients to a CSV file.
            This function uses save_to_csv internally.
            :param water0: Starting water reserve value.
            :param step_water: Step size for water reserve.
            :param n_water: Number of water reserve values to generate.
            :param area0: Starting area value.
            :param step_area: Step size for area.
            :param n_area: Number of area values to generate.
            :param tg0: Starting tg value.
            :param step_tg: Step size for tg.
            :param n_tg: Number of tg values to generate.
            :param path: Path to save the CSV file.
            :param water_col: Name for the water reserve column.
            :param area_col: Name for the area column.
            :param tg_col: Name for the tg column.
            :param coefficient_col: Name for the coefficient column.
            :param delimiter: CSV delimiter (default is ',').
            """
            if n_water <= 0 or step_water <= 0 or n_area <= 0 or step_area <= 0 or n_tg <= 0 or step_tg <= 0:
                raise ValueError("All steps and counts must be positive.")
    
            waters = [water0 + i * step_water for i in range(n_water)]
            areas = [area0 + j * step_area for j in range(n_area)]
            tgs = [tg0 + k * step_tg for k in range(n_tg)]
    
            self.save_to_csv(waters, areas, tgs, path, water_col, area_col, tg_col, coefficient_col, delimiter)