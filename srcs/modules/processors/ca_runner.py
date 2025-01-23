import os
import zipfile
import pandas as pd
from typing import Optional, Dict, Any
from pathlib import Path



class CaTopRunner:


    def __init__(self, core, cfg, handler, calculator, plotter):
        """
        Initializes the top-level class with entry points for various actions.

        :param self.core (CaCore): An instance of the self.core manager.
        :param cfg (CaTopConfigurator): An instance of the top configurator manager.
        :param handler (CaTopHandler): An instance of the top handler manager.
        :param calculator (CaTopCalculator): An instance of the top claculator manager.
        :param plotter (CaTopPlotter): An instance of the plotter manager.
        """

        self.core = core
        self.cfg = cfg
        self.handler = handler
        self.calculator = calculator
        self.plotter = plotter


    def execute_command(self, command_obj, verbose, additional_args, **kwargs):
       is_verbose = str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}
       command_name = self.core.register.find_command_name(command_obj)
       command_args = {
           key[len(command_name) + 1:]: value[0] if isinstance(value, list) else value
           for key, value in kwargs.items()
           if key.startswith(command_name + ".")
       }
       if not is_verbose:
           command_args["verbose"] = verbose[0]
       if additional_args:
           command_args.update(additional_args)
       return self.core.execute_command(
           command=command_name,
           command_args=command_args,
           commands=self.core.register.commands
       )


    def main(self, path: str = None, list: str = "n", verbose: str = "y", **kwargs) -> None:
        """
        Main function to analyze data step by step.

          Options:
            --path    | TEXT | Path to the folder file containing the data (default: None).
            --verbose | TEXT | Enable or disable output messages (default: "y"; verbose: "1|y|yes|true", no-verbose: "any").
            --list    | TEXT | Show list of the commands that will execute (default: "n": 1|y|yes|true).
            **kwargs  | ARGS | Additional arguments passed to the internal execution commands.

          Example:
            crystal [cmd] --path path/to/data
            crystal [cmd] --path path/to/data --hand.read.verbose no
        """
        if str(list[0]).strip().lower() in {"1", "y", "yes", "true"}:
            cmds = []
            cmds.append(self.core.register.find_command_name(self.handler.extract))
            cmds.append(self.core.register.find_command_name(self.cfg.find_config_file))
            cmds.append(self.core.register.find_command_name(self.cfg.upload))
            cmds.append(self.core.register.find_command_name(self.handler.read))
            cmds.append(self.core.register.find_command_name(self.calculator.process_main))
            cmds.append(self.core.register.find_command_name(self.calculator.process_profiles))
            cmds.append(self.core.register.find_command_name(self.calculator.analysis_profiles))
            cmds.append(self.core.register.find_command_name(self.handler.print))
            cmds.append(self.core.register.find_command_name(self.plotter.all))
            cmds.append(self.core.register.find_command_name(self.handler.save_dfs_to_csv))
            
            print(cmds)
            
            return


        is_verbose = str(verbose[0]).strip().lower() in {"1", "y", "yes", "true"}
        if is_verbose:
            print("Welcome to the snow dance: a graceful performance of data processing and crystal-clear analysis.")

        # Look for a directory with data and unzip if needed
        data_folder_path = self.execute_command( self.handler.extract, verbose,
                                                 {"path": path[0]} if path else None, **kwargs )

        # Look for a configuration file in the data folder
        cfg_file = self.execute_command( self.cfg.find_config_file, verbose,
                                         {"path": data_folder_path} if data_folder_path else None, **kwargs )

        # Upload the configuration file
        self.execute_command( self.cfg.upload, verbose,
                              {"path": cfg_file} if cfg_file else None, **kwargs )

        # Load all data into data frames
        self.execute_command( self.handler.read, verbose,
                              {"path": data_folder_path} if data_folder_path else None, **kwargs )

        # Process input table
        self.execute_command(self.calculator.process_main, verbose, None, **kwargs)

        # Process profiles tables
        self.execute_command(self.calculator.process_profiles, verbose, None, **kwargs)

        # Process objects tables
        self.execute_command(self.calculator.analysis_profiles, verbose, None, **kwargs)

        # Print loaded and processed data
        self.execute_command(self.handler.print, verbose, None, **kwargs)

        # Plot results
        self.execute_command(self.plotter.all, verbose, None, **kwargs)

        # Save results
        self.execute_command(self.handler.save_dfs_to_csv, verbose, None, **kwargs)

        if is_verbose:
            print("Thank you for dancing with us in this enchanting blizzard of frost, ice and crystals.")

        return
