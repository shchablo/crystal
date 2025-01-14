import inspect
from pathlib import Path


class CaRegister:
    """
    A class to manage and register commands, provide help functionality, and generate configuration files.
    """

    def __init__(self, configurator):
        """

        Initializes the command registry with an empty command dictionary and a configurator.

        :param configurator (CaConfigurator): An instance of the configuration manager.

        """
        self.commands = {}
        self.configurator = configurator

    def add_command(self, name, func) -> None:
        """

        Registers a command or a list of commands with a corresponding function.

        :param name (str | list): The name(s) of the command(s) to register.
        :param func (callable): The function to associate with the command(s).

        """
        if isinstance(name, str):
            self.commands[name] = func
        elif isinstance(name, list) and all(isinstance(alias, str) for alias in name):
            for alias in name:
                self.commands[alias] = func
        else:
            raise TypeError("The command name must be a string or a list of strings.")

    def help_command(self, cmd: str = None) -> None:
        """

        Provides help for a specific command or lists all available commands.

        :param cmd: The name of the command to get help for. Defaults to None.

        """
        if cmd:
            if cmd in self.commands:
                doc = inspect.getdoc(self.commands[cmd])
                if doc:
                    print(f"Help for command '{cmd}':\n{doc}")
                else:
                    print(f"Command '{cmd}' does not have a description.")
            else:
                print(f"Command '{cmd}' not found.")
        else:
            print("Available commands:")
            for command, func in self.commands.items():
                doc = inspect.getdoc(func)
                description = doc.strip().splitlines()[0] if doc else "No description available."
                print(f"  {command}: {description}")
            print("\nUse 'help --cmd [name]' for detailed descriptions (ex: help --cmd cfg.load).")

    def generate_config_file(self, path: str = None) -> None:
        """

        Generates a configuration file based on registered commands and their signatures.

        :param path (str): The path to the output configuration file.

        """

        if not path:
            raise ValueError("Please provide the path to the output configuration file using --path.")

        generated_config = {}

        for command_name, func in self.commands.items():
            func_signature = inspect.signature(func)
            command_config = {}

            for param_name, param in func_signature.parameters.items():
                # Ignore parameters without a default value
                if param.default is inspect.Parameter.empty:
                   continue

                # Use value from the loaded config if it exists, otherwise use the default
                if (command_name in self.configurator.config and
                        param_name in self.configurator.config[command_name]):
                    command_config[param_name] = self.configurator.config[command_name][param_name]
                else:
                    command_config[param_name] = param.default

            generated_config[command_name] = command_config

        self.configurator.update_config(generated_config)
        self.configurator.upload_config(path)
        print(f"Configuration file successfully generated and saved to: {path}")