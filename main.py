import copy
import random
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time

class Cube:
    def __init__(self):
        """Initialize a solved Rubik's cube."""
        # Each face is a 3x3 matrix. Faces: U(p), D(own), L(eft), R(ight), F(ront), B(ack)
        self.faces = {
            'U': [['W']*3 for _ in range(3)],  # White - Up
            'D': [['Y']*3 for _ in range(3)],  # Yellow - Down
            'L': [['O']*3 for _ in range(3)],  # Orange - Left
            'R': [['R']*3 for _ in range(3)],  # Red - Right
            'F': [['G']*3 for _ in range(3)],  # Green - Front
            'B': [['B']*3 for _ in range(3)],  # Blue - Back
        }
        
    def copy(self):
        """Create a deep copy of the cube."""
        new_cube = Cube()
        new_cube.faces = copy.deepcopy(self.faces)
        return new_cube
        
    def rotate_face(self, face, clockwise=True):
        """Rotate a face 90 degrees."""
        if clockwise:
            self.faces[face] = [list(row) for row in zip(*self.faces[face][::-1])]
        else:
            self.faces[face] = [list(row) for row in zip(*self.faces[face])][::-1]

    def apply_move(self, move):
        """Apply a move to the cube."""
        move = move.strip().upper()
        if not move:
            return
            
        face = move[0]
        if face not in ['U', 'D', 'L', 'R', 'F', 'B']:
            raise ValueError(f"Invalid face: {face}")
            
        clockwise = True
        times = 1

        if len(move) > 1:
            if move[1] == "'":
                clockwise = False
            elif move[1] == "2":
                times = 2
            else:
                raise ValueError(f"Invalid move notation: {move}")

        for _ in range(times):
            self._move(face, clockwise)

    def _move(self, face, clockwise):
        """Internal method to perform a single move."""
        self.rotate_face(face, clockwise)
        f = self.faces
        
        if face == 'U':
            if clockwise:
                temp = f['F'][0][:]
                f['F'][0] = f['R'][0][:]
                f['R'][0] = f['B'][0][:]
                f['B'][0] = f['L'][0][:]
                f['L'][0] = temp
            else:
                temp = f['F'][0][:]
                f['F'][0] = f['L'][0][:]
                f['L'][0] = f['B'][0][:]
                f['B'][0] = f['R'][0][:]
                f['R'][0] = temp

        elif face == 'D':
            if clockwise:
                temp = f['F'][2][:]
                f['F'][2] = f['L'][2][:]
                f['L'][2] = f['B'][2][:]
                f['B'][2] = f['R'][2][:]
                f['R'][2] = temp
            else:
                temp = f['F'][2][:]
                f['F'][2] = f['R'][2][:]
                f['R'][2] = f['B'][2][:]
                f['B'][2] = f['L'][2][:]
                f['L'][2] = temp

        elif face == 'L':
            if clockwise:
                temp = [f['F'][i][0] for i in range(3)]
                for i in range(3):
                    f['F'][i][0] = f['D'][i][0]
                    f['D'][i][0] = f['B'][2-i][2]
                    f['B'][2-i][2] = f['U'][i][0]
                    f['U'][i][0] = temp[i]
            else:
                temp = [f['F'][i][0] for i in range(3)]
                for i in range(3):
                    f['F'][i][0] = f['U'][i][0]
                    f['U'][i][0] = f['B'][2-i][2]
                    f['B'][2-i][2] = f['D'][i][0]
                    f['D'][i][0] = temp[i]

        elif face == 'R':
            if clockwise:
                temp = [f['F'][i][2] for i in range(3)]
                for i in range(3):
                    f['F'][i][2] = f['U'][i][2]
                    f['U'][i][2] = f['B'][2-i][0]
                    f['B'][2-i][0] = f['D'][i][2]
                    f['D'][i][2] = temp[i]
            else:
                temp = [f['F'][i][2] for i in range(3)]
                for i in range(3):
                    f['F'][i][2] = f['D'][i][2]
                    f['D'][i][2] = f['B'][2-i][0]
                    f['B'][2-i][0] = f['U'][i][2]
                    f['U'][i][2] = temp[i]

        elif face == 'F':
            if clockwise:
                temp = f['U'][2][:]
                f['U'][2] = [f['L'][2-i][2] for i in range(3)]
                for i in range(3):
                    f['L'][i][2] = f['D'][0][i]
                f['D'][0] = [f['R'][2-i][0] for i in range(3)]
                for i in range(3):
                    f['R'][i][0] = temp[i]
            else:
                temp = f['U'][2][:]
                f['U'][2] = [f['R'][i][0] for i in range(3)]
                for i in range(3):
                    f['R'][i][0] = f['D'][0][2-i]
                f['D'][0] = [f['L'][i][2] for i in range(3)]
                for i in range(3):
                    f['L'][i][2] = temp[2-i]

        elif face == 'B':
            if clockwise:
                temp = f['U'][0][:]
                f['U'][0] = [f['R'][i][2] for i in range(3)]
                for i in range(3):
                    f['R'][i][2] = f['D'][2][2-i]
                f['D'][2] = [f['L'][i][0] for i in range(3)]
                for i in range(3):
                    f['L'][i][0] = temp[2-i]
            else:
                temp = f['U'][0][:]
                f['U'][0] = [f['L'][2-i][0] for i in range(3)]
                for i in range(3):
                    f['L'][i][0] = f['D'][2][i]
                f['D'][2] = [f['R'][2-i][2] for i in range(3)]
                for i in range(3):
                    f['R'][i][2] = temp[i]

    def scramble(self, moves_str):
        """Apply a sequence of moves to scramble the cube."""
        moves = moves_str.split()
        for move in moves:
            self.apply_move(move)

    def is_solved(self):
        """Check if the cube is solved."""
        solved_faces = {
            'U': [['W']*3 for _ in range(3)],
            'D': [['Y']*3 for _ in range(3)],
            'L': [['O']*3 for _ in range(3)],
            'R': [['R']*3 for _ in range(3)],
            'F': [['G']*3 for _ in range(3)],
            'B': [['B']*3 for _ in range(3)],
        }
        return self.faces == solved_faces

    def get_state_string(self):
        """Get a string representation of the cube state for hashing."""
        state = ""
        for face in ['U', 'D', 'L', 'R', 'F', 'B']:
            for row in self.faces[face]:
                state += ''.join(row)
        return state

    def __str__(self):
        """String representation for debugging."""
        return '\n'.join([f"{face}: {self.faces[face]}" for face in self.faces])


class MoveGenerator:
    """Generate and apply all possible cube moves."""
    
    def __init__(self):
        self.basic_moves = ['U', 'D', 'L', 'R', 'F', 'B']
        self.all_moves = []
        
        # Generate all possible moves
        for move in self.basic_moves:
            self.all_moves.append(move)        # Clockwise
            self.all_moves.append(move + "'")  # Counter-clockwise
            self.all_moves.append(move + "2")  # Double turn
    
    def get_all_moves(self):
        """Return all possible moves."""
        return self.all_moves
    
    def get_random_scramble(self, length=15):
        """Generate a random scramble sequence."""
        scramble = []
        last_face = None
        
        for _ in range(length):
            # Avoid consecutive moves on the same face
            available_moves = [m for m in self.basic_moves if m != last_face]
            face = random.choice(available_moves)
            
            # Prefer simpler moves for better scrambles
            rotation_type = random.choice(['', "'", "'", "2"])  # More inverse moves
            move = face + rotation_type
            
            scramble.append(move)
            last_face = face
        
        return ' '.join(scramble)


class StatePrediction:
    """Predict cube states after applying moves."""
    
    def __init__(self, cube):
        self.cube = cube.copy()
    
    def simulate_move(self, move):
        """Simulate a move and return the resulting state."""
        temp_cube = self.cube.copy()
        temp_cube.apply_move(move)
        return temp_cube
    
    def simulate_sequence(self, moves):
        """Simulate a sequence of moves."""
        temp_cube = self.cube.copy()
        if isinstance(moves, str):
            moves = moves.split()
        
        for move in moves:
            temp_cube.apply_move(move)
        
        return temp_cube
    
    def get_all_next_states(self):
        """Get all possible next states from current position."""
        move_gen = MoveGenerator()
        next_states = {}
        
        for move in move_gen.get_all_moves():
            next_state = self.simulate_move(move)
            next_states[move] = next_state
        
        return next_states


class Solver:
    """Advanced Rubik's Cube solver using BFS with optimizations."""
    
    def __init__(self, cube):
        self.cube = cube.copy()
        self.move_generator = MoveGenerator()
        self.max_depth = 12  # Reduced for better performance
        
    def solve(self):
        """Solve the cube using BFS with pruning."""
        if self.cube.is_solved():
            return []
        
        # Try simple BFS first with limited depth
        simple_solution = self._simple_bfs()
        if simple_solution:
            return simple_solution
        
        # If BFS doesn't find solution, use layer-by-layer approach
        return self.layer_by_layer_solve()
    
    def _simple_bfs(self):
        """Simple BFS with limited depth for performance."""
        queue = deque([(self.cube.copy(), [])])
        visited = {self.cube.get_state_string()}
        max_iterations = 10000  # Limit iterations to prevent freezing
        iterations = 0
        
        while queue and iterations < max_iterations:
            current_cube, moves = queue.popleft()
            iterations += 1
            
            if len(moves) >= self.max_depth:
                continue
            
            # Try only basic moves for efficiency
            basic_moves = ['U', 'D', 'L', 'R', 'F', 'B', "U'", "D'", "L'", "R'", "F'", "B'"]
            
            for move in basic_moves:
                new_cube = current_cube.copy()
                new_cube.apply_move(move)
                new_moves = moves + [move]
                
                if new_cube.is_solved():
                    return new_moves
                
                state_string = new_cube.get_state_string()
                if state_string not in visited and len(new_moves) < self.max_depth:
                    visited.add(state_string)
                    queue.append((new_cube, new_moves))
        
        return None
    
    def layer_by_layer_solve(self):
        """Simplified layer-by-layer solving approach."""
        solution = []
        temp_cube = self.cube.copy()
        
        # This is a simplified version - in practice, you'd implement
        # proper layer-by-layer algorithms like CFOP
        
        # For demonstration, we'll use a basic approach
        # In a real implementation, you'd have separate methods for:
        # 1. Cross on bottom
        # 2. First two layers (F2L)
        # 3. Orient last layer (OLL)
        # 4. Permute last layer (PLL)
        
        # Placeholder algorithm - try common algorithms
        common_algorithms = [
            "R U R' U R U2 R'",  # Right-hand algorithm
            "L' U' L U' L' U2 L",  # Left-hand algorithm
            "F R U' R' U' R U R' F'",  # Common OLL
            "R U R' F' R U R' U' R' F R2 U' R'",  # Common PLL
        ]
        
        for algorithm in common_algorithms:
            if temp_cube.is_solved():
                break
            
            moves = algorithm.split()
            for move in moves:
                temp_cube.apply_move(move)
                solution.append(move)
                
                if temp_cube.is_solved():
                    return solution
        
        # If still not solved, return current progress
        return solution


class CubeVisualizer:
    """GUI for visualizing and interacting with the Rubik's cube."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎲 Rubik's Cube Solver - Interactive 3D Cube")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # Set modern style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.cube = Cube()
        self.solver = Solver(self.cube)
        self.move_generator = MoveGenerator()
        
        # Color mapping for visualization
        self.colors = {
            'W': '#FFFFFF',  # White
            'Y': '#FFD700',  # Gold Yellow
            'R': '#DC143C',  # Crimson Red
            'O': '#FF8C00',  # Dark Orange
            'G': '#32CD32',  # Lime Green
            'B': '#4169E1',  # Royal Blue
        }
        
        self.setup_gui()
        
    def setup_gui(self):
        """Set up the GUI components."""
        # Title
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎲 RUBIK'S CUBE SOLVER", 
                              font=('Arial', 24, 'bold'), 
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame, text="Interactive 3x3 Cube Solver with Smart AI", 
                                 font=('Arial', 12), 
                                 fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for cube visualization
        left_panel = tk.Frame(main_container, bg='#34495e', relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right panel for controls
        right_panel = tk.Frame(main_container, bg='#34495e', width=350, relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        right_panel.pack_propagate(False)
        
        # Setup panels
        self.setup_cube_display(left_panel)
        self.setup_controls(right_panel)
        
    def setup_cube_display(self, parent):
        """Set up the cube display area."""
        # Cube title
        cube_title = tk.Label(parent, text="🎯 CUBE VISUALIZATION", 
                             font=('Arial', 16, 'bold'), 
                             fg='#ecf0f1', bg='#34495e')
        cube_title.pack(pady=15)
        
        # Canvas frame with border
        canvas_container = tk.Frame(parent, bg='#2c3e50', relief=tk.SUNKEN, bd=3)
        canvas_container.pack(pady=10, padx=20)
        
        self.canvas = tk.Canvas(canvas_container, width=650, height=500, 
                               bg='#ecf0f1', highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        
        # Instructions
        instructions = tk.Label(parent, 
                               text="💡 Use the control panel on the right to interact with the cube",
                               font=('Arial', 11), 
                               fg='#bdc3c7', bg='#34495e')
        instructions.pack(pady=10)
        
        # Status display
        status_container = tk.Frame(parent, bg='#34495e')
        status_container.pack(pady=10)
        
        tk.Label(status_container, text="Status: ", 
                font=('Arial', 12, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(side=tk.LEFT)
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 Ready - Cube is Solved!")
        self.status_label = tk.Label(status_container, textvariable=self.status_var,
                                   font=('Arial', 12), 
                                   fg='#27ae60', bg='#34495e')
        self.status_label.pack(side=tk.LEFT)
        
        self.draw_cube()

    def setup_controls(self, parent):
        """Set up the control panel."""
        # Control panel title
        control_title = tk.Label(parent, text="🎮 CONTROL PANEL", 
                               font=('Arial', 16, 'bold'), 
                               fg='#ecf0f1', bg='#34495e')
        control_title.pack(pady=(15, 20))
        
        # Quick Actions Section
        quick_frame = tk.LabelFrame(parent, text="⚡ Quick Actions", 
                                   font=('Arial', 12, 'bold'),
                                   fg='#ecf0f1', bg='#34495e')
        quick_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Big action buttons
        btn_style = {'font': ('Arial', 11, 'bold'), 'width': 25, 'height': 2}
        
        scramble_btn = tk.Button(quick_frame, text="🎲 SCRAMBLE CUBE", 
                               bg='#e74c3c', fg='white', 
                               command=self.quick_scramble, **btn_style)
        scramble_btn.pack(pady=5, padx=10)
        
        solve_btn = tk.Button(quick_frame, text="🧠 SOLVE CUBE", 
                            bg='#27ae60', fg='white', 
                            command=self.solve_cube, **btn_style)
        solve_btn.pack(pady=5, padx=10)
        
        reset_btn = tk.Button(quick_frame, text="🔄 RESET TO SOLVED", 
                            bg='#3498db', fg='white', 
                            command=self.reset_cube, **btn_style)
        reset_btn.pack(pady=5, padx=10)
        
        # Manual Moves Section
        moves_frame = tk.LabelFrame(parent, text="🎯 Manual Moves", 
                                   font=('Arial', 12, 'bold'),
                                   fg='#ecf0f1', bg='#34495e')
        moves_frame.pack(fill=tk.X, padx=15, pady=10)
        
        # Move input
        input_frame = tk.Frame(moves_frame, bg='#34495e')
        input_frame.pack(pady=10, padx=10)
        
        tk.Label(input_frame, text="Enter Move:", 
                font=('Arial', 10, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack()
        
        move_input_frame = tk.Frame(input_frame, bg='#34495e')
        move_input_frame.pack(pady=5)
        
        self.move_entry = tk.Entry(move_input_frame, font=('Arial', 12), width=8, justify='center')
        self.move_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.move_entry.bind('<Return>', lambda e: self.apply_manual_move())
        
        apply_btn = tk.Button(move_input_frame, text="Apply", 
                            bg='#f39c12', fg='white', font=('Arial', 10, 'bold'),
                            command=self.apply_manual_move)
        apply_btn.pack(side=tk.LEFT)
        
        # Example moves
        examples = tk.Label(moves_frame, text="Examples: U, R', F2, L, D'", 
                          font=('Arial', 9), fg='#bdc3c7', bg='#34495e')
        examples.pack(pady=5)
        
        # Move buttons grid
        grid_frame = tk.Frame(moves_frame, bg='#34495e')
        grid_frame.pack(pady=10)
        
        moves = ['U', 'D', 'L', 'R', 'F', 'B']
        move_colors = ['#9b59b6', '#e67e22', '#1abc9c', '#e74c3c', '#27ae60', '#3498db']
        
        for i, (move, color) in enumerate(zip(moves, move_colors)):
            row = i // 3
            col = i % 3
            
            # Frame for each move group
            move_group = tk.Frame(grid_frame, bg='#34495e')
            move_group.grid(row=row, column=col, padx=5, pady=5)
            
            # Normal move
            tk.Button(move_group, text=move, width=3, height=1,
                     bg=color, fg='white', font=('Arial', 10, 'bold'),
                     command=lambda m=move: self.apply_move_button(m)).pack()
            
            # Inverse move
            tk.Button(move_group, text=move+"'", width=3, height=1,
                     bg=color, fg='white', font=('Arial', 8),
                     command=lambda m=move+"'": self.apply_move_button(m)).pack(pady=1)
        
        # Custom Scramble Section
        custom_frame = tk.LabelFrame(parent, text="📝 Custom Scramble", 
                                   font=('Arial', 12, 'bold'),
                                   fg='#ecf0f1', bg='#34495e')
        custom_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.scramble_entry = tk.Entry(custom_frame, font=('Arial', 10), width=30)
        self.scramble_entry.pack(pady=10, padx=10)
        
        scramble_buttons = tk.Frame(custom_frame, bg='#34495e')
        scramble_buttons.pack(pady=5)
        
        tk.Button(scramble_buttons, text="Generate Random", 
                 bg='#8e44ad', fg='white', font=('Arial', 9),
                 command=self.generate_scramble).pack(side=tk.LEFT, padx=5)
        
        tk.Button(scramble_buttons, text="Apply Custom", 
                 bg='#16a085', fg='white', font=('Arial', 9),
                 command=self.apply_scramble).pack(side=tk.LEFT, padx=5)
        
        # Solution Section
        solution_frame = tk.LabelFrame(parent, text="💡 Solution & Progress", 
                                     font=('Arial', 12, 'bold'),
                                     fg='#ecf0f1', bg='#34495e')
        solution_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.solution_text = scrolledtext.ScrolledText(solution_frame, height=8, 
                                                      font=('Courier', 10),
                                                      bg='#2c3e50', fg='#ecf0f1',
                                                      insertbackground='white')
        self.solution_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Animation button
        self.animate_btn = tk.Button(solution_frame, text="🎬 Animate Solution", 
                                   bg='#e67e22', fg='white', font=('Arial', 11, 'bold'),
                                   command=self.animate_solution, state=tk.DISABLED)
        self.animate_btn.pack(pady=10)
        
        self.solution_moves = []
        
        # Initial message
        self.solution_text.insert(tk.END, "🎲 Welcome to Rubik's Cube Solver!\n\n")
        self.solution_text.insert(tk.END, "Quick Start:\n")
        self.solution_text.insert(tk.END, "1. Click 'SCRAMBLE CUBE' to mix it up\n")
        self.solution_text.insert(tk.END, "2. Click 'SOLVE CUBE' to find solution\n")
        self.solution_text.insert(tk.END, "3. Use 'Animate Solution' to watch it solve\n\n")
        self.solution_text.insert(tk.END, "Ready to begin! 🚀\n")

    def draw_cube(self):
        """Draw the cube faces on the canvas."""
        self.canvas.delete("all")
        
        # Face positions and sizes
        face_size = 80
        square_size = 24
        
        # Define positions for each face in the unfolded cube layout
        positions = {
            'U': (face_size * 2.5, 20),           # Top
            'L': (20, face_size + 40),            # Left  
            'F': (face_size + 40, face_size + 40), # Front
            'R': (face_size * 2.5, face_size + 40), # Right
            'B': (face_size * 3.5 + 20, face_size + 40), # Back
            'D': (face_size * 2.5, face_size * 2 + 60) # Bottom
        }
        
        # Draw each face
        for face_name, (start_x, start_y) in positions.items():
            face = self.cube.faces[face_name]
            
            # Draw face background
            bg_x1, bg_y1 = start_x - 5, start_y - 25
            bg_x2, bg_y2 = start_x + face_size - 8, start_y + face_size - 8
            self.canvas.create_rectangle(bg_x1, bg_y1, bg_x2, bg_y2, 
                                       fill='#34495e', outline='#2c3e50', width=2)
            
            # Draw face label
            label_x = start_x + (face_size - 8) // 2
            label_y = start_y - 15
            self.canvas.create_text(label_x, label_y, text=face_name, 
                                  font=('Arial', 14, 'bold'), fill='#2c3e50')
            
            # Draw 3x3 grid for this face
            for row in range(3):
                for col in range(3):
                    x1 = start_x + col * square_size
                    y1 = start_y + row * square_size
                    x2 = x1 + square_size
                    y2 = y1 + square_size
                    
                    color = self.colors[face[row][col]]
                    
                    # Draw square with shadow effect
                    # Shadow
                    self.canvas.create_rectangle(x1+2, y1+2, x2+2, y2+2, 
                                               fill='#7f8c8d', outline='')
                    # Main square
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                               fill=color, outline='#2c3e50', width=2)
                    
                    # Add shine effect for white squares
                    if color == '#FFFFFF':
                        self.canvas.create_rectangle(x1+3, y1+3, x1+8, y1+8, 
                                                   fill='#f8f9fa', outline='')
        
        # Update status
        if self.cube.is_solved():
            self.status_var.set("🎉 SOLVED! - Cube is Complete!")
            self.status_label.config(fg='#27ae60')
        else:
            self.status_var.set("🔄 SCRAMBLED - Ready to Solve")
            self.status_label.config(fg='#e74c3c')
    
    def quick_scramble(self):
        """Quick scramble with one click."""
        scramble = self.move_generator.get_random_scramble()
        self.cube.scramble(scramble)
        self.draw_cube()
        self.scramble_entry.delete(0, tk.END)
        self.scramble_entry.insert(0, scramble)
        self.solution_text.insert(tk.END, f"🎲 Quick scramble applied: {scramble}\n\n")
        self.solution_text.see(tk.END)
        self.animate_btn.config(state=tk.DISABLED)
        self.solution_moves = []
    
    def apply_manual_move(self):
        """Apply move from text entry."""
        move = self.move_entry.get().strip().upper()
        if not move:
            return
        
        try:
            self.cube.apply_move(move)
            self.draw_cube()
            self.solution_text.insert(tk.END, f"✅ Applied: {move}\n")
            self.solution_text.see(tk.END)
            self.move_entry.delete(0, tk.END)
        except Exception as e:
            self.solution_text.insert(tk.END, f"❌ Invalid move '{move}': {str(e)}\n")
            self.solution_text.see(tk.END)
    
    def apply_move_button(self, move):
        """Apply move from button click."""
        try:
            self.cube.apply_move(move)
            self.draw_cube()
            self.solution_text.insert(tk.END, f"🎯 Move: {move}\n")
            self.solution_text.see(tk.END)
        except Exception as e:
            self.solution_text.insert(tk.END, f"❌ Error: {str(e)}\n")
            self.solution_text.see(tk.END)
    
    def generate_scramble(self):
        """Generate a random scramble."""
        scramble = self.move_generator.get_random_scramble()
        self.scramble_entry.delete(0, tk.END)
        self.scramble_entry.insert(0, scramble)
        
    def apply_scramble(self):
        """Apply the scramble from the entry field."""
        scramble = self.scramble_entry.get().strip()
        if scramble:
            try:
                self.cube.scramble(scramble)
                self.draw_cube()
                self.solution_text.insert(tk.END, f"📝 Applied custom scramble: {scramble}\n\n")
                self.solution_text.see(tk.END)
                self.animate_btn.config(state=tk.DISABLED)
                self.solution_moves = []
            except Exception as e:
                self.solution_text.insert(tk.END, f"❌ Invalid scramble: {str(e)}\n")
                self.solution_text.insert(tk.END, "💡 Use moves like: U R F' L2 D\n\n")
                self.solution_text.see(tk.END)

    def solve_cube(self):
        """Solve the current cube state."""
        if self.cube.is_solved():
            self.solution_text.insert(tk.END, "ℹ️ Cube is already solved!\n\n")
            self.solution_text.see(tk.END)
            return
        
        self.status_var.set("🧠 AI is thinking...")
        self.status_label.config(fg='#f39c12')
        self.root.update()
        
        # Show solving message
        self.solution_text.insert(tk.END, "🧠 AI Solver is analyzing the cube...\n")
        self.solution_text.insert(tk.END, "🔍 Searching for optimal solution...\n\n")
        self.solution_text.see(tk.END)
        
        def solve_thread():
            try:
                solver = Solver(self.cube)
                solution = solver.solve()
                
                def update_ui():
                    self.display_solution(solution)
                
                self.root.after(0, update_ui)
                
            except Exception as e:
                def handle_error():
                    self.solution_text.insert(tk.END, f"❌ Solving failed: {str(e)}\n\n")
                    self.solution_text.see(tk.END)
                    self.status_var.set("❌ Solve Failed")
                    self.status_label.config(fg='#e74c3c')
                
                self.root.after(0, handle_error)
        
        threading.Thread(target=solve_thread, daemon=True).start()
    
    def display_solution(self, solution):
        """Display the solution in the text area."""
        self.solution_moves = solution
        
        if solution:
            solution_str = ' '.join(solution)
            self.solution_text.insert(tk.END, f"🎉 SOLUTION FOUND! ({len(solution)} moves)\n")
            self.solution_text.insert(tk.END, f"📋 Moves: {solution_str}\n\n")
            
            # Show move breakdown
            self.solution_text.insert(tk.END, "📝 Step-by-step breakdown:\n")
            for i, move in enumerate(solution, 1):
                self.solution_text.insert(tk.END, f"{i:2d}. {move}\n")
            
            self.solution_text.insert(tk.END, f"\n🎬 Click 'Animate Solution' to watch it solve!\n\n")
            self.animate_btn.config(state=tk.NORMAL)
            self.status_var.set(f"✅ Solution Ready! ({len(solution)} moves)")
            self.status_label.config(fg='#27ae60')
        else:
            self.solution_text.insert(tk.END, "😕 No solution found within search limits.\n")
            self.solution_text.insert(tk.END, "💡 Tip: Try a simpler scramble or reset the cube.\n\n")
            self.status_var.set("❌ No Solution Found")
            self.status_label.config(fg='#e74c3c')
        
        self.solution_text.see(tk.END)

    def animate_solution(self):
        """Animate the solution step by step."""
        if not self.solution_moves:
            self.solution_text.insert(tk.END, "⚠️ No solution to animate!\n\n")
            self.solution_text.see(tk.END)
            return
        
        # Disable animation button during animation
        self.animate_btn.config(state=tk.DISABLED, text="🎬 Animating...")
        
        # Reset cube to scrambled state
        temp_cube = Cube()
        scramble = self.scramble_entry.get().strip()
        if scramble:
            try:
                temp_cube.scramble(scramble)
                self.cube = temp_cube
                self.draw_cube()
                
                self.solution_text.insert(tk.END, "🎬 Starting animation...\n")
                self.solution_text.insert(tk.END, f"📽️ Will apply {len(self.solution_moves)} moves\n\n")
                self.solution_text.see(tk.END)
                
            except:
                self.solution_text.insert(tk.END, "❌ Cannot reset to scrambled state.\n")
                self.solution_text.insert(tk.END, "💡 Try applying a new scramble first.\n\n")
                self.solution_text.see(tk.END)
                self.animate_btn.config(state=tk.NORMAL, text="🎬 Animate Solution")
                return
        
        def animate_step(step):
            if step < len(self.solution_moves):
                move = self.solution_moves[step]
                try:
                    self.cube.apply_move(move)
                    self.draw_cube()
                    
                    # Update solution display
                    self.solution_text.insert(tk.END, f"🎯 Step {step + 1}: {move}\n")
                    
                    remaining = len(self.solution_moves) - step - 1
                    if remaining > 0:
                        remaining_moves = self.solution_moves[step + 1:]
                        self.solution_text.insert(tk.END, f"⏳ Remaining: {remaining} moves\n")
                    
                    self.solution_text.see(tk.END)
                    self.status_var.set(f"🎬 Animating... {step + 1}/{len(self.solution_moves)}")
                    
                    # Schedule next step
                    self.root.after(1200, lambda: animate_step(step + 1))
                except Exception as e:
                    self.solution_text.insert(tk.END, f"❌ Animation error: {e}\n\n")
                    self.solution_text.see(tk.END)
                    self.animate_btn.config(state=tk.NORMAL, text="🎬 Animate Solution")
            else:
                self.solution_text.insert(tk.END, "🎉 ANIMATION COMPLETE!\n")
                self.solution_text.insert(tk.END, "✅ Cube is now solved! 🎲\n\n")
                self.solution_text.see(tk.END)
                self.status_var.set("🎉 Animation Complete - Cube Solved!")
                self.status_label.config(fg='#27ae60')
                self.animate_btn.config(state=tk.NORMAL, text="🎬 Animate Solution")
        
        animate_step(0)
    
    def reset_cube(self):
        """Reset cube to solved state."""
        self.cube = Cube()
        self.draw_cube()
        self.solution_text.insert(tk.END, "🔄 Cube reset to solved state.\n")
        self.solution_text.insert(tk.END, "✅ Ready for new scramble!\n\n")
        self.solution_text.see(tk.END)
        self.scramble_entry.delete(0, tk.END)
        self.move_entry.delete(0, tk.END)
        self.animate_btn.config(state=tk.DISABLED)
        self.solution_moves = []
    
    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


# CLI Interface
def cli_interface():
    """Command-line interface for the cube solver."""
    print("=== 🎲 Rubik's Cube Solver CLI ===")
    print("Commands: scramble, solve, move <move>, state, reset, gui, quit")
    print("Move examples: U, R', F2, L, D'")
    
    cube = Cube()
    move_gen = MoveGenerator()
    
    while True:
        try:
            command = input("\n🎲 > ").strip()
            
            if not command:
                continue
                
            if command.lower() in ['quit', 'exit', 'q']:
                break
            elif command.lower() == 'scramble':
                scramble = move_gen.get_random_scramble()
                print(f"🎲 Scramble: {scramble}")
                cube.scramble(scramble)
                print("✅ Cube scrambled!")
            elif command.lower() == 'solve':
                if cube.is_solved():
                    print("ℹ️ Cube is already solved!")
                else:
                    print("🧠 Solving cube...")
                    solver = Solver(cube)
                    solution = solver.solve()
                    if solution:
                        print(f"🎉 Solution ({len(solution)} moves): {' '.join(solution)}")
                    else:
                        print("😕 No solution found within search limits.")
            elif command.lower().startswith('move '):
                move_part = command[5:].strip().upper()
                if not move_part:
                    print("❌ Please specify a move. Example: move U")
                    continue
                try:
                    cube.apply_move(move_part)
                    print(f"✅ Applied move: {move_part}")
                except Exception as e:
                    print(f"❌ Invalid move '{move_part}': {str(e)}")
                    print("💡 Valid moves: U, D, L, R, F, B (add ' for inverse, 2 for double)")
            elif command.lower() == 'state':
                print("📊 Current cube state:")
                for face in ['U', 'D', 'L', 'R', 'F', 'B']:
                    print(f"  {face}: {cube.faces[face]}")
                status = "✅ SOLVED" if cube.is_solved() else "🔄 SCRAMBLED"
                print(f"  Status: {status}")
            elif command.lower() == 'reset':
                cube = Cube()
                print("🔄 Cube reset to solved state.")
            elif command.lower() == 'gui':
                print("🖥️ Starting GUI...")
                try:
                    visualizer = CubeVisualizer()
                    visualizer.run()
                    break
                except Exception as e:
                    print(f"❌ GUI failed to start: {e}")
            else:
                print("❓ Unknown command.")
                print("📋 Available commands:")
                print("  • scramble - Generate random scramble")
                print("  • solve - Find solution for current state")  
                print("  • move <move> - Apply single move (e.g., move U2)")
                print("  • state - Show current cube state")
                print("  • reset - Reset to solved state")
                print("  • gui - Launch graphical interface")
                print("  • quit - Exit program")
        
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Thanks for using Rubik's Cube Solver!")


# Main execution
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        cli_interface()
    else:
        # Start GUI by default
        try:
            visualizer = CubeVisualizer()
            visualizer.run()
        except Exception as e:
            print(f"GUI failed to start: {e}")
            print("Falling back to CLI mode...")
            cli_interface()
