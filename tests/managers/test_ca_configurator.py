import contextlib
import io

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
        self.configurator.config = {"key": "value"}
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.configurator.upload_config(self.test_json)

    def test_load_config_json(self):
        with open(self.test_json, "w") as f:
            f.write('{"key": "value"}')
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.configurator.load_config(self.test_json)
        self.assertEqual(self.configurator.config["key"], "value")

    def test_upload_config_yaml(self):
        self.configurator.config = {"key": "value"}
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.configurator.upload_config(self.test_yaml)

    def test_load_config_yaml(self):
        with open(self.test_yaml, "w") as f:
            f.write("key: value\n")
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.configurator.load_config(self.test_yaml)
        self.assertEqual(self.configurator.config["key"], "value")