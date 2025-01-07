# CRYSTAL

**Calculation of Rates, Yield, and Stability of Avalanches in Locations** is an application designed for analyzing avalanche characteristics in specified locations. 


## Installation

```bash
python3 -m build
pip install --force-reinstall dist/crystal-0.1.0-py3-none-any.whl
```

## Before Start

For a list of available commands, run:

```bash
python crystal.py man
```

For detailed help on a specific command, use:

```bash
python crystal.py help --cmd <command_name>
```


## Quick Start

1. **Interactive Mode**: Enter commands step-by-step during runtime.
2. **Command-Line Mode**: Execute predefined commands in a single line.


### Interactive Mode

Run the program and input commands step-by-step:

```bash
python crystal.py
```

Once the program starts, you can type commands like:

```plaintext
>> man
>> help cfg
>> cfg --path /path/to/config.json
```

### Command-Line Mode

Run multiple actions in a single line. For example:

```bash
python crystal.py cfg --path /path/to/config.json help --cmd gen gen --path /path/to/output/file/of/config.json
```


## Input Data Formats

The program processes input data in the following formats:

- **Argis Data**: Spatial and geographical data.
- **Profiles Data**: Data containing details about avalanches or terrain profiles.
- **Object List**: A list of objects or locations to analyze.

Make sure your input data complies with the required format to ensure accurate results.


## Unit Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```


## Contribution & Contact

We welcome contributions to the [GitHub repository](https://github.com/shchablo/CRYSTAL.git)! Feel free to suggest features, fix bugs, or enhance the program.

- **Authors**: Konstantin Shchablo, Elizaveta Zhukova

For questions or support, don't hesitate to reach out.