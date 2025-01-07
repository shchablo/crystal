import json
import yaml
from pathlib import Path


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

        Args:
            path (str): The path to the configuration file.

        Raises:
            ValueError: If the file format is unsupported or the path is invalid.
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

        Args:
            path (str): The path to the output configuration file.

        Raises:
            ValueError: If the file format is unsupported.
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

        Args:
            new_config (dict): A dictionary containing new configuration values.
        """
        if not isinstance(new_config, dict):
            raise TypeError("The new configuration must be a dictionary.")

        self.config.update(new_config)
        print("Configuration successfully updated.")

    def get_config(self) -> dict:
        """
        Retrieves the current configuration.

        Returns:
            dict: The current configuration.
        """
        return self.config.copy()