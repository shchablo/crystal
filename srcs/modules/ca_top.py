from typing import Dict, Any


class CaTop:

    def __init__(self, core):
        """

        Initializes the top-level class with entry points for various actions.

        :param core (CaCore): An instance of the core manager.

        """
        self.core = core

    def load_conf_and_generate_conf_wrapper(self, **kwargs) -> None:
        """
        Wrapper command to load the configuration and generate a configuration file.

        :param kwargs: Additional arguments to pass to the included commands.
        """

        print(kwargs)

        load_args: Dict[str, Any] = {
            key[5:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith("load_")
        }
        print("Executing 'cfg.load' command with arguments:", load_args)
        self.core.execute_command(
            command="cfg.load",
            command_args=load_args,
            commands=self.core.register.commands
        )

        gen_args: Dict[str, Any] = {
            key[4:]: value[0] if isinstance(value, list) else value
            for key, value in kwargs.items()
            if key.startswith("gen_")
        }
        print("Executing 'cfg.gen' command with arguments:", gen_args)
        self.core.execute_command(
            command="cfg.gen",
            command_args=gen_args,
            commands=self.core.register.commands
        )
