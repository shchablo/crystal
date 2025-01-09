import csv

from srcs.modules.common.ca_common import ca_add_common_doc


class CaTableKh:
    """
    Class to calculate and manage kH coefficients based on snow height and avalanche type.
    """

    def __init__(self):
        self.height_ranges = [
            (-float("inf"), 0.3),
            (0.3, 0.4),
            (0.4, 0.6),
            (0.6, 0.8),
            (0.8, 1.0),
            (1.0, 1.5),
            (1.5, 2.0),
            (2.0, float("inf")),
        ]
        self.coefficients = {
            "dry": [0.6, 0.5, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4],
            "wet": [0.8, 0.7, 0.6, 0.6, 0.6, 0.6, 0.5, 0.4],
        }

    @ca_add_common_doc("""
        :param h: Snow height in meters.
        :param avalanche_type: Avalanche type ('dry' or 'wet').
        :return: Corresponding kH coefficient.
    """)
    def get(self, height: float, avalanche_type: str = "dry") -> float:
        if avalanche_type not in self.coefficients:
            raise ValueError("Invalid type. Use 'dry' or 'wet'.")
        for i, (low, high) in enumerate(self.height_ranges):
            if low <= height < high:
                return self.coefficients[avalanche_type][i]
        raise ValueError("Snow height out of range.")

    @ca_add_common_doc("""
        Prints the kH coefficient for the given height and type.
        :param h: Snow height in meters.
        :param atype: Avalanche type ('dry' or 'wet').
    """)
    def print(self, h: float, atype: str = "dry") -> None:
        print(self.get(h, atype))

    def save_to_csv(
        self,
        hs: list[float],
        path: str,
        atype: str = "dry",
        height_col: str = "height",
        coefficient_col: str = "kH",
        delimiter: str = ",",
    ) -> None:
        """
        Saves kH coefficients for given snow heights to a CSV file.
        :param hs: List of snow heights in meters.
        :param path: Path to save the CSV file.
        :param atype: Avalanche type ('dry' or 'wet').
        :param height_col: Name for the height column.
        :param coefficient_col: Name for the coefficient column.
        :param delimiter: CSV delimiter (default is ',').
        """
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow([height_col, coefficient_col])
            for h in hs:
                try:
                    writer.writerow([h, self.get(h, atype)])
                except ValueError:
                    continue

    def save_to_csv_with_steps(
        self,
        h0: float,
        step_h: float,
        n_h: int,
        path: str,
        atype: str = "dry",
        height_col: str = "height",
        coefficient_col: str = "kH",
        delimiter: str = ",",
    ) -> None:
        """
        Generates heights based on step and saves corresponding kH coefficients to a CSV file.
        :param h0: Starting height in meters.
        :param step_h: Step size in meters.
        :param n_h: Number of heights to generate.
        :param path: Path to save the CSV file.
        :param atype: Avalanche type ('dry' or 'wet').
        :param height_col: Name for the height column.
        :param coefficient_col: Name for the coefficient column.
        :param delimiter: CSV delimiter (default is ',').
        """
        if n_h <= 0 or step_h <= 0:
            raise ValueError("Number of heights and step must be positive.")
        hs = [h0 + i * step_h for i in range(n_h)]
        self.save_to_csv(hs, path, atype, height_col, atype + "_" + coefficient_col, delimiter)