# CRYSTAL - Calculation of Rates, Yield, and Stability of Avalanches

## Requirements

- Python 3.7 or higher

## Data Formats

This program is designed to evaluate avalanches for a given object by providing the necessary input data. The input data must be provided in the following formats:

- **Argis data**
- **Profiles data**
- **Object list**

## Quick Start

The program is implemented as Python scripts following a paradigm where the necessary data must be provided first. Afterward, the program can process the data using specific commands for the required analysis. It supports two modes of operation:

1. **Command-Line Mode**: Process a set of commands and parameters directly via the command line.
2. **Interactive Mode**: Input commands step-by-step during runtime.

Before starting, please refer to the manual for detailed instructions:

```bash
python crystal.py man
```

### Command-Line Mode

Run multiple actions in one line:

```bash
python crystal.py extract --dir /path/to/dir1 plot --type profiles extract --dir /path/to/dir2 plot --type histograms
```

### Interactive Mode

Run the program and input commands step-by-step:

```bash
python crystal.py
```
## **Contact**

Author: **Zhukova, Shchablo**  
