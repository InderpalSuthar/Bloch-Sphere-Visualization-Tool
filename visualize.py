import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from qutip import Bloch, Qobj

class QubitSimulator:
    def __init__(self, master):
        self.master = master
        self.master.title("Qubit Challenge Mode")
        self.master.configure(bg="#2E2E2E")

        self.state = np.array([1, 0])  # Initial state |0>
        self.history = []

        self.setup_gui()
        self.update_bloch_sphere()

    def setup_gui(self):
        # Create a PanedWindow to organize the layout
        self.paned_window = tk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left Panel for buttons and timeline
        self.left_panel = tk.Frame(self.paned_window, width=300, bg="#2E2E2E")
        self.paned_window.add(self.left_panel)

        # Menu Bar
        menubar = tk.Menu(self.master, bg="#2E2E2E", fg="white")
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0, bg="#2E2E2E", fg="white")
        menubar.add_cascade(label="Menu", menu=file_menu)
        file_menu.add_command(label="Tutorial", command=self.show_tutorial, background="#3A3A3A", foreground="white")
        file_menu.add_command(label="Gate Challenge", command=self.show_gate_challenge, background="#3A3A3A", foreground="white")
        file_menu.add_command(label="Pulse Challenge", command=self.show_pulse_challenge, background="#3A3A3A", foreground="white")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit, background="#3A3A3A", foreground="white")

        # Horizontal Button Frame
        self.button_frame = tk.Frame(self.left_panel, bg="#2E2E2E")
        self.button_frame.pack(pady=10, padx=10)

        # Gate Buttons with Colors, Size Adjustments, and Rounded Edges
        self.x_button = tk.Button(self.button_frame, text="X-Gate", command=self.apply_x_gate, bg="#1E3A5F", fg="white", font=('Arial', 10, 'bold'), relief="groove", bd=2, highlightbackground="black", width=12, height=2, padx=10, pady=5)
        self.x_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.y_button = tk.Button(self.button_frame, text="Y-Gate", command=self.apply_y_gate, bg="#1E3A5F", fg="white", font=('Arial', 10, 'bold'), relief="groove", bd=2, highlightbackground="black", width=12, height=2, padx=10, pady=5)
        self.y_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.h_button = tk.Button(self.button_frame, text="Hadamard Gate", command=self.apply_h_gate, bg="#1E3A5F", fg="white", font=('Arial', 10, 'bold'), relief="groove", bd=2, highlightbackground="black", width=18, height=2, padx=10, pady=5)
        self.h_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        # Undo and Clear Buttons with Rounded Edges
        self.undo_button = tk.Button(self.button_frame, text="Undo", command=self.undo_last_operation, bg="#1E3A5F", fg="white", font=('Arial', 10, 'bold'), relief="groove", bd=2, highlightbackground="black", width=12, height=2, padx=10, pady=5)
        self.undo_button.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.clear_button = tk.Button(self.button_frame, text="Clear", command=self.clear_timeline, bg="#1E3A5F", fg="white", font=('Arial', 10, 'bold'), relief="groove", bd=2, highlightbackground="black", width=12, height=2, padx=10, pady=5)
        self.clear_button.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Timeline Section
        self.timeline_label = tk.Label(self.left_panel, text="Operation Timeline", font=('Arial', 12, 'bold'), bg="#2E2E2E", fg="white")
        self.timeline_label.pack(pady=10)

        self.timeline_text = tk.Text(self.left_panel, width=50, height=10, font=('Arial', 10), bg="#3A3A3A", fg="white")
        self.timeline_text.pack(pady=10)
        self.timeline_text.tag_configure('bold', font=('Arial', 10, 'bold'))

        # Right Panel for Bloch Sphere
        self.right_panel = tk.Frame(self.paned_window, bg='black')
        self.paned_window.add(self.right_panel, stretch="always")

        self.fig = plt.figure(figsize=(6, 6))  # Adjust the figure size here
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])
        self.ax.set_zlim([-1, 1])
        self.ax.view_init(azim=60, elev=30)  # Set view angle to focus on the upper quadrant

        self.bloch_sphere = Bloch(fig=self.fig)
        self.bloch_sphere.add_states([Qobj(self.state)])

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_bloch_sphere(self):
        self.bloch_sphere.clear()
        self.plot_state(self.state)
        self.bloch_sphere.render()
        self.canvas.draw()

    def plot_state(self, state):
        psi = Qobj(state)
        self.bloch_sphere.add_states([psi])

    def apply_x_gate(self):
        x_gate = np.array([[0, 1], [1, 0]])
        self.state = np.dot(x_gate, self.state)
        self.history.append(('X-Gate', self.state.copy()))  # Store operation with state
        self.update_bloch_sphere()
        self.update_timeline()

    def apply_y_gate(self):
        y_gate = np.array([[0, -1j], [1j, 0]])
        self.state = np.dot(y_gate, self.state)
        self.history.append(('Y-Gate', self.state.copy()))  # Store operation with state
        self.update_bloch_sphere()
        self.update_timeline()

    def apply_h_gate(self):
        h_gate = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        self.state = np.dot(h_gate, self.state)
        self.history.append(('Hadamard Gate', self.state.copy()))  # Store operation with state
        self.update_bloch_sphere()
        self.update_timeline()

    def undo_last_operation(self):
        if self.history:
            last_operation, last_state = self.history.pop()
            self.state = last_state
            self.update_bloch_sphere()
            self.update_timeline()
            messagebox.showinfo("Undo", f"Undid {last_operation}")
        else:
            messagebox.showwarning("Undo", "No operations to undo")

    def clear_timeline(self):
        self.history = []
        self.state = np.array([1, 0])  # Reset to initial state
        self.update_bloch_sphere()
        self.timeline_text.delete(1.0, tk.END)
        messagebox.showinfo("Clear", "Timeline and state cleared")

    def update_timeline(self):
        self.timeline_text.delete(1.0, tk.END)
        for operation, state in self.history:
            state_str = f"[{state[0].real:.2f}, {state[1].real:.2f}]"  # Format state for display
            self.timeline_text.insert(tk.END, f"{operation} -> State: {state_str}\n", ('bold',))
        self.timeline_text.tag_config('bold', font=('Arial', 10, 'bold'))

    def show_tutorial(self):
        messagebox.showinfo("Tutorial", "Welcome to the Qubit Tutorial. Learn about qubit states and gates.")
        # Here, you can implement step-by-step instructions and interactive elements.

    def show_gate_challenge(self):
        messagebox.showinfo("Gate Challenge", "Solve the Gate Challenge. Apply gates to reach the target state.")
        # Implement challenge logic here.

    def show_pulse_challenge(self):
        messagebox.showinfo("Pulse Challenge", "Complete the Pulse Challenge. Use pulses to manipulate the qubit.")
        # Implement pulse challenge logic here.

if __name__ == "__main__":
    root = tk.Tk()
    app = QubitSimulator(root)
    root.mainloop()
