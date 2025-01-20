import pandas as pd
from shapely.geometry import LineString, Point, MultiPoint
import math

class CaTopCalculator:

    def __init__(self, core, calculator):
        """

        Initializes the top-level class with entry points for various actions.

        :param core (CaCore): An instance of the core manager.
        :param handler (CaCalculator): An instance of the handler manager.

        """
        self.core = core
        self.calculator = calculator


    def process_inputs(self, verbose: str = "y") -> None:

        self.calculator.handler.inputs['tg_psi'] = self.calculator.handler.inputs.apply(self.calculator.calculate_input_tg, axis=1)
        self.calculator.handler.inputs['volume'] = self.calculator.handler.inputs.apply(self.calculator.calculate_input_v, axis=1)

        if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:
            print("Input data has been processed.")

        return

    def process_profiles(self, verbose: str = "y") -> None:

        isVerbose = verbose.strip().lower() in {"1", "y", "yes", "true"}

        if isVerbose:
            print("Processing profiles...")

        for key, df in self.calculator.handler.profiles.items():

            atype = self.calculator.find_in_inputs(key, "type")
            tgpsi = self.calculator.find_in_inputs(key, "tg_psi")
            pa = self.calculator.find_in_inputs(key, "p_a")
            volume = self.calculator.find_in_inputs(key, "volume")
            hi = self.calculator.find_in_inputs(key, "hi")
            try:
                hi = float(hi)
            except (ValueError, TypeError):
                hi = None

            try:
                first_index = df[df["h"] != 0].index[0]
                h0 = df.loc[first_index, "h"]
            except (KeyError, IndexError, ValueError, TypeError):
                h0 = None

            df["tg"] = df.apply(lambda row: self.calculator.calculate_profile_tg(row, df), axis=1)
            df["rad"] = df.apply(self.calculator.calculate_profile_atan, axis=1)
            df["deg"] = df.apply(self.calculator.calculate_profile_deg, axis=1)
            df["tg_psi"] = tgpsi
            df["estim_1"] = df.apply(self.calculator.calculate_profile_estim_1, axis=1)
            df["h_sec"] = df.apply(lambda row: self.calculator.calculate_profile_hsec(row, h0), axis=1)
            df["estim_2"] = df.apply(self.calculator.calculate_profile_estim_2, axis=1)
            df["velocity"] = df.apply(self.calculator.calculate_profile_v, axis=1)
            df["p_a"] = pa
            df["P"] = df.apply(self.calculator.calculate_profile_P, axis=1)
            df["P_peak"] = df.apply(self.calculator.calculate_profile_Ppeak, axis=1)

            if (self.calculator._isCh(atype)) == True:
                df["h_front"] = df.apply(lambda row: self.calculator.calculate_profile_hfront_ch(row, volume), axis=1)
            elif (self.calculator._isCh(atype)) == False:
                df["h_front"] = 3 * hi

        if isVerbose:
            print("All profiles have been processed.")

        return

    def process_objects(self, verbose: str = "y") -> None:

        isVerbose = verbose.strip().lower() in {"1", "y", "yes", "true"}

        if isVerbose:
            print("Processing objects...")


        for key, df in self.calculator.handler.profiles.items():
            matching_objects = self.calculator.handler.objects.loc[
                self.calculator.handler.objects['name'].astype(str) == str(key)
            ]

            if not matching_objects.empty:
                for idx, obj_row in matching_objects.iterrows():
                    dist_value = obj_row['dist']

                    closest_row = df.iloc[(df['l'] - dist_value).abs().idxmin()]

                    self.calculator.handler.objects.loc[idx, 'velocity'] = closest_row['velocity']
                    self.calculator.handler.objects.loc[idx, 'P'] = closest_row['P']
                    self.calculator.handler.objects.loc[idx, 'P_peak'] = closest_row['P_peak']
                    self.calculator.handler.objects.loc[idx, 'h_front'] = closest_row['h_front']
                    self.calculator.handler.objects.loc[idx, 'L'] = self.calculator.find_intersection(df)

        if isVerbose:
            print("All objects have been processed.")


class CaCalculator:
    def __init__(self, handler, kh, kf, tgpsi_ch, tgpsi_unch):

        self.handler = handler

        self.kh = kh
        self.kf = kf
        self.tgpsi_ch = tgpsi_ch
        self.tgpsi_unch = tgpsi_unch


    def find_in_inputs(self, key, param):
        try:
            result = self.handler.inputs.loc[self.handler.inputs['name'].astype(str) == str(key), str(param)]
            result = result.values[0] if not result.empty else None
            return result
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_input_v(self, row):
        try:
            h0 = float(row["hi"]) * self.kh.get_coefficient(float(row["hi"]), str(row["cat"]))
            kf = self.kf.get_coefficient(h0, float(row["area"]), str(row["cat"]))
            return h0 * kf * float(row["area"]) * 10
        except (KeyError, IndexError, ValueError, TypeError):
            return None

    def _isCh(self, atype: str = None):
        atype = str(atype).strip().lower()
        if atype in {"1", "lotok", "ch", "channaled", "l", "channal"}:
            return True
        elif atype in {"0", "ostov", "unch", "unchannaled", "o", "unchannal"}:
            return False
        else:
            return None

    def calculate_input_tg(self, row):
        try:

            if self._isCh(row['type']) == True:
                return self.tgpsi_ch.get_angle(
                    float(row["W"]),
                    float(row["slope"]),
                    float(row["area"])
                )
            elif self._isCh(row['type']) == False:
                return self.tgpsi_unch.get_angle(
                    float(row["W"]),
                    float(row["slope"])
                )
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_tg(self, row, df):
        try:
            current_index = row.name
            next_index = current_index + 1

            if next_index >= len(df):
                return None

            x1 = float(row["l"])
            x2 = float(df.loc[next_index, "l"])
            y1 = float(row["h"])
            y2 = float(df.loc[next_index, "h"])

            if x2 == x1:
                raise ValueError("Division by zero: x2 and x1 are equal.")

            return (y1 - y2) / (x2 - x1)
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_atan(self, row):
        try:
            return math.atan(row["tg"])
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_deg(self, row):
        try:
            return math.degrees(row["rad"])
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_estim_1(self, row):
        try:
            return float(row["l"]) * float(row["tg_psi"])
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_hsec(self, row, h0):
        try:
            return float(h0) - float(row["estim_1"])
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_estim_2(self, row):
        try:
            return float(row["h"]) - float(row["h_sec"])
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_v(self, row):
        try:
            return math.pow(20 * float(row["estim_2"]), 0.5)
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_P(self, row):
        try:
            return float(row["velocity"]) * math.pow(float(row["p_a"]), 2) / 1000
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_Ppeak(self, row):
        try:
            return float(row["P"]) * 3
        except (KeyError, IndexError, ValueError, TypeError):
            return None


    def calculate_profile_hfront_ch(self, row, volume):
        try:
            volume = float(volume) * 1000
            velocity = float(row["velocity"])
            return (0.08 * (math.log(volume) - 0.1)) * math.pow(velocity, 0.74 + 0.12)
        except (KeyError, IndexError, ValueError, TypeError):
            return None
        
    def find_intersection(self, df):
        """
        Находит пересечения двух кривых, исключая точку с l=0, и возвращает
        координату l самой дальней точки пересечения.
        """
        # Создаем линии для h и h_sec, используя x из столбца l, исключая x=0
        line_h = LineString([(x, h) for x, h in zip(df['l'], df['h']) if x != 0])
        line_h_sec = LineString([(x, h) for x, h in zip(df['l'], df['h_sec']) if x != 0])
    
        # Находим пересечение линий
        intersection = line_h.intersection(line_h_sec)
    
        # Если пересечений нет, возвращаем None
        if intersection.is_empty:
            return None
    
        # Определяем точки пересечения
        if isinstance(intersection, Point):
            # Одно пересечение
            intersection_points = [intersection]
        elif isinstance(intersection, MultiPoint):
            # Несколько пересечений
            intersection_points = list(intersection.geoms)
        else:
            # Обработка других случаев (например, MultiLineString)
            intersection_points = [
                geom for geom in intersection.geoms if isinstance(geom, Point)
            ]
    
        # Если есть пересечения, возвращаем l (x-координату) самой дальней точки
        if intersection_points:
            furthest_point = max(intersection_points, key=lambda p: p.x)
            return furthest_point.x
    
        # Если пересечений нет, возвращаем None
        return None