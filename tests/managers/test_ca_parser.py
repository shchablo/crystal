import unittest
from srcs.modules.managers.ca_parser import CaParser



class TestCaParser(unittest.TestCase):


    def setUp(self):
        self.parser = CaParser()

        return


    def test_parse_single_command(self):

        commands = {"test": lambda arg1=None: {"arg1": arg1}}
        args = ["test", "--arg1", "value1"]

        parsed = self.parser.parse_commands(args, commands)

        self.assertEqual(len(parsed), 1, "Parsed output does not contain exactly one command.")
        self.assertEqual(parsed[0][0], "test", "Parsed command name is incorrect.")
        self.assertIn("arg1", parsed[0][1], "Key 'arg1' is missing in parsed command arguments.")
        self.assertEqual(parsed[0][1]["arg1"], "value1", "Value of 'arg1' is incorrect.")

        return