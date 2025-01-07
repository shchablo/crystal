import unittest
import os
import tempfile
from srcs.modules.managers.ca_configurator import CaConfigurator


class TestCaConfigurator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_json = os.path.join(self.test_dir.name, "test_ca_configurator.json")
        self.test_yaml = os.path.join(self.test_dir.name, "test_ca_configurator.yaml")
        
        self.configurator = CaConfigurator()
        self.configurator.config = {}

    def tearDown(self):
        self.test_dir.cleanup()

    def test_upload_config_json(self):
        print(f"\n{'-' * 80}\n{self.__class__.__name__}.{self._testMethodName}")
        self.configurator.config = {"key": "value"}
        self.configurator.upload_config(self.test_json)

    def test_load_config_json(self):
        print(f"\n{'-' * 80}\n{self.__class__.__name__}.{self._testMethodName}")
        with open(self.test_json, "w") as f:
            f.write('{"key": "value"}')
        self.configurator.load_config(self.test_json)
        self.assertEqual(self.configurator.config["key"], "value")

    def test_upload_config_yaml(self):
        print(f"\n{'-' * 80}\n{self.__class__.__name__}.{self._testMethodName}")
        self.configurator.config = {"key": "value"}
        self.configurator.upload_config(self.test_yaml)

    def test_load_config_yaml(self):
        print(f"\n{'-' * 80}\n{self.__class__.__name__}.{self._testMethodName}")
        with open(self.test_yaml, "w") as f:
            f.write("key: value\n")
        self.configurator.load_config(self.test_yaml)
        self.assertEqual(self.configurator.config["key"], "value")