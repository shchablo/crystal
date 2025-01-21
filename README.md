# CRYSTAL

**Calculation of Rates, Yield, and Stability of Avalanches in Locations** is an application designed for analyzing avalanche characteristics in specified locations.


## Installation


Update system packages

```bash
cd ~
sudo apt update
```

Install Python pip and essential build dependencies

```bash
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
```

Set up a Python virtual environment

```bash
sudo apt install python3.10-venv
python3 -m venv cold
source ~/cold/bin/activate
```

> Add virtual environment activation to .bashrc
> (Edit .bashrc to include the activation command)
>
> ```bash
> vim ~/.bashrc
> ```

Ensure Python and pip are properly installed

```bash
sudo apt update
sudo apt install python3
pip install build
```

Clone the project repository

```bash
git clone [repository]
cd path/to/crystal
```

Build and install the project package

```bash
python3 -m build
pip install dist/crystal-0.0.0-py3-none-any.whl
```
> Add the application binary to the system PATH
> ```bash
> export PATH=$PATH:/path/to/your/bin
> ```
## Before Start

For a list of available commands, run:

```bash
crystal man
```

For project tests using Crystal's built-in testing tools, run:

```bash
crystal test
```

For detailed help on a specific command, use:

```bash
crystal help --cmd [name]
```

## Input Data Formats

The program processes input data in the following formats:

- **Argis Data (input.csv)**: Spatial and geographical data.
- **Profiles Data (profiles)**: Data containing details about avalanches or terrain profiles.
- **Object List (objects.csv)**: A list of objects or locations to analyze.

```bash
|-- input.csv
|-- objects.csv
|-- profiles
       |-- 1.txt
       |-- 2.txt
       |-- ...
       |-- [name].txt
       |-- ...
       |-- n.txt
```

> Make sure your input data complies with the required format to ensure accurate results.

## Getting Started

1. **Interactive Mode**: Enter commands step-by-step during runtime.
2. **Command-Line Mode**: Execute predefined commands in a single line.


### Interactive Mode

Run the program and input commands step-by-step:

```bash
crystal
```

Once the program starts, you can type commands like:

```plaintext
>> man
>> help --cmd man
>> cfg.load --path /path/to/config.json
```


### Command-Line Mode

Run multiple actions in a single line. For examples:

```bash
crystal man
```

```bash
crystal cfg.load --path /path/to/config.json help --cmd cfg.gen cfg.gen --path /path/to/output/file/of/config.yaml
```

## Unit Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```


## Contribution & Contact

We welcome contributions to the [GitHub repository](https://github.com/shchablo/CRYSTAL.git)! Feel free to suggest features, fix bugs, or enhance the program.

- **Authors**: Konstantin Shchablo, Elizaveta Zhukova

For questions or support, don't hesitate to reach out.