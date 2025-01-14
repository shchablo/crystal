import unittest
from parameterized import parameterized
from srcs.modules.tables.ca_tgpsi_ch import CaTgPsiCh


class TestCaTgPsiCh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tgpsi_ch = CaTgPsiCh()

    table_data = {
        100: [
            (25, 0.456), (26, 0.479), (27, 0.502), (28, 0.525), (29, 0.548),
            (30, 0.571), (31, 0.594), (32, 0.617), (33, 0.64), (34, 0.663),
            (35, 0.686), (36, 0.709), (37, 0.732), (38, 0.755), (39, 0.778), (40, 0.801)
        ],
        300: [
            (25, 0.431), (26, 0.453), (27, 0.475), (28, 0.497), (29, 0.519),
            (30, 0.541), (31, 0.563), (32, 0.585), (33, 0.607), (34, 0.629),
            (35, 0.651), (36, 0.673), (37, 0.695), (38, 0.717), (39, 0.739), (40, 0.761)
        ],
        350: [
            (25, 0.4185), (26, 0.44), (27, 0.4615), (28, 0.483), (29, 0.5045),
            (30, 0.526), (31, 0.5475), (32, 0.569), (33, 0.5905), (34, 0.612),
            (35, 0.6335), (36, 0.655), (37, 0.6765), (38, 0.698), (39, 0.7195), (40, 0.741)
        ],
    }

    @parameterized.expand([
        (water_reserve, tg, coefficient)
        for water_reserve, values in table_data.items()
        for tg, coefficient in values
    ])
    def test_get_coefficient(self, water, tg, expected):
        print(f"\n{'-' * 80}\n{self.__class__.__name__}.{self._testMethodName}")
        
        result = self.tgpsi_ch.get_coefficient(tg=tg, water=water)
        self.assertAlmostEqual(result, expected, places=4)