import os
import zipfile
import pandas as pd
from typing import Optional, Dict, Any
import random
import ast

class CaTopHandler:


    def __init__(self, core, handler):
        """

        Initializes the top-level class with entry points for various actions.

        :param core (CaCore): An instance of the core manager.
        :param handler (CaHandler): An instance of the handler manager.

        """
        self.core = core
        self.handler = handler


    def extract(self, path: str = None, verbose: str = "y") -> str:
        """
        Extracts the contents of a ZIP file into a directory with the same name as the archive.
        It returns and saves into memory of programm the path to the extracted folder.
        If the file is not a ZIP archive, returns the original path.

          Options:

            --path    | TEXT | Path to a ZIP archive or a folder containing the data.
            --verbose | TEXT | Enable or disable output messages (default: "y"; verbose: "1|y|yes|true", no-verbose: "any").
        """

        self.handler.path = self.handler.extract(path)

        if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:
            print(f"Data folder found {self.handler.path}.")

        return self.handler.path


    def execute(
            self,
            profiles_path_postfix: str = "profiles",
            profile_extension: str = ".txt",
            profile_separator: str = "\t",
            profile_decimal: str = ",",
            profile_column_aliases: Optional[Dict[str, str]] = { "l": "X",
                                                                 "h" : "Feature Profile 1"  },
            main_path_postfix: str = "main.csv",
            main_separator: str = ";",
            main_decimal: str = ",",
            main_column_aliases: Optional[Dict[str, str]] = { "name": "name",
                                                                "type" : "type",
                                                                "area" : "area",
                                                                "slope" : "slope",
                                                                "W" : "W",
                                                                "hi" : "hi",
                                                                "cat" : "cat",
                                                                "plt" : "plt" },
            object_path_postfix: str = "objects.csv",
            object_separator: str = ",",
            object_decimal: str = ".",
            object_column_aliases: Optional[Dict[str, str]] = { "name": "name",
                                                                "object" : "object",
                                                                "dist" : "dist" },
    ) -> None:
        """
        Prepare the folder or archive for processing and load all data.

          This command processes a folder or ZIP archive containing data files and loads profiles, input CSV, and objects CSV into memory.
          Supports configuring file extensions, separators, decimals, and column aliases for each data type.

          Options:

            --profiles_path_postfix  | TEXT | Subfolder name where profiles are stored (default: profiles).
            --profile_extension      | TEXT | File extension for profile files (default: .txt).
            --profile_separator      | TEXT | Separator for profile files (default: \t).
            --profile_decimal        | TEXT | Decimal character for profile files (default: ,).
            --profile_column_aliases | DICT | Optional column renaming dictionary for profiles.

            --main_path_postfix     | TEXT | Filename for the input CSV (default: input.csv).
            --main_separator         | TEXT | Separator for the input CSV (default: ;).
            --main_decimal           | TEXT | Decimal character for the input CSV (default: ,).
            --main_column_aliases    | DICT | Optional column renaming dictionary for the input CSV.

            --object_path_postfix    | TEXT | Filename for the objects CSV (default: objects.csv).
            --object_separator       | TEXT | Separator for the objects CSV (default: ,).
            --object_decimal         | TEXT | Decimal character for the objects CSV (default: .).
            --object_column_aliases  | DICT | Optional column renaming dictionary for the objects CSV.
        """

        profiles_path = os.path.join(self.handler.path, profiles_path_postfix)
        self.handler.profiles = self.handler.load_profiles(
            profiles_path,
            file_extension=profile_extension,
            separator=profile_separator,
            decimal=profile_decimal,
            column_aliases=profile_column_aliases,
        )

        main_path = os.path.join(self.handler.path, main_path_postfix)
        self.handler.main = self.handler.load_csv(
            main_path,
            separator=main_separator,
            decimal=main_decimal,
            column_aliases=main_column_aliases,
        )
        self.handler.internal_main = self.handler.main

        objects_path = os.path.join(self.handler.path, object_path_postfix)
        self.handler.objects = self.handler.load_csv(
            objects_path,
            separator=object_separator,
            decimal=object_decimal,
            column_aliases=object_column_aliases,
        )

        return


    def read(self, path: str = None, verbose: str = "y", **kwargs) -> None:
        """
          This command reads and loads data from a specified path.

          Options:
            --path    | TEXT | Path to the folder file containing the data (default: None).
            --verbose | TEXT | Enable or disable output messages (default: "y"; verbose: "1|y|yes|true", no-verbose: "any").
            **kwargs  | ARGS | Additional arguments passed to the internal execution command.

          Example:
            crystal [cmd] --path path/to/data
            crystal [cmd] --path path/to/data --main_extension .txt
        """


        self.handler.path = self.handler.extract(path)

        args: Dict[str, Any] = {
            key: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
        }
        self.core.execute_command(
            command=self.core.register.find_command_name(self.execute),
            command_args=args,
            commands=self.core.register.commands
        )
        if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:
            print(f"Data was read and loaded from: {self.handler.path}.")

        return


    def print(self, mode: str = "sample", profiles: str = "'any'", verbose: str = "y") -> None:
        """
          Displays a summary based on the chosen mode.
          The display mode can show either the "head" or "tail" of the data.
          Supports specifying the names of the profile to display.

          Options:
            --mode     | TEXT | Display mode for the data. Options are "head", "tail", "info", "describe", "sample" (default: sample).
            --profiles | TEXT | Name of the profile to display (default: ""; "['1', '2']" , "'all'", "'any'").
            --verbose  | TEXT | Enable or disable output messages (default: "y"; verbose: "1|y|yes|true", no-verbose: "any").

          Example:
            crystal [cmd] --mode head
            crystal [cmd] --mode head --profiles "['1', '[name]']"
        """

        if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:

            supported_modes = {"head", "tail", "info", "describe", "sample"}

            if mode in supported_modes:

                print("Input:\n", getattr(self.handler.main, mode)())
                print("Objects:\n", getattr(self.handler.objects, mode)())

                print(f"Number of Profiles: {len(self.handler.profiles)}")
                try:
                      # Parse profile string into a list
                      parsed_profile = ast.literal_eval(profiles) if profiles else []

                      selected_profiles = []
                      if isinstance(parsed_profile, str) and parsed_profile == "all":
                          selected_profiles = self.handler.profiles.keys()
                      elif parsed_profile == "any":
                        if self.handler.profiles:
                            selected_profiles = [random.choice(list(self.handler.profiles.keys()))]
                        else:
                            print("No profiles available for selection.")
                      elif isinstance(parsed_profile, list):
                          selected_profiles = [p.strip() for p in parsed_profile]
                      else:
                          raise ValueError("Invalid format for profile.")

                except (SyntaxError, ValueError):
                    print("Error: Profile must be a valid string, list, or 'all'.")
                    return

                for profile_name in selected_profiles:
                    if profile_name in self.handler.profiles:
                        method = getattr(self.handler.profiles[profile_name], mode, None)
                        if callable(method):
                            print(f"Profile {profile_name}:\n", method())
                        else:
                            print(f"Mode '{mode}' is not callable for the profile '{profile_name}'.")
                    else:
                        print(f"Profile '{profile_name}' does not exist.")
            else:
                print(f"Invalid mode: {mode}. Supported modes: {', '.join(supported_modes)}.")

            return


    def save_dfs_to_csv(
                self,
                path: str = "result",
                encoding: str = 'cp1251',

                profiles_path_postfix: str = "profiles",
                profile_extension: str = ".txt",
                profile_separator: str = ";",
                profile_decimal: str = ",",
                profile_column_aliases: Optional[Dict[str, str]] = { "l": "Гориз. проложение, м",
                                                                     "h" : "Абс. высота, м",
                                                                     "tg" : "Тангенс",
                                                                     "rad" : "Угол, рад.",
                                                                     "deg" : "Угол, °",
                                                                     "tg_psi" : "Тангенс пси",
                                                                     "estim_1" : "Первая расчетная",
                                                                     "h_sec" : "Высота секущей, м",
                                                                     "estim_2" : "Вторая расчетная",
                                                                     "velocity" : "Скорость, м/с",
                                                                     "plt" : "Плотность, кг/м3",
                                                                     "P" : "Давление, кПа",
                                                                     "P_peak" : "Пиковое давление, кПа",
                                                                     "h_front" : "Высота фронта, м"
                                                                    },
                main_path_postfix: str = "main.csv",
                main_separator: str = ";",
                main_decimal: str = ",",
                main_column_aliases: Optional[Dict[str, str]] = { "name": "№ очага",
                                                                  "type" : "Морфологический тип",
                                                                  "area" : "Площадь, га",
                                                                  "slope" : "Угол наклона зон зарождения и транзита, °",
                                                                  "W" : "Водозапас, мм",
                                                                  "hi" : "Высота снежного покрова, м",
                                                                  "cat" : "Вид",
                                                                  "plt" : "Плотность, кг/м3",
                                                                  "tg_psi" : "Тангенс пси",
                                                                  "volume" : "Объем, тыс. м3",
                                                                  "L_max" : "Дальность выброса лавины, м"
                                                                  },
                object_path_postfix: str = "objects.csv",
                object_separator: str = ";",
                object_decimal: str = ",",
                object_column_aliases: Optional[Dict[str, str]] = { "name": "№ очага",
                                                                    "object" : "Объект",
                                                                    "dist" : "Расстояние до объекта, м",
                                                                    "velocity" : "Скорость, м/с",
                                                                    "P" : "Давление, кПа",
                                                                    "P_peak" : "Пиковое давление, кПа",
                                                                    "h_front" : "Высота фронта, м",
                                                                    "L_max" : "Дальность выброса лавины, м"
                                                                  },
                verbose: str = "y"
            ) -> None:
            """
            Prepare the folder or archive for processing and load all data.

              This command processes a folder or ZIP archive containing data files and loads profiles, input CSV, and objects CSV into memory.
              Supports configuring file extensions, separators, decimals, and column aliases for each data type.

              Options:

                --path                   | TEXT | Path to the folder to save the data (default: None).
                --encoding               | TEXT | Encoding to read the configuration file (default: "utf-8", e.g., "utf-8", "cp1251").

                --profiles_path_postfix  | TEXT | Subfolder name where profiles are stored (default: profiles).
                --input_path_postfix     | TEXT | Filename for the input CSV (default: input.csv).
                --object_path_postfix    | TEXT | Filename for the objects CSV (default: objects.csv).

                --profile_extension      | TEXT | File extension for profile files (default: .txt).
                --profile_separator      | TEXT | Separator for profile files (default: \t).
                --profile_decimal        | TEXT | Decimal character for profile files (default: ,).
                --profile_column_aliases | DICT | Optional column renaming dictionary for profiles.

                --main_separator         | TEXT | Separator for the input CSV (default: ;).
                --main_decimal           | TEXT | Decimal character for the input CSV (default: ,).
                --main_column_aliases    | DICT | Optional column renaming dictionary for the input CSV.

                --object_separator       | TEXT | Separator for the objects CSV (default: ,).
                --object_decimal         | TEXT | Decimal character for the objects CSV (default: .).
                --object_column_aliases  | DICT | Optional column renaming dictionary for the objects CSV.

                --verbose                | TEXT | Enable or disable output messages (default: "y"; verbose: "1|y|yes|true", no-verbose: "any").

              Example:
                  crystal [cmd] --path path/to/data
            """

            save_path = os.path.join(self.handler.path, path)
            os.makedirs(save_path, exist_ok=True)

            input_path = os.path.join(save_path, main_path_postfix)
            self.handler.main.rename(columns=main_column_aliases, inplace=True)
            self.handler.main.to_csv(
                input_path,
                index=False,
                sep=main_separator,
                decimal=main_decimal,
                encoding=encoding
            )

            object_path = os.path.join(save_path, object_path_postfix)
            self.handler.objects.rename(columns=object_column_aliases, inplace=True)
            self.handler.objects.to_csv(
                object_path,
                index=False,
                sep=object_separator,
                decimal=object_decimal,
                encoding=encoding
            )

            profiles_dir = os.path.join(save_path, profiles_path_postfix)
            os.makedirs(profiles_dir, exist_ok=True)
            for name, df in self.handler.profiles.items():
                if isinstance(df, pd.DataFrame):
                    profile_path = os.path.join(profiles_dir, f"{name}{profile_extension}")
                    df.rename(columns=profile_column_aliases, inplace=True)
                    df.to_csv(
                        profile_path,
                        index=False,
                        sep=profile_separator,
                        decimal=profile_decimal,
                        encoding=encoding
                    )
            if str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}:
                print(f"All results was saved into: {save_path}.")

            return



class CaHandler:
    """
    A class to handle data processing tasks such as loading profiles and CSV files, extracting ZIP archives, and preparing data for analysis.
    """


    def __init__(self):

        """
        Initializes the CaHandler instance with empty profiles and CSV placeholders.
        """

        self.config_file = None
        self.path = None
        self.profiles = {}
        self.main = None
        self.internal_main = None
        self.objects = None




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
                filename = os.path.splitext(os.path.basename(filepath))[0]
                profiles[filename] = df

        return profiles


    def load_csv(
            self,
            file_path: str,
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
        df = pd.read_csv(file_path, sep=separator, decimal=decimal)
        if column_aliases:
            df.rename(columns=self._reverse_dict(column_aliases), inplace=True)

        return df


    def extract(self, path: str) -> str:
        """
        Extracts the contents of a ZIP file into a directory with the same name as the archive and returns the path to the extracted folder.
        If the file is not a ZIP archive, returns the original path.

        :param path Path to a ZIP archive or a folder containing the data.
        """

        if not path:
            raise ValueError("Path must not be None or empty.")

        if not os.path.exists(path):
            raise FileNotFoundError(f"The file '{path}' does not exist.")

        archive_dir = os.path.dirname(path)
        archive_name = os.path.splitext(os.path.basename(path))[0]
        extraction_folder = os.path.join(archive_dir, archive_name)

        if path.endswith(".zip"):
            if not os.path.exists(extraction_folder):
                try:
                    os.makedirs(extraction_folder)
                except PermissionError as e:
                    raise PermissionError(f"Failed to create directory '{extraction_folder}': {e}")

            try:
                with zipfile.ZipFile(path, "r") as zip_ref:
                    zip_ref.extractall(extraction_folder)
            except zipfile.BadZipFile as e:
                raise zipfile.BadZipFile(f"Failed to extract ZIP archive: {e}")
            return extraction_folder
        else:
            return path

        return

