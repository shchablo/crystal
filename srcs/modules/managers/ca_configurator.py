import json
import yaml
from pathlib import Path

from typing import Dict, Any


class CaTopConfigurator:

    def __init__(self, core):
        """

        Initializes the top-level class with entry points for various actions.

        :param core (CaCore): An instance of the core manager.

        """
        self.core = core

    def load_conf_and_generate_conf(self, **kwargs) -> None:
        """
        Wrapper command to load the configuration and generate a configuration file.

        :param kwargs: Additional arguments to pass to the included commands.
        """

        print(kwargs)

        load_args: Dict[str, Any] = {
            key[5:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith("load_")
        }
        print("Executing 'cfg.load' command with arguments:", load_args)
        self.core.execute_command(
            command="cfg.load",
            command_args=load_args,
            commands=self.core.register.commands
        )

        gen_args: Dict[str, Any] = {
            key[4:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith("gen_")
        }
        print("Executing 'cfg.gen' command with arguments:", gen_args)
        self.core.execute_command(
            command="cfg.gen",
            command_args=gen_args,
            commands=self.core.register.commands
        )


class CaConfigurator:
    """
    A class to handle configuration files in various formats (JSON, YAML).
    Provides functionality to load, modify, and save configurations.
    """

    def __init__(self):
        """
        Initializes the configuration manager with an empty configuration dictionary.
        """
        self.config = {}

    def load_config(self, path: str = None) -> None:
        """
        Loads a configuration file and updates the internal configuration.

        :paran path: The path to the configuration file.

        """
        file_path = Path(path)

        if not file_path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        extension = file_path.suffix.lower()
        with file_path.open("r", encoding="utf-8") as f:
            if extension == ".json":
                self.config.update(json.load(f))
            elif extension in {".yaml", ".yml"}:
                self.config.update(yaml.safe_load(f))
            else:
                raise ValueError(f"Unsupported file format: {extension}")

        print(f"Configuration successfully loaded from {path}.")

    def upload_config(self, path: str = None) -> None:
        """

        Saves the current configuration to a specified file.

        :param path: The path to the output configuration file.

        """
        file_path = Path(path)
        extension = file_path.suffix.lower()

        with file_path.open("w", encoding="utf-8") as f:
            if extension == ".json":
                json.dump(self.config, f, indent=4)
            elif extension in {".yaml", ".yml"}:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            else:
                raise ValueError(f"Unsupported file format: {extension}")

        print(f"Configuration successfully saved to {path}.")

    def update_config(self, new_config: dict) -> None:
        """

        Updates the internal configuration with the given dictionary.

        :param new_config: A dictionary containing new configuration values.

        """
        if not isinstance(new_config, dict):
            raise TypeError("The new configuration must be a dictionary.")

        self.config.update(new_config)
        print("Configuration successfully updated.")

    def get_config(self) -> dict:
        """

        :param new_config: The current configuration.

        """
        return self.config.copy()