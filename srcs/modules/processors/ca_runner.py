import os
import zipfile
import pandas as pd
from typing import Optional, Dict, Any
from pathlib import Path



class CaTopRunner:


    def __init__(self, core, cfg, handler, calculator):
        """
        Initializes the top-level class with entry points for various actions.

        :param core (CaCore): An instance of the core manager.
        :param cfg (CaTopConfigurator): An instance of the top configurator manager.
        :param handler (CaTopHandler): An instance of the top handler manager.
        :param calculator (CaTopCalculator): An instance of the top claculator manager.
        """
        
        self.core = core
        self.cfg = cfg
        self.handler = handler
        self.calculator = calculator


    def main(self, path: str = None, verbose: str = "y", **kwargs) -> None:
        """
        Main function to analyze data step by step.

          Options:
            --path    | TEXT | Path to the folder file containing the data (default: None).
            --verbose | TEXT | Enable or disable output messages (default: "y"; verbose: "1|y|yes|true", no-verbose: "any").
            **kwargs  | ARGS | Additional arguments passed to the internal execution commands.

          Example:
            crystal [cmd] --path path/to/data
            crystal [cmd] --path path/to/data --hand.read.verbose no
        """
        
        # Start analysis of data step by step using the command list
        isVerbose = str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}  
        if (isVerbose):
            print("Starting to process your data with the given crystal analysis.")
    
        # Look for a directory with data and unzip if needed
        handler_extract_name = self.core.register.find_command_name(self.handler.extract)
        handler_extract_args: Dict[str, Any] = {
            key[len(handler_extract_name) + 1:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith(handler_extract_name + ".")
        }
        if not (isVerbose):
            handler_extract_args["verbose"] = verbose[0]
        if not (path == None):
            handler_extract_args["path"] = path[0]
        data_folder_path = self.core.execute_command(
            command=handler_extract_name,
            command_args=handler_extract_args,
            commands=self.core.register.commands
        )
        
        # Look for a configuration file in the data folder
        # Load the configuration file if it exists in the data folder; otherwise, use the default path.
        cfg_find_name = self.core.register.find_command_name(self.cfg.find_config_file)
        cfg_find_args: Dict[str, Any] = {
            key[len(cfg_find_name) + 1:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith(cfg_find_name + ".")
        }
        if not (isVerbose):
            cfg_find_args["verbose"] = verbose[0]
        if not (data_folder_path == None):
            cfg_find_args["path"] = data_folder_path
        cfg_file = self.core.execute_command(
            command=cfg_find_name,
            command_args=cfg_find_args,
            commands=self.core.register.commands
        )
        
        # Upload the configuration file or proceed with default settings if not found
        cfg_upload_name = self.core.register.find_command_name(self.cfg.upload)
        cfg_upload_args: Dict[str, Any] = {
            key[len(cfg_upload_name) + 1:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith(cfg_upload_name + ".")
        }
        if not (isVerbose):
            cfg_upload_args["verbose"] = verbose[0]
        if not (cfg_file == None):
            cfg_upload_args["path"] = cfg_file
        self.core.execute_command(
            command=cfg_upload_name,
            command_args=cfg_upload_args,
            commands=self.core.register.commands
        )

        # Look inside the folder and load all data into data frames
        handler_read_name = self.core.register.find_command_name(self.handler.read)
        handler_read_args: Dict[str, Any] = {
            key[len(handler_read_name) + 1:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith(handler_read_name + ".")
        }
        if not (isVerbose):
            handler_read_args["verbose"] = verbose[0]
        if not (data_folder_path == None):
            handler_read_args["path"] = data_folder_path
        self.core.execute_command(
            command=handler_read_name,
            command_args=handler_read_args,
            commands=self.core.register.commands
        )
        
       # proccesing input table 
        calc_input_name = self.core.register.find_command_name(self.calculator.process_inputs)
        calc_input_args: Dict[str, Any] = {
            key[len(calc_input_name) + 1:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith(calc_input_name + ".")
        }
        if not (isVerbose):
            calc_input_args["verbose"] = verbose[0]
        self.core.execute_command(
            command=calc_input_name,
            command_args=calc_input_args,
            commands=self.core.register.commands
        )

        # proccessing profiles tables
        calc_profiles_name = self.core.register.find_command_name(self.calculator.process_profiles)
        calc_profiles_args: Dict[str, Any] = {
            key[len(calc_profiles_name) + 1:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith(calc_profiles_name + ".")
        }
        if not (isVerbose):
            calc_input_args["verbose"] = verbose[0]
        self.core.execute_command(
            command=calc_profiles_name,
            command_args=calc_profiles_args,
            commands=self.core.register.commands
        )

        
        # print data that was loaded and proccesed
        handler_print_name = self.core.register.find_command_name(self.handler.print)
        handler_print_args: Dict[str, Any] = {
            key[len(handler_print_name) + 1:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith(handler_print_name + ".")
        }
        if not (isVerbose):
            handler_read_args["verbose"] = verbose[0]
        self.core.execute_command(
            command=handler_print_name,
            command_args=handler_print_args,
            commands=self.core.register.commands
        )