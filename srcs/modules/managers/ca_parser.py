import inspect
from typing import List, Dict, Callable, Tuple, Any



class CaParser:
    """
    A class to parse commands and their arguments, ensuring compatibility with registered commands and their signatures.
    """


    def parse_commands(self, args: List[str], commands: Dict[str, Callable]) -> List[Tuple[str, Dict[str, Any]]]:
        """
        Parses commands and their arguments and returns a list of tuples with parsed arguments.

        :param args: A list of command-line arguments.
        :param commands: A dictionary mapping command names to their respective functions.

        :return list: A list of tuples where each tuple contains the command name and a dictionary of its parsed arguments.
        """

        parsed_commands = []
        current_command = None
        command_args = []

        for i, arg in enumerate(args):
            if arg in commands and not (i > 0 and args[i - 1].startswith("--")):
                # Process the previous command if present
                if current_command:
                    parsed_args = self._prepare_args(current_command, command_args, commands)
                    parsed_commands.append((current_command, parsed_args))
                current_command = arg
                command_args = []
            else:
                command_args.append(arg)

        # Add the last command and its arguments
        if current_command:
            parsed_args = self._prepare_args(current_command, command_args, commands)
            parsed_commands.append((current_command, parsed_args))

        return parsed_commands


    def _prepare_args(self, command: str, command_args: List[str], commands: Dict[str, Callable]) -> Dict[str, Any]:
        """
        Parses the arguments for a specific command.

        :param command: The command name.
        :param command_args: A list of arguments associated with the command.
        :param commands: A dictionary mapping command names to their respective functions.

        :return: A dictionary of parsed and validated arguments for the command.
        """
        if command not in commands:
            raise ValueError(f"Command '{command}' not found.")

        func = commands[command]
        func_signature = inspect.signature(func)

        accepts_kwargs = any(
            param.kind == inspect.Parameter.VAR_KEYWORD
            for param in func_signature.parameters.values()
        )

        # Parse arguments into a dictionary
        parsed_args = {}
        i = 0
        while i < len(command_args):
            arg = command_args[i]
            if arg.startswith("--"):  # Identify parameter names
                key = arg[2:]
                value = None
                # Check if a value follows the parameter name
                if i + 1 < len(command_args) and not command_args[i + 1].startswith("--"):
                    value = command_args[i + 1]
                    i += 1  # Skip the value in the next iteration
                parsed_args[key] = value
            i += 1

        # If the function accepts **kwargs, return parsed_args without filtering
        if accepts_kwargs:
            return {key: [value] for key, value in parsed_args.items()}

        # Otherwise, filter parsed_args based on the function's signature
        final_args = {}
        for param_name, param in func_signature.parameters.items():
            if param_name in parsed_args:
                value = parsed_args[param_name]
                if value is None and param.default is not inspect.Parameter.empty:
                    # Use default value if no value is provided
                    final_args[param_name] = param.default
                elif param.annotation != inspect.Parameter.empty:  # Convert type if specified
                    try:
                        final_args[param_name] = param.annotation(value)
                    except (ValueError, TypeError):
                        raise TypeError(f"Argument '{param_name}' must be of type {param.annotation}.")
                else:
                    final_args[param_name] = value

        return final_args