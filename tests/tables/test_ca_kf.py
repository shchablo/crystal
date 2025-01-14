import unittest
from srcs.modules.tables.ca_kf import CaKf

class TestCaKf(unittest.TestCase):
    def setUp(self):
        self.kf = CaKf()

    def test_get_coefficient(self):
        print(f"\n{'-' * 80}\n{self.__class__.__name__}.{self._testMethodName}")
        
        coefficient_dry = self.kf.get_coefficient(height_zero=0.5, area=15, avalanche_type="dry")
        coefficient_wet = self.kf.get_coefficient(height_zero=1.0, area=7, avalanche_type="wet")
        self.assertAlmostEqual(coefficient_dry, 0.3, places=2)
        self.assertAlmostEqual(coefficient_wet, 0.5, places=2)

        with self.assertRaises(ValueError):
            self.kf.get_coefficient(height_zero=0.5, area=10, avalanche_type="unknown")