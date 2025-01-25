import os
from pathlib import Path
import pandas as pd
import unittest


from srcs.modules.managers.ca_core import CaCore
from srcs.modules.managers.ca_configurator import CaConfigurator

from srcs.modules.tables.ca_kh import CaKh
from srcs.modules.tables.ca_kf import CaKf
from srcs.modules.tables.ca_tgpsi_ch import CaTgPsiCh
from srcs.modules.tables.ca_tgpsi_unch import CaTgPsiUnCh

from srcs.modules.processors.ca_handler import CaHandler, CaTopHandler
from srcs.modules.processors.ca_calculator import CaCalculator, CaTopCalculator
from srcs.modules.processors.ca_plotter import CaPlotter, CaTopPlotter


class TestCaHandler(unittest.TestCase):

    def setUp(self):

        self.core = CaCore()
        
        self.expected_objects = pd.DataFrame({
            "№ очага": [1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "Объект": [
                "garage", "Будка", "garage", "garage", "garage", "garage", "garage", "garage",
                "garage", "garage", "garage", "budka", "budka", "budka", "budka", "budka", "budka", "budka", "budka"
            ],
            "Расстояние до объекта, м": [
                881, 120, 862, 823, 854, 873, 940, 692, 1138, 1359, 673, 445, 464, 189, 480, 555, 521, 590, 599
            ],
            "Скорость, м/с": [
                None, 13.9, None, None, None, None, None, None, None, None, None, None, 3.7, None, 18.9, None, None, None, None
            ],
            "Давление, кПа": [
                None, 58.0, None, None, None, None, None, None, None, None, None, None, 4.1, None, 107.2, None, None, None, None
            ],
            "Пиковое давление, кПа": [
                None, 174.0, None, None, None, None, None, None, None, None, None, None, 12.3, None, 321.6, None, None, None, None
            ],
            "Высота фронта, м": [
                2.7, 2.7, None, 2.7, None, 2.7, None, 2.7, 2.7, 2.7, 2.7, 2.7, 0.7, 2.7, 8.5, None, 2.7, 2.7, 2.7
            ],
            "Дальность выброса лавины, м": [
                226.0, 226.0, 279.0, 191.0, 239.0, 194.0, 291.0, 193.0, 327.0, 457.0, 523.0, 259.0, 467.0, 132.0, 569.0, 487.0,
                322.0, 412.0, 418.0
            ],
        })


    def test_main(self):

        # 1
        handler = CaHandler()
        handler.path = str(Path(__file__).resolve().parent / "data_ca_handler")
        handler.extract(path=handler.path)
        
        # 2
        configurator = CaConfigurator()
        file_cfg = configurator.find_config_file(directory_path=handler.path)
        configurator.upload(path=str(file_cfg))
        
        # 3
        top_handler = CaTopHandler(self.core, handler)
        top_handler.execute()

        # 4 
        kh = CaKh()
        kf = CaKf()
        tgpsi_ch = CaTgPsiCh()
        tgpsi_unch = CaTgPsiUnCh()
        calculator = CaCalculator(handler, kh, kf, tgpsi_ch, tgpsi_unch)
        top_calculator = CaTopCalculator(self.core, calculator)
        top_calculator.process_main(verbose="n") 
        
        # 5
        top_calculator.process_profiles(verbose="n") 
        
        # 6
        top_calculator.analysis_profiles(verbose="n") 

        # 7
        plotter = CaPlotter(handler)
        top_plotter = CaTopPlotter(self.core, plotter)
        top_plotter.all(verbose="n")

        # 8
        top_handler.save_dfs_to_csv(verbose="n")

        pd.testing.assert_frame_equal(handler.objects, self.expected_objects)