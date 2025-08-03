# Rubik's Cube Solver with Python GUI 🧩

This project is a Python-based 3×3 Rubik’s Cube simulator and solver that allows users to scramble, manually configure, visualize, and automatically solve a cube through an interactive GUI.

## 🔍 Features

- **Interactive GUI using Tkinter**
  - Real-time cube visualization
  - Manual face configuration (custom color inputs)
  - Button controls for scrambling, solving, and resetting

- **Smart Solver**
  - Uses **Breadth-First Search (BFS)** to compute the shortest sequence of moves to solve the cube
  - Solves most configurations in **under 2 seconds**

- **Manual Controls**
  - Apply moves like `U`, `R'`, `F2` manually
  - Accepts standard Rubik's Cube notation

- **Visual Output**
  - Clear visual feedback on the cube state before and after each move
  - Solving steps are displayed for user understanding

## 🚀 How to Run

### Requirements

- Python 3.7+
- No external dependencies required (built-in modules and Tkinter)

### To Launch the GUI:

```bash
python rubiks_solver.py
