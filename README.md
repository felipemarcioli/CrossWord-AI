# 🧩 Crossword AI — Constraint Satisfaction with AC-3 & Backtracking

![Python](https://img.shields.io/badge/python-3-blue.svg)
![Pillow](https://img.shields.io/badge/image_export-Pillow-green.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen.svg)

An AI crossword generator that fills a predefined grid using **Constraint Satisfaction Problems (CSPs)**, **AC-3 constraint propagation**, and **Backtracking Search** guided by variable and value ordering heuristics.

Developed as part of **Harvard's CS50's Introduction to Artificial Intelligence with Python course**.

---

## 💡 About the Project

Filling a crossword requires more than finding words of the right length. Every word must agree with the letters of intersecting words, and the same word cannot be used more than once.

This project models each horizontal or vertical word slot as a **variable**, with a **domain** of candidate words. The AI first removes incompatible candidates through node and arc consistency, then searches for a complete assignment that satisfies all constraints.

The program takes a grid structure and a vocabulary file as input, prints a solution to the terminal, and can optionally save it as an image. If no valid assignment exists, it prints `No solution.`

### Key Highlights:

- **Constraint-Based Modeling:** Represents word lengths, intersections, and word uniqueness as constraints.
- **Node Consistency:** Removes words whose lengths do not match their slots.
- **AC-3 Algorithm:** Propagates overlap constraints between neighboring variables before search.
- **Heuristic-Guided Search:** Uses Minimum Remaining Values (MRV), the degree heuristic, and Least Constraining Value (LCV) ordering.
- **Recursive Backtracking:** Explores consistent assignments and undoes choices when a branch cannot produce a solution.
- **Image Export:** Renders completed crosswords using Pillow.

---

## 🧠 How the Algorithm Works

### 1. Constraint Satisfaction Model

The crossword is represented by three components:

| Component       | Representation                                                                  |
| --------------- | ------------------------------------------------------------------------------- |
| **Variables**   | Horizontal and vertical word slots, each with a position, direction, and length |
| **Domains**     | Candidate words available for each slot                                         |
| **Constraints** | Correct word lengths, matching letters at intersections, and no repeated words  |

If variables `X` and `Y` overlap at character positions `i` and `j`, their assigned words must satisfy **`X[i] == Y[j]`**.

### 2. Node Consistency

`enforce_node_consistency()` filters each variable's domain by word length.

For example, a slot with **five cells** can only contain words with **five letters**. All other candidates are removed before checking intersections.

### 3. Arc Consistency — AC-3

`revise(x, y)` removes a candidate from `x` when no word in `y` matches its letter at their intersection.

The `ac3()` method repeatedly processes directed arcs between overlapping variables:

1. Revise the domain of `x` against `y`.
2. If the domain becomes empty, report failure.
3. If candidates were removed, add incoming arcs from the other neighbors of `x` for reconsideration.
4. Continue until no arcs remain to process.

This propagates local constraints across the grid and reduces the search space. Arc consistency alone does not guarantee a complete solution; backtracking handles the remaining choices.

### 4. Search Heuristics

The search uses three heuristics to decide which slot and word to try next:

| Heuristic | Decision | Purpose |
| --- | --- | --- |
| **Minimum Remaining Values (MRV)** | Choose the unassigned variable with the smallest domain | Prioritize slots with fewer candidates |
| **Degree Heuristic** | Break MRV ties by choosing the variable with the most overlapping neighbors | Prioritize slots connected to more constraints |
| **Least Constraining Value (LCV)** | Try words that rule out the fewest candidates in unassigned neighboring variables | Preserve more options for later assignments |

### 5. Backtracking Search

`backtrack(assignment)` recursively builds a solution:

1. Return the assignment if every variable has a word.
2. Select an unassigned variable using MRV and the degree heuristic.
3. Try candidate words in LCV order.
4. Check word lengths, uniqueness, and overlapping letters with `consistent()`.
5. Recurse if the assignment is consistent.
6. Undo the choice if the branch fails and try the next candidate.

In this implementation, **AC-3 runs before backtracking**. During recursive search, consistency checks validate each new assignment without rerunning AC-3.

---

## 🛠️ Built With

- **Language:** Python 3
- **Image Rendering:** Pillow — optional, required only for image export
- **Paradigms:** Object-Oriented Programming (OOP) / Constraint Satisfaction / Recursion
- **Algorithms:** AC-3 / Backtracking Search / MRV / Degree Heuristic / LCV

---

## 🚀 Getting Started

### Prerequisites

Ensure you have **Python 3** installed. Solving crosswords in the terminal requires no third-party packages.

### Installation & Execution

1. **Clone the repository:**

   ```bash
   git clone https://github.com/felipemarcioli/CrossWord-AI.git
   cd CrossWord-AI
   ```

2. **Set up a virtual environment (recommended for image export):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / macOS
   # Windows PowerShell: .\venv\Scripts\Activate.ps1
   ```

   If your system uses `python3`, replace `python` with `python3` in these commands.

3. **Generate a crossword in the terminal:**

   ```bash
   python generate.py data/structure0.txt data/words0.txt
   ```

4. **Optionally install Pillow and save the solution as an image:**

   ```bash
   python -m pip install Pillow
   python generate.py data/structure0.txt data/words0.txt crossword.png
   ```

Run the commands from the repository root so the image exporter can locate `assets/fonts/OpenSans-Regular.ttf`.

### Custom Puzzles

The command-line format is:

```bash
python generate.py structure words [output]
```

- **`structure`:** Path to a text file where `_` represents an open cell and other characters represent blocked cells.
- **`words`:** Path to a vocabulary file containing one word per line. Words are converted to uppercase when loaded.
- **`output`:** Optional image filename, such as `crossword.png`.

You can use the included files in `data/` or supply your own grid and vocabulary.

---

## 📁 Repository Structure

| Path                                     | Description                                                                                               |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| `generate.py`                            | CSP solver and command-line entry point; my implementation of the AI methods within the CS50 starter code |
| `crossword.py`                           | CS50-provided crossword representation, variable definitions, and overlap detection                       |
| `data/structure0.txt` – `structure2.txt` | Example crossword layouts                                                                                 |
| `data/words0.txt` – `words2.txt`         | Example vocabulary lists                                                                                  |
| `assets/fonts/OpenSans-Regular.ttf`      | Font used for image rendering                                                                             |
| `LICENSE`                                | MIT license                                                                                               |
| `README.md`                              | Project documentation                                                                                     |

---

## 📄 License

This project is licensed under the [MIT License](./LICENSE). Feel free to use, modify, and distribute it under the terms of the license.

---

## 📞 Contact

If you have any questions or would like to get in touch, feel free to email me at: felipemmarcioli@gmail.com

