import pandas as pd
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
        
        self.calculator.handler.inputs['tgpsi'] = self.calculator.handler.inputs.apply(self.calculator.calculate_input_tg, axis=1)
        self.calculator.handler.inputs['v'] = self.calculator.handler.inputs.apply(self.calculator.calculate_input_v, axis=1)

        if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:
            print("Input data has been processed.")
        
        return
    
    def process_profiles(self, verbose: str = "y") -> None:
        
        for key, df in self.calculator.handler.profiles.items():
            df["tg"] = df.apply(lambda row: self.calculator.calculate_profile_tg(row, df), axis=1)
            df["rad"] = df.apply(self.calculator.calculate_profile_atan, axis=1)
            df["deg"] = df.apply(self.calculator.calculate_profile_deg, axis=1)
            df["tgpsi"] = df.apply(lambda row: self.calculator.find_profile_tgpsi(key), axis=1)

        if verbose.strip().lower() in {"1", "y", "yes", "true"}:
            print("All profiles have been processed.")

        return


class CaCalculator:
    def __init__(self, handler, kh, kf, tgpsi_ch, tgpsi_unch):
        
        self.handler = handler
        
        self.kh = kh
        self.kf = kf
        self.tgpsi_ch = tgpsi_ch
        self.tgpsi_unch = tgpsi_unch
    
    
    def calculate_input_v(self, row):
        h0 = float(row["hi"]) * self.kh.get_coefficient(float(row["hi"]), str(row["cat"]))
        kf = self.kf.get_coefficient(h0, float(row["area"]), str(row["cat"]))

        return h0 * kf * float(row["area"]) * 10


    def calculate_input_tg(self, row):
        row_type = str(row['type']).strip().lower()
        if row_type in {"1", "lotok", "ch", "channaled", "l", "channal"}:
            return self.tgpsi_ch.get_angle(
                float(row["W"]),
                float(row["slope"]),
                float(row["area"])
            )
        elif row_type in {"0", "ostov", "unch", "unchannaled", "o", "unchannal"}:
            return self.tgpsi_unch.get_angle(
                float(row["W"]),
                float(row["slope"])
            )

    def calculate_profile_tg(self, row, df):
        try:
            current_index = row.name  
            next_index = current_index + 1  

            if next_index >= len(df):
                return None

            x1 = float(row["x"])
            x2 = float(df.loc[next_index, "x"])
            y1 = float(row["alt"])
            y2 = float(df.loc[next_index, "alt"])

            if x2 == x1:
                raise ValueError("Division by zero: x2 and x1 are equal.")

            return (y1 - y2) / (x2 - x1)
        except KeyError as e:
            raise KeyError(f"Missing key in the row: {e}")
        except Exception as e:
            raise ValueError(f"Error processing the row: {e}")


    def calculate_profile_atan(self, row):
        return math.atan(row["tg"])
    
    
    def calculate_profile_deg(self, row):
        return math.degrees(row["rad"])


    def find_profile_tgpsi(self, key):
        
        result = self.handler.inputs.loc[self.handler.inputs['name'].astype(str) == str(key), 'tgpsi']
        result = result.values[0] if not result.empty else None
        
        return result