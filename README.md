# opendatastructures-python

Personal implementations, notes, and experiments based on Pat Morin's *Open Data Structures – Pseudocode Edition*. Started in September 2026, working through the book at a slow but steady pace.

Unit tests will be added in time...

### Open Datastructures - Pseudocode Edition (0.1Gβ)
| Chapter | Contents                                       |
|---------|------------------------------------------------|
| 1       | Introduction, notation, running time models    |
| 2       | Array-Based Lists                              |
| 3       | Linked lists                                   |
| 4       | Skiplists                                      |
| 5       | Hash tables                                    |
| 6       | Binary trees                                   |
| 7       | Random Binary Search Trees                     |
| 8       | Scapegoat Trees                                |
| 9       | Red-black Trees                                |
| 10      | Heaps                                          |
| 11      | Sorting Algorithms                             |
| 12      | Graphs                                         |
| 13      | Data Structures for Integers                   |
| 14      | External Memory Searching                      |


## Requirements

- Python >= 3.10

Runtime dependencies (installed automatically):

- numpy >= 1.26.4
- pandas >= 2.3.1
- matplotlib >= 3.10.5

## Installation

The notebooks import the source code like any other package, so first
set up a virtual environment and install the project in editable mode:

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# .venv\Scripts\activate       # Windows

# 2. Install as an editable package (dependencies are pulled from pyproject.toml)
pip install -e .
```

## Pre-commit hooks
The repo uses pre-commit with the following hooks:

- General checks – YAML/TOML validation, merge conflict detection, end-of-file fixer, trailing whitespace removal
- isort (black profile) – sorts imports into correct order
- toml-sort – sorts keys in TOML files
- ruff – linting (ruff-check --fix) and formatting (ruff-format, the modern replacement for black)

Run manually on all files:
```bash
pre-commit run --all-files
```
