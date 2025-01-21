import unittest
from srcs.modules.managers.ca_configurator import CaConfigurator
from srcs.modules.managers.ca_register import CaRegister



class TestCaRegister(unittest.TestCase):


    def setUp(self):
        self.configurator = CaConfigurator()
        self.register = CaRegister(self.configurator)

        return


    def test_register_single_command(self):
        def test_func(): pass
        self.register.add_command("test", test_func)
        self.assertIn("test", self.register.commands)
        self.assertEqual(self.register.commands["test"], test_func)

        return
