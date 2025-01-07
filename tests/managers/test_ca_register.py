import unittest
from modules.managers.ca_configurator import CaConfigurator
from modules.managers.ca_register import CaRegister


class TestCaRegister(unittest.TestCase):
    def setUp(self):
        self.configurator = CaConfigurator()
        self.register = CaRegister(self.configurator)

    def test_register_single_command(self):
        print(f"\n{'-' * 80}\n{self.__class__.__name__}.{self._testMethodName}")
        def test_func(): pass
        self.register.add_command("test", test_func)
        self.assertIn("test", self.register.commands)
        self.assertEqual(self.register.commands["test"], test_func)
