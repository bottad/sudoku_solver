# Sudoku Solver

This Python based Sudoku solver utilizes the [Wavefunction Collapse Algorithm](https://github.com/mxgmn/WaveFunctionCollapse) to solve any Sudoku. The Sudoku needs to be given in a .jason file as follows:
```
  7   | 5 8 3 |   2                [ 
  5 9 | 2     | 3                       [null, 7, null, 5, 8, 3, null, 2, null],
3 4   |     6 | 5   7                   [null, 5, 9, 2, null, null, 3, null, null],
------|-------|------                   [3, 4, null, null, null, 6, 5, null, 7],
7 9 5 |       | 6 3 2                   [7, 9, 5, null, null, null, 6, 3, 2],
    3 | 6 9 7 | 1           -->         [null, null, 3, 6, 9, 7, 1, null, null],  
6 8   |     2 | 7                       [6, 8, null, null, null, 2, 7, null, null],
------|-------|------                   [9, 1, 4, 8, 3, 5, null, 7, 6],
9 1 4 | 8 3 5 |   7 6                   [null, 3, null, 7, null, 1, 4, 9, 5],
  3   | 7   1 | 4 9 5                   [5, 6, 7, 4, 2, 9, null, 1, 3]
5 6 7 | 4 2 9 |   1 3               ]
```

For ease of use, you can simply fill in the corresponding numbers of your Sudoku in the [template file](boards/board_template.json).

Then, simply give the program the name of your Sudoku-board file when prompted to and the Sudoku will be solved.

---

## Setup Instructions

### 1. Install Python

Make sure you have Python 3.6 or later installed. You can check by running:

```bash
python --version
```

or

```bash
python3 --version
```

### 2. Install dependencies

This project requires the `colorama` package for colored terminal output.

You have two options to install the dependencies:

#### a) Install directly with `pip`

Run this command in your terminal or command prompt:

```bash
pip install -r requirements.txt
```

#### b) Use a virtual environment (recommended)

Create and activate a virtual environment:

```bash
python -m venv .venv
```

* On Windows:

```bash
.venv\Scripts\activate
```

* On macOS/Linux:

```bash
source .venv/bin/activate
```

Then install dependencies inside the virtual environment:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the solver script from the project directory like this:

```bash
python src/main.py [flags]
```

If you do **not** provide the board name flag, the program will prompt you to enter it manually. Enure that jor board file is saved in the [boards folder](boards/) and the board file is a .json file in the expected formatting. You can use the [template](boards/board_template.json) by copying it and filling in your given Sudoku.

---

### Flags

| Flag                 | Short | Description                                               | Default                                     |
|----------------------|-------|-----------------------------------------------------------|---------------------------------------------|
| `--name`             | `-n`  | Name of the Sudoku board file (without `.json` extension) | Will prompt if not provided                 |
| `--show-progress`    | `-p`  | Show the solving progress updates in the terminal         | Uses the default from settings.py (`False`) |
| `--delay`            | `-d`  | Delay in seconds between progress updates                 | Defaults to value in settings.py (0.5 sec). If set to `0.0`, the program will pause and wait for you to press Enter before proceeding to the next iteration.   |
---

### Examples

* Run solver, prompt for board name, no progress shown:

```bash
python main.py
```

* Run solver with board name and show progress with default delay:

```bash
python main.py -n board_2 -p
```

* Run solver with board name, show progress, and custom delay of 0.3 seconds:

```bash
python main.py -n board_2 -p -d 0.3
```

---

## Notes

* Your Sudoku board files should be placed in the `boards` folder and saved as JSON files, e.g., [board_1.json](boards/board_1.json).
* You can edit the provided [board\_template.json](boards/board_template.json) to create your own puzzles.
