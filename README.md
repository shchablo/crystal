# CRYSTAL

> **Calculation of Rate, Yield, and Stability of Avalanche in Location**

Crystal is an application designed for analyzing avalanche characteristics in specified location.


## Quick Start

For a list of available commands, run:

```bash
crystal help
```

For project tests using Crystal's built-in testing tools, run:

```bash
crystal test
```

For detailed help on a specific command, use:

```bash
crystal help --cmd [name]
```

Run multiple actions in a single line: 

```plaintext
crystal help --cmd cfg.load help --cmd cfg.gen
```

For examples: 

```plaintext
crystal cfg.load --path /path/to/input/config.json help --cmd cfg.gen cfg.gen --path /path/to/output/config.yaml
```

## Input Data Formats

The program processes input data in the following formats:

- **Argis Data (main.csv)**: Spatial and geographical data.
- **Profiles Data (profiles)**: Data containing details about avalanches or terrain profiles.
- **Object List (objects.csv)**: A list of objects or locations to analyze.

```plaintext
|-- main.csv
|-- objects.csv
|-- profiles
       |-- 1.csv
       |-- 2.csv
       |-- ...
       |-- [name].csv
       |-- ...
       |-- n.csv
```

> Make sure your input data complies with the required format to ensure accurate results.



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
```

Run virtual environment

```bash
source ~/cold/bin/activate
```

> Add virtual environment activation to .bashrc
> ```text
> vim ~/.bashrc
> ```

Install Python pip and essential build dependencies to virtual environment

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

## Unit Tests

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```


## Contribution & Contact

We welcome contributions to the [GitHub repository](https://github.com/shchablo/CRYSTAL.git)! Feel free to suggest features, fix bugs, or enhance the program.

- **Authors**: Konstantin Shchablo, Elizaveta Zhukova

For questions or support, don't hesitate to reach out.
