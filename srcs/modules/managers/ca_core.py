import sys
import inspect
from typing import List, Dict, Any

from srcs.modules.managers.ca_parser import CaParser
from srcs.modules.managers.ca_configurator import CaConfigurator
from srcs.modules.managers.ca_register import CaRegister



class CaCore:
    """
    The core class for managing command parsing, registration, and execution.
    """


    def __init__(self):
        """
        Initializes the core application with a parser, configurator, and register.
        Automatically registers default commands.
        """

        self.parser = CaParser()
        self.configurator = CaConfigurator()
        self.register = CaRegister(self.configurator)


    def execute_commands(self, parsed_commands: List[Dict[str, Any]], commands: Dict[str, Any]) -> None:
        """
        Executes a list of parsed commands with their arguments.

        :param parsed_commands (list): List of parsed commands and their arguments.
        :param commands (dict): A dictionary mapping command names to functions.
        """

        for command, command_args in parsed_commands:
            self.execute_command(command, command_args, commands)

        return


    def execute_command(self, command: str, command_args: Dict[str, Any], commands: Dict[str, Any]) -> Any:
        """
        Executes a single command with its arguments.

        :param command: The name of the command to execute.
        :param command_args: A dictionary of arguments for the command.
        :param commands: A dictionary mapping command names to functions.
        """

        if command not in commands:
            print(f"Command '{command}' not found.")
            return

        func = commands[command]
        func_signature = inspect.signature(func)
        kwargs = {}

        # Build arguments for the function
        accepts_kwargs = any(
            param.kind == inspect.Parameter.VAR_KEYWORD
            for param in func_signature.parameters.values()
        )

        for param_name, param in func_signature.parameters.items():
            # Priority: Command arguments > Config file > Default value
            config_value = self.configurator.config.get(command, {}).get(param_name, param.default)
            kwargs[param_name] = command_args.get(param_name, config_value)

        if accepts_kwargs:
            for key, value in command_args.items():
                kwargs[key] = value

        try:
            result = func(**kwargs)
        except TypeError as e:
            print(f"Error executing command '{command}': {e}")

        return result

    def run(self) -> None:
        """
        Runs the core application. Supports both CLI and interactive modes.
        """

        if len(sys.argv) > 1:
            # Command-line mode
            args = sys.argv[1:]
            parsed_commands = self.parser.parse_commands(args, self.register.commands)
            self.execute_commands(parsed_commands, self.register.commands)
        else:
            print("Calculation of Rate, Yield, and Stability of Avalanche in Location.")
        return