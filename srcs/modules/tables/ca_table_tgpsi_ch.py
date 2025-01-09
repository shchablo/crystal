import numpy as np
from scipy.interpolate import RegularGridInterpolator
import csv


class CaTableTgPsiCh:
    """
    Class to calculate coefficients based on tg and water reserve values using interpolation.
    """

    def init(self):
        self.init_base_table()

    def init_base_table(self):
        self.base_table_water_reserve = [100, 200, 300, 400, 500, 600]
        self.base_table_tg_values = [25, 30, 35, 40]
        self.base_table_coefficients = [
            [0.456, 0.571, 0.686, 0.801],
            [0.456, 0.571, 0.686, 0.801],
            [0.431, 0.541, 0.651, 0.761],
            [0.406, 0.511, 0.616, 0.721],
            [0.381, 0.481, 0.581, 0.681],
            [0.356, 0.451, 0.546, 0.641],
        ]

        self.base_table_interpolator = RegularGridInterpolator(
            (self.base_table_water_reserve, self.base_table_tg_values),
            self.base_table_coefficients,
            method="linear",
            bounds_error=False,
            fill_value=None,
        )

    def print(self, tg: float = None, W: float = None) -> None:
        """
        Prints the interpolated coefficient for given tg and water reserve.
        :param tg: tg value.
        :param W: Water reserve value.
        """
        print(self.get(tg, W))

    def get(self, tg: float = None, water_reserve: float = None) -> float:
        """
        Gets the interpolated coefficient for given tg and water reserve.
        :param tg: tg value.
        :param water_reserve: Water reserve value.
        :return: Interpolated coefficient.
        """
        if tg is None or water_reserve is None:
            raise ValueError("Both 'tg' and 'water_reserve' must be provided.")
        return float(self.base_table_interpolator((water_reserve, tg)))

    def save_to_csv(
        self,
        tgs: list[float],
        waters: list[float],
        path: str,
        tg_col: str = "tg",
        water_col: str = "water_reserve",
        coefficient_col: str = "coefficient",
        delimiter: str = ",",
    ) -> None:
        """
        Saves interpolated coefficients for given tg and water reserve values to a CSV file.
        :param tgs: List of tg values.
        :param waters: List of water reserve values.
        :param path: Path to save the CSV file.
        :param tg_col: Name for the tg column.
        :param water_col: Name for the water reserve column.
        :param coefficient_col: Name for the coefficient column.
        :param delimiter: CSV delimiter (default is ',').
        """
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow([tg_col, water_col, coefficient_col])

            for water in waters:
                for tg in tgs:
                    try:
                        writer.writerow([tg, water, self.get(tg, water)])
                    except ValueError:
                        continue

    def save_to_csv_with_steps(
        self,
        tg0: float,
        step_tg: float,
        n_tg: int,
        water0: float,
        step_water: float,
        n_water: int,
        path: str,
        tg_col: str = "tg",
        water_col: str = "water_reserve",
        coefficient_col: str = "coefficient",
        delimiter: str = ",",
    ) -> None:
        """
        Generates tg and water reserve values with steps and saves interpolated coefficients to a CSV file.
        This function uses save_to_csv internally.
        :param tg0: Starting tg value.
        :param step_tg: Step size for tg.
        :param n_tg: Number of tg values to generate.
        :param water0: Starting water reserve value.
        :param step_water: Step size for water reserve.
        :param n_water: Number of water reserve values to generate.
        :param path: Path to save the CSV file.
        :param tg_col: Name for the tg column.
        :param water_col: Name for the water reserve column.
        :param coefficient_col: Name for the coefficient column.
        :param delimiter: CSV delimiter (default is ',').
        """
        if n_tg <= 0 or step_tg <= 0 or n_water <= 0 or step_water <= 0:
            raise ValueError("Number of tg values, water reserve values, and steps must be positive.")

        tgs = [tg0 + i * step_tg for i in range(n_tg)]
        waters = [water0 + j * step_water for j in range(n_water)]

        self.save_to_csv(tgs, waters, path, tg_col, water_col, coefficient_col, delimiter)