import csv

from srcs.modules.common.ca_common import ca_add_common_doc


class CaTableKf:
    """
    Class to calculate the kF coefficient based on snow height and avalanche area
    without repeating data in the table.
    """

    def __init__(self):
        # Independent height ranges
        self.height_ranges = [
            (-float("inf"), 0.2),
            (0.2, 0.4),
            (0.4, 0.6),
            (0.6, 1.0),
            (1.0, 1.5),
            (1.5, 2.0),
            (2.0, float("inf"))
        ]

        # Independent area ranges
        self.area_ranges = [
            (-float("inf"), 5),
            (5, 10),
            (10, 20),
            (20, 40),
            (40, float("inf"))
        ]

        # Coefficients matrix for each combination of height and area ranges
        self.coefficients = {
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
        }

    _kf_doc = """
        :param h: Snow height in meters.
        :param area: Avalanche area in hectares.
        :param atype: Avalanche type ('dry' or 'wet').
        :return: The corresponding kF coefficient.
    """

    @ca_add_common_doc(_kf_doc)
    def get(self, h: float, area: float, atype: str = "dry") -> float:
        if atype not in self.coefficients:
            raise ValueError("Invalid avalanche type. Use 'dry' or 'wet'.")

        height_index = next((i for i, (low, high) in enumerate(self.height_ranges) if low <= h < high), None)
        if height_index is None:
            raise ValueError("Snow height out of range.")

        area_index = next((i for i, (low, high) in enumerate(self.area_ranges) if low <= area < high), None)
        if area_index is None:
            raise ValueError("Avalanche area out of range.")

        return self.coefficients[atype][height_index][area_index]

    @ca_add_common_doc(_kf_doc)
    def print(self, h: float, area: float, atype: str = "dry") -> None:
        print(self.get(h, area, atype))

    def save_to_csv(
        self,
        hs: list[float],
        areas: list[float],
        path: str,
        atype: str = "dry",
        height_col: str = "height",
        area_col: str = "area",
        coefficient_col: str = "kF",
        delimiter: str = ",",
    ) -> None:
        """
        Saves kF coefficients for given snow heights and areas to a CSV file.
        :param hs: List of snow heights in meters.
        :param areas: List of avalanche areas in hectares.
        :param path: Path to save the CSV file.
        :param atype: Avalanche type ('dry' or 'wet').
        :param height_col: Name for the height column.
        :param area_col: Name for the area column.
        :param coefficient_col: Name for the coefficient column.
        :param delimiter: CSV delimiter (default is ',').
        """
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow([height_col, area_col, coefficient_col])

            for h in hs:
                for area in areas:
                    try:
                        writer.writerow([h, area, self.get(h, area, atype)])
                    except ValueError:
                        continue
    def save_to_csv_with_steps(
            self,
            h0: float,
            step_h: float,
            n_h: int,
            area0: float,
            step_a: float,
            n_a: int,
            path: str,
            atype: str = "dry",
            height_col: str = "height",
            area_col: str = "area",
            coefficient_col: str = "kF",
            delimiter: str = ",",
        ) -> None:
            """
            Generates snow heights and areas with steps and saves kF coefficients to a CSV file.
            This function uses save_to_csv internally.
            :param h0: Starting height in meters.
            :param step_h: Step size for height in meters.
            :param n_h: Number of heights to generate.
            :param area0: Starting area in hectares.
            :param step_a: Step size for area in hectares.
            :param n_a: Number of areas to generate.
            :param path: Path to save the CSV file.
            :param atype: Avalanche type ('dry' or 'wet').
            :param height_col: Name for the height column.
            :param area_col: Name for the area column.
            :param coefficient_col: Name for the coefficient column.
            :param delimiter: CSV delimiter (default is ',').
            """
            if n_h <= 0 or step_h <= 0 or n_a <= 0 or step_a <= 0:
                raise ValueError("Number of heights, areas, and steps must be positive.")

            heights = [h0 + i * step_h for i in range(n_h)]
            areas = [area0 + j * step_a for j in range(n_a)]

            self.save_to_csv(heights, areas, path, atype, height_col, area_col, coefficient_col, delimiter)