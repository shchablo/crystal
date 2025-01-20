# CRYSTAL

**Calculation of Rates, Yield, and Stability of Avalanches in Locations** is an application designed for analyzing avalanche characteristics in specified locations.


## Installation


```bash
cd ~
sudo apt install -y python3-pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev
python3 -m venv cold
source crystal_venv/bin/activate
```
> add source crystal_venv/bin/activate at the end of `.bashrc`.
> ```bash
> vim ~/.bashrc
>```

```bash
sudo apt update
sudo apt install python3
pip install build
```


```bash
git clone [repository]
cd path/to/crystal
python3 -m build
pip install dist/crystal-0.0.0-py3-none-any.whl
```



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

## Extra

```bash
git stash
git pull
python3 -m build
pip install --force-reinstall --break-system-packages dist/crystal-0.5.0-py3-none-any.whl
```
