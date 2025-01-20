import os
from pathlib import Path

import unittest
import pandas as pd

from srcs.modules.processors.ca_handler import CaHandler



class TestCaHandler(unittest.TestCase):
    
    
    def setUp(self):
        
        self.instance = CaHandler()

        self.path = str(Path(__file__).resolve().parent / "data_ca_handler")
        
        self.expected_profile_34 = pd.DataFrame({
            "ColA": [
                0.0, 
                4.79181755284, 
                9.58363510574, 
                14.3754526586, 
                19.0226480886,
                23.6698435185,
                28.3170389485,
                32.436143198,
                36.555247448,
                40.6743516976,
                44.7934559476
            ],
            "ColB": [
                699.755741837, 
                696.764291012, 
                692.753288689, 
                688.637827039, 
                684.502373303, 
                680.280974353, 
                676.307399174, 
                673.207359137, 
                669.816873684, 
                666.418409164, 
                663.262168635
            ],
        })
        
        self.expected_profile_28 = pd.DataFrame({
            "ColA": [
                0.0, 
                4.81933370548, 
                9.63866741099, 
                14.4580011165, 
                18.5101960446,
                22.562390972,
                26.6145859001,
                30.6667808275,
                34.7189757557
            ],
            "ColB": [
                514.399065721, 
                512.134141056, 
                509.832571846, 
                507.549226801, 
                505.612816477, 
                503.695892883, 
                501.751713252, 
                499.784599568, 
                497.746029123
            ],
        })
        
        self.expected_main = pd.DataFrame({
            "name": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34],
            "type": ['O', 'L', 'O', 'L', 'O', 'L', 'O', 'O', 'O', 'O', 'O', 'L', 'O', 'L', 'L', 'O', 'O', 'O', 'O', 'O', 'L', 'O', 'O', 'L', 'O', 'O', 'L', 'L', 'L', 'O', 'O', 'O', 'O', 'L'],
            "area": [8.6, 1.4, 1.4, 1.1, 1.6, 0.9, 7.1, 5.4, 14.5, 5.3, 4.7, 1, 8, 6.7, 1.8, 3.3, 5.1, 8.3, 7.3, 10.2, 3.8, 1.2, 3, 1.8, 1.3, 3.8, 1.7, 2.8, 0.7, 2.3, 1.6, 4.2, 5.3, 16],
            "slope": [28, 28, 31, 31, 30, 31, 30, 25, 28, 29, 35, 36, 27, 33, 34, 35, 33, 35, 35, 32, 31, 31, 27, 31, 31, 31, 29, 27, 27, 26, 28, 27, 29, 35],
            "W": [350] * 34,
            "hi": [0.9] * 34,
            "cat": ['dry'] * 34,
            "plt": [300] * 34
        })
        
        self.expected_objects = pd.DataFrame({
            "name": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "object": ["garage", "budka", "garage", "garage", "garage", "garage", "garage", "garage", "garage", "garage", "garage", "budka", "budka", "budka", "budka", "budka", "budka", "budka", "budka"],
            "dist": [881, 120, 862, 823, 854, 873, 940, 692, 1138, 1359, 673, 445, 464, 189, 480, 555, 521, 590, 599]
        })


    def test_execute(self):
        
        self.instance.path =  self.instance.extract(str(self.path))

        profiles_path_postfix="profiles"
        profile_extension=".txt"
        profile_separator="\t"
        profile_decimal=","
        profile_column_aliases={"ColA": "X", "ColB" : "Feature Profile 1"}
        input_path_postfix="main.csv"
        input_extension=".csv"
        input_separator=";"
        input_decimal=","
        object_path_postfix="objects.csv"
        object_extension=".csv"
        object_separator=","
        object_decimal="."

        profiles_path = os.path.join(self.instance.path, profiles_path_postfix)
        self.instance.profiles = self.instance.profiles = self.instance.load_profiles(
            profiles_path,
            file_extension=profile_extension,
            separator=profile_separator,
            decimal=profile_decimal,
            column_aliases=profile_column_aliases
        )

        main_path = os.path.join(self.instance.path, input_path_postfix)
        self.instance.main = self.instance.main = self.instance.load_csv(
            main_path,
            file_extension=input_extension,
            separator=input_separator,
            decimal=input_decimal
        )

        objects_path = os.path.join(self.instance.path, object_path_postfix)
        self.instance.objects = self.instance.load_csv(
            objects_path,
            file_extension=object_extension,
            separator=object_separator,
            decimal=object_decimal
        )

        pd.testing.assert_frame_equal(self.instance.profiles["34"], self.expected_profile_34)
        pd.testing.assert_frame_equal(self.instance.profiles["28"], self.expected_profile_28)
        pd.testing.assert_frame_equal(self.instance.main, self.expected_main)
        pd.testing.assert_frame_equal(self.instance.objects, self.expected_objects)
