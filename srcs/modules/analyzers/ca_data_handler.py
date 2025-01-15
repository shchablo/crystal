import os
import zipfile
import pandas as pd
from typing import Optional, Dict, Any

class CaTopDataHandler:

    def __init__(self, core, data_handler, print_cmds):
        """

        Initializes the top-level class with entry points for various actions.

        :param core (CaCore): An instance of the core manager.
        :param print_cmds: List of command names in the order of use in the print function.

        """
        self.core = core
        self.data_handler = data_handler
        self.print_cmds = print_cmds

    def print(self, path: str = None, mode: str = "head", index: int = 0, **kwargs) -> None:
        """
        Load and display a summary of the processed data.
      
        :param path: Path to the folder or ZIP file containing the data.
        :param mode: Display mode for the data. Options are "head" or "tail" (default: head).
        :param index: Index of the profile to display (0-based).

        :param kwargs: Additional arguments to pass to the included commands (See: handler.execute).

        """
        
        args: Dict[str, Any] = {
            key: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
        }
        args["path"] = path[0]
        self.core.execute_command(
            command=self.print_cmds[0],
            command_args=args,
            commands=self.core.register.commands
        )
        
        # Print loaded data
        if mode == "head":
            profile_key = list(self.data_handler.profiles.keys())[index]
            print(f"Profiles Index {index}:\n", self.data_handler.profiles[profile_key].head())
            print("\nInput CSV:\n", self.data_handler.input_csv.head())
            print("\nObject CSV:\n", self.data_handler.object_csv.head())
        elif mode == "tail":
            profile_key = list(self.data_handler.profiles.keys())[index]
            print(f"Profiles Index {index}:\n", self.data_handler.profiles[profile_key].tail())
            print("\nInput CSV:\n", self.data_handler.input_csv.tail())
            print("\nObject CSV:\n", self.data_handler.object_csv.tail())

class CaDataHandler:

    """
    A class to handle data processing tasks such as loading profiles and CSV files, extracting ZIP archives, and preparing data for analysis.
    """

    def __init__(self):

        """
        Initializes the CaDataHandler instance with empty profiles and CSV placeholders.
        """

        self.profiles = {}
        self.input_csv = None
        self.object_csv = None

    def _reverse_dict(self, input_dict):
        return {value: key for key, value in input_dict.items()}

    def load_profiles(
            self,
            profiles_path: str,
            file_extension: str,
            separator: str,
            decimal: str,
            column_aliases: Optional[Dict[str, str]] = None,
    ) -> Dict[str, pd.DataFrame]:
        """

        Load all profiles from the specified folder.

        :param profiles_path: Path to the folder containing profile files.
        :param file_extension: Expected file extension for the profiles (e.g., ".csv").
        :param separator: Character used to separate values in the file (e.g., ",").
        :param decimal: Character used to denote decimals in numeric data.
        :param column_aliases: Optional dictionary to rename columns in the profiles.

        :return: A dictionary where keys are filenames and values are corresponding DataFrames.

        """
        profiles = {}
        for filename in os.listdir(profiles_path):
            if filename.endswith(file_extension):
                filepath = os.path.join(profiles_path, filename)
                df = pd.read_csv(filepath, sep=separator, decimal=decimal)
                if column_aliases:
                    df.rename(columns=self._reverse_dict(column_aliases), inplace=True)
                profiles[filename] = df
        return profiles

    def load_csv(
            self,
            file_path: str,
            file_extension: str,
            separator: str,
            decimal: str,
            column_aliases: Optional[Dict[str, str]] = None,
    ) -> pd.DataFrame:
        """

        Load a CSV file and apply column aliases if provided.

        :param file_path: Path to the CSV file.
        :param file_extension: Expected file extension for the input file (e.g., ".csv").
        :param separator: Character used to separate values in the file (e.g., ",").
        :param decimal: Character used to denote decimals in numeric data.
        :param column_aliases: Optional dictionary to rename columns in the CSV.

        :return: A DataFrame containing the loaded data.

        :raises ValueError: If the file does not have the expected extension.

        """
        if not file_path.endswith(file_extension):
            raise ValueError(f"File must have the extension {file_extension}")
        df = pd.read_csv(file_path, sep=separator, decimal=decimal)
        if column_aliases:
            df.rename(columns=self._reverse_dict(column_aliases), inplace=True)
        return df

    def execute(
            self,
            path: str = None,
            profiles_path_postfix: str = "profiles",
            input_path_postfix: str = "input.csv",
            object_path_postfix: str = "objects.csv",
            profile_extension: str = ".txt",
            profile_separator: str = "\t",
            profile_decimal: str = ",",
            profile_column_aliases: Optional[Dict[str, str]] = { "X": "X", "altitude" : "Feature Profile 1"  },
            input_extension: str = ".csv",
            input_separator: str = ";",
            input_decimal: str = ",",
            input_column_aliases: Optional[Dict[str, str]] = None,
            object_extension: str = ".csv",
            object_separator: str = ",",
            object_decimal: str = ".",
            object_column_aliases: Optional[Dict[str, str]] = None,
    ) -> None:
        """

        Prepare the folder or archive for processing and load all data.

        :param path: Path to a ZIP archive or a folder containing the data.

        :param profiles_path_postfix: Subfolder name where profiles are stored.
        :param input_path_postfix: Filename for the input CSV.
        :param object_path_postfix: Filename for the objects CSV.

        :param profile_extension: Expected file extension for profile files.
        :param profile_separator: Separator for profile files.
        :param profile_decimal: Decimal character for profile files.
        :param profile_column_aliases: Optional column renaming dictionary for profiles.

        :param input_extension: Expected file extension for the input CSV.
        :param input_separator: Separator for the input CSV.
        :param input_decimal: Decimal character for the input CSV.
        :param input_column_aliases: Optional column renaming dictionary for the input CSV.

        :param object_extension: Expected file extension for the objects CSV.
        :param object_separator: Separator for the objects CSV.
        :param object_decimal: Decimal character for the objects CSV.
        :param object_column_aliases: Optional column renaming dictionary for the objects CSV.

        :return: None
        """
        
        # Extract directory and archive name
        archive_dir = os.path.dirname(path)
        archive_name = os.path.splitext(os.path.basename(path))[0]
        extraction_folder = os.path.join(archive_dir, archive_name)

        # If it's a ZIP file, extract it
        if path.endswith(".zip"):
            if not os.path.exists(extraction_folder):
                os.makedirs(extraction_folder)
            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(extraction_folder)  # Extract directly into the correct folder
            folder_path = extraction_folder
        else:
            folder_path = path

        # Load profiles
        profiles_path = os.path.join(folder_path, profiles_path_postfix)
        self.profiles = self.load_profiles(
            profiles_path,
            file_extension=profile_extension,
            separator=profile_separator,
            decimal=profile_decimal,
            column_aliases=profile_column_aliases,
        )

        # Load input.csv
        input_csv_path = os.path.join(folder_path, input_path_postfix)
        self.input_csv = self.load_csv(
            input_csv_path,
            file_extension=input_extension,
            separator=input_separator,
            decimal=input_decimal,
            column_aliases=input_column_aliases,
        )

        # Load object.csv
        object_csv_path = os.path.join(folder_path, object_path_postfix)
        self.object_csv = self.load_csv(
            object_csv_path,
            file_extension=object_extension,
            separator=object_separator,
            decimal=object_decimal,
            column_aliases=object_column_aliases,
        )