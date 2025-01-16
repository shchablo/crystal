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

        Display help for a specific command or list all commands.

          This command provides detailed help for a specified command if its name is given.
          If no command name is provided, it lists all available commands.

          Options:
            --cmd | TEXT | Name of the command to display help for (default: None).

          Example:
            crystal [cmd] --cmd man

        """
        if cmd:
            if cmd in self.commands:
                doc = inspect.getdoc(self.commands[cmd])
                if doc:
                    print(f"Help for command '{cmd}': {doc}")
                else:
                    print(f"Command '{cmd}' does not have a description.")
            else:
                print(f"Command '{cmd}' not found.")
        else:
            self._print_commands(self.commands)

    def _print_commands(self, commands):
        """
        Display a list of available commands with their descriptions.

        This function dynamically formats and displays a list of registered commands.
        Each command is aligned based on the longest command name and includes a brief description.
        If a command does not have a description, it is marked as "No description available."

        :param commands: dict, A dictionary where keys are command names and values are functions.

        :return: None
        """

        # Calculate the maximum command name length for alignment
        max_command_length = max(len(command) for command in commands.keys())
        header = f"{'Command':<{max_command_length}} : Description"
        separator = "-" * len(header)

        # Print header and separator
        print(header)
        print(separator)

        # Print each command with its description
        for command, func in commands.items():
            doc = inspect.getdoc(func)
            description = doc.strip().splitlines()[0] if doc else "No description available."
            print(f"{command:<{max_command_length}} : {description}")

        # Provide usage examples
        print("\nUsage:")
        print("  To view all available commands:")
        print("    crystal man")
        print("  To get detailed help for a specific command:")
        print("    crystal help --cmd [name]")

        print("\nExample:")
        print("  crystal help --cmd man")

    def generate_config_file(self, path: str = None) -> None:
        """

        Save the current configuration to a specified file.

          This command saves the current configuration to a file.
          It supports saving in JSON or YAML formats.
          Requires a valid file path as input.

          Options:
            --path | TEXT | Path to save the configuration file (e.g., output.json or output.yaml).

          Example:
            crystal [cmd] --path /path/to/output/file.json
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