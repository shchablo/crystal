import os
import json
import yaml
from typing import Optional, Dict, Any

from pathlib import Path


class CaTopConfigurator:


    def __init__(self, core):
        """
        Initializes the top-level class with entry points for various actions.
        :param core (CaCore): An instance of the core manager.
        """
        self.core = core


    def find_config_file(self, path: str = None, verbose: str = "y") -> str:
        """
        Locate the configuration file based on the provided path.

          This function searches for a configuration file using the specified path. 
          If the path is not provided, it uses a default search mechanism. 
          The located configuration file path is returned, and an optional verbose output confirms the found file.

          Options:
            --path    | STRING | Path to the configuration file (default: None).
            --verbose | STRING | Controls the verbosity of the process (default: "y").
                                 Accepted values: "y", "yes", "true", "1" for verbose output.
        
          Example:
            crystal find_config_file --path "/path/to/config" --verbose "yes"
        """
        
        config_file = self.core.configurator.find_config_file(path)

        if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:
            print(f"Configuration file found: {config_file}.")

        return config_file

    def upload(self, path: str = None, verbose: str = "y", encoding: str='cp1251') -> None:
        """
        Loads a configuration file into the manager.

          This command allows uploading a configuration file in JSON or YAML format.
          Supported file formats include: .json, .yaml, .yml.

          Options:
            --path     | TEXT | Path to the configuration file (default: None; [name].[json|yaml].
            --encoding | TEXT | Encoding to read the configuration file (default: "utf-8", e.g., "utf-8", "cp1251").
            --verbose  | TEXT | Enable or disable output messages (default: "y"; verbose: "1|y|yes|true", no-verbose: "any").

          Example:
            crystal [cmd] --path path/to/file.json
         """

        isVerbose = str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}

        if (path == None):
            path = self.core.configurator.default_path
            if isVerbose:
                print(f"Loading the default file: {path}.")

        isLoaded = self.core.configurator.upload(path, encoding)

        if isVerbose:
            if (isLoaded):
                print(f"Configuration successfully loaded from {path}.")
            else:
                print(f"Configuration completed with default signatures.")


        return self.core.configurator.config


    def download(self, path: str = None, verbose: str = "y", encoding: str='cp1251') -> None:
        """
        Saves the current configuration to a specified file.

          This command allows uploading a configuration file in JSON or YAML format.
          Supported file formats include: .json, .yaml, .yml.

          Options:
            --path     | TEXT | Path to the configuration file (default: None, e.g., [name].[json|yaml].
            --encoding | TEXT | Encoding to read the configuration file (default: "utf-8", e.g., "utf-8", "cp1251").
            --verbose  | TEXT | Enable or disable output messages (default: "y", verbose: "1|y|yes|true", no-verbose: "any").

          Example:
            crystal [cmd] --path path/to/file.json
         """

        self.core.configurator.download(path, encoding)
        if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:
            print(f"Configuration successfully saved to {path}.")

        return self.core.configurator.config



class CaConfigurator:
    """
    A class to handle configuration files in various formats (JSON, YAML).
    Provides functionality to load, modify, and save configurations.
    """


    def __init__(self):
        """
        Initializes the configuration manager with an empty configuration dictionary.
        """

        self.default_path: str
        self.config = {}


    def find_config_file(self, directory_path: str) -> Optional[str]:
        """
        Search for a single JSON or YAML file in the specified directory.

        :param directory_path: Path to the directory where the search will be performed.
        :return: The path to the file if exactly one JSON or YAML file is found; otherwise, None.
        :raises ValueError: If the directory does not exist or is not a directory.
        """
        if not os.path.isdir(directory_path):
            raise ValueError(f"The provided path '{directory_path}' is not a valid directory.")

        # Collect all .json, .yaml, and .yml files in the directory
        config_files = [
            os.path.join(directory_path, f) for f in os.listdir(directory_path)
            if f.endswith(('.json', '.yaml', '.yml'))
        ]

        # Return the file path if exactly one file is found, otherwise None
        return config_files[0] if len(config_files) == 1 else None


    def upload(self, path: str, encoding: str='cp1251') -> bool:
        """
        Loads a configuration file (JSON or YAML) into the internal dictionary.

        :param path: Path to the configuration file.

        :raises ValueError: If the file format is unsupported.
        """
        file_path = Path(path)

        if not file_path.is_file():
            return False

        extension = file_path.suffix.lower()
        with file_path.open("r", encoding=encoding) as f:
            if extension == ".json":
                self.config.update(json.load(f))
            elif extension in {".yaml", ".yml"}:
                self.config.update(yaml.safe_load(f))
            else:
                raise ValueError(f"Unsupported file format: {extension}")

        return True


    def download(self, path: str, encoding: str='cp1251') -> None:
        """
        Saves the current configuration to a specified file in JSON or YAML format.

        :param path: The path to the output configuration file.

        :raises ValueError: If the file format is unsupported.
        """
        file_path = Path(path)
        extension = file_path.suffix.lower()

        with file_path.open("w", encoding=encoding) as f:
            if extension == ".json":
                json.dump(self.config, f, indent=4)
            elif extension in {".yaml", ".yml"}:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
            else:
                raise ValueError(f"Unsupported file format: {extension}")

        return


    def update(self, new_config: dict) -> None:
        """
        Updates the internal configuration with the given dictionary.

        :param new_config: A dictionary containing new configuration values.

        :raises TypeError: If the provided new_config is not a dictionary.
        """
        if not isinstance(new_config, dict):
            raise TypeError("The new configuration must be a dictionary.")

        self.config.update(new_config)

        return


    def get(self) -> dict:
        """
        Retrieves a copy of the current configuration.

        :return: A dictionary containing the current configuration.
        """
        return self.config.copy()