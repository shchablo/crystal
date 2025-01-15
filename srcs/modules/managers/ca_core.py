import sys
import inspect
from typing import List, Dict, Any

from srcs.modules.managers.ca_parser import CaParser
from srcs.modules.managers.ca_configurator import CaConfigurator
from srcs.modules.managers.ca_register import CaRegister
from srcs.modules.managers.ca_test import ca_test


class CaCore:
    """
    The core class for managing command parsing, registration, and execution.
    """

    def __init__(self):
        """
        Initializes the core application with a parser, configurator, and register. Automatically registers default commands.
        """
        self.parser = CaParser()
        self.configurator = CaConfigurator()
        self.register = CaRegister(self.configurator)

        # Register default commands
        self.register.add_command("cfg.load", self.configurator.load_config)
        self.register.add_command("cfg.gen", self.register.generate_config_file)
        self.register.add_command(["man", "help"], self.register.help_command)
        self.register.add_command(["test"], ca_test)

    def execute_commands(self, parsed_commands: List[Dict[str, Any]], commands: Dict[str, Any]) -> None:
        """

        Executes a list of parsed commands with their arguments.

        :param parsed_commands (list): List of parsed commands and their arguments.
        :param commands (dict): A dictionary mapping command names to functions.

        """
        for command, command_args in parsed_commands:
            self.execute_command(command, command_args, commands)

    def execute_command(self, command: str, command_args: Dict[str, Any], commands: Dict[str, Any]) -> None:
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
        if accepts_kwargs:
            for key, value in command_args.items():
                kwargs[key] = value
        else:
            for param_name, param in func_signature.parameters.items():
                # Priority: Command arguments > Config file > Default value
                config_value = self.configurator.config.get(command, {}).get(param_name, param.default)
                kwargs[param_name] = command_args.get(param_name, config_value)

        try:
            func(**kwargs)
        except TypeError as e:
            print(f"Error executing command '{command}': {e}")

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
            # Interactive mode
            print("Interactive Mode. Type 'help' for a list of commands or 'exit' to quit.")
            while True:
                try:
                    user_input = input(">> ").strip()
                    if user_input.lower() in {"exit", "quit", ".q"}:
                        print("Exiting...")
                        break
                    if not user_input:
                        continue

                    # Parse and execute the user's input
                    args = user_input.split()
                    parsed_commands = self.parser.parse_commands(args, self.register.commands)
                    self.execute_commands(parsed_commands, self.register.commands)
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"An error occurred: {e}")