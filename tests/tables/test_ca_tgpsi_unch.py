import unittest
from srcs.modules.tables.ca_tgpsi_unch import CaTgPsiUnCh


class TestCaTgPsiUcCh(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tgpsi_ch = CaTgPsiUnCh()

    table_data = {
        100: [
            (25, 0.456), (26, 0.479), (27, 0.502), (28, 0.525), (29, 0.548),
            (30, 0.571), (31, 0.594), (32, 0.617), (33, 0.640), (34, 0.663),
            (35, 0.686), (36, 0.709), (37, 0.732), (38, 0.755), (39, 0.778),
        ],
        300: [
            (25, 0.431), (26, 0.453), (27, 0.475), (28, 0.497), (29, 0.519),
            (30, 0.541), (31, 0.563), (32, 0.585), (33, 0.607), (34, 0.629),
            (35, 0.651), (36, 0.673), (37, 0.695), (38, 0.717), (39, 0.739),
        ],
        350: [
            (25, 0.4185), (26, 0.4400), (27, 0.4615), (28, 0.4830), (29, 0.5045),
            (30, 0.5260), (31, 0.5475), (32, 0.5690), (33, 0.5905), (34, 0.6120),
            (35, 0.6335), (36, 0.6550), (37, 0.6765), (38, 0.6980), (39, 0.7195),
        ],
    }

    def test_get_coefficient(self):
        for water, values in self.table_data.items():
            for tg, expected in values:
                with self.subTest(water=water, tg=tg):
                    result = self.tgpsi_ch.get_coefficient(tg=tg, water=water)
                    self.assertAlmostEqual(result, expected, places=4)