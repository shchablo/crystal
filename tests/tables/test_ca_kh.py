import unittest
from srcs.modules.tables.ca_kh import CaKh



class TestCaKh(unittest.TestCase):
    
    
    def setUp(self):
        self.kh = CaKh()


    def test_get_coefficient(self):
        
        coefficient_dry = self.kh.get_coefficient(height=0.5, avalanche_type="dry")
        coefficient_wet = self.kh.get_coefficient(height=1.0, avalanche_type="wet")
        self.assertAlmostEqual(coefficient_dry, 0.4, places=2)
        self.assertAlmostEqual(coefficient_wet, 0.6, places=2)

        with self.assertRaises(ValueError):
            self.kh.get_coefficient(height=0.5, avalanche_type="unknown")