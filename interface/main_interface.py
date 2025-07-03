import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from sympy import sympify, Symbol, sqrt, diff
from interface.equation_field import EquationField
from tools.input_field import InputField

class NewtonRaphsonGUI:
    def __init__(self, window: tk.Tk):
        self.window = window
        self.window.title('Newton-Raphson Method Graphical')
        self.window.geometry('1280x720')
        self.window.resizable(0, 0)

        # Configurar columnas (60%, 20%, 20%)
        self.window.columnconfigure(0, weight=6)
        self.window.columnconfigure(1, weight=2)
        self.window.columnconfigure(2, weight=2)

        # Configurar filas
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=1)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)
        self.window.rowconfigure(4, weight=1)
        self.window.rowconfigure(5, weight=1)

        # Crear columnas
        self.make_left_column()
        self.make_right_column()

    def make_left_column(self):
        # Crea contenido de la columna izquierda
        self.fig = Figure(figsize=(6, 4))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=6, sticky="nsew", padx=10, pady=10)
        self.ax.clear()
        self.ax.text(0.5, 0.5, "Enter an equation to graph", fontsize=14, ha="center", va="center")
        self.ax.axis("off")
        self.canvas.draw()

    def make_right_column(self):
        # Crea contenido de la columna derecha
        self.equation_field = EquationField(self.window, row=0, column=1)
        self.x_input = InputField(self.window, 'Initial x value', row=3, column=1)
        self.x_input.entry.insert(0, "-1.0")  # Ajustado para converger a x=0
        button = tk.Button(self.window, text='Calculate', command=self.process_inputs,
                           font=("Arial", 12), bg="lightgray")
        button.grid(row=4, column=1, columnspan=2, sticky="ew", padx=10, pady=10)
        self.result_label = tk.Label(self.window, text="Result: ", font=("Arial", 12))
        self.result_label.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    def process_inputs(self):
        # Procesa la ecuación con Newton-Raphson
        try:
            ecuacion = self.equation_field.get_text()
            x0 = float(self.x_input.get_text())
            x = Symbol('x')
            expr = sympify(ecuacion, locals={"sqrt": sqrt})
            derivative = diff(expr, x)
            max_iterations = 100
            tolerance = 1e-6
            x_n = x0
            iterations = [x_n]

            for _ in range(max_iterations):
                f_x = float(expr.subs(x, x_n))
                f_prime_x = float(derivative.subs(x, x_n))
                if abs(f_prime_x) < 1e-8 and abs(f_x) < 1e-6:
                    break
                if abs(f_prime_x) < 1e-8:
                    raise ValueError("Derivative too small, consider a different initial guess")
                x_next = x_n - f_x / f_prime_x
                iterations.append(x_next)
                if abs(x_next - x_n) < tolerance:
                    break
                x_n = x_next

            self.result_label.config(text=f"Result: Root ≈ {x_n:.6f}")
            self.plot_function(expr, x_n, iterations)
        except Exception as e:
            self.result_label.config(text=f"Error: {str(e)}")
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Error: {str(e)}", fontsize=12, ha="center", va="center", color="red")
            self.ax.axis("off")
            self.canvas.draw()

    def plot_function(self, expr, x_n, iterations):
        # Grafica la función y las iteraciones
        try:
            x_vals = np.linspace(max(x_n - 4, -5), min(x_n + 4, 5), 200)
            y_vals = [float(expr.subs('x', x)) for x in x_vals]
            self.ax.clear()
            latex_expr = self.equation_field.get_text_for_latex()
            self.ax.plot(x_vals, y_vals, label=f"${latex_expr}$")
            self.ax.axhline(0, color='black', linestyle='--', linewidth=0.5)

            for i, x_i in enumerate(iterations[:-1]):
                y_i = float(expr.subs('x', x_i))
                self.ax.plot(x_i, y_i, 'ro', markersize=5)
                self.ax.plot([x_i, x_i], [0, y_i], 'r--', linewidth=0.5)
                x_next = iterations[i + 1]
                slope = float(diff(expr, 'x').subs('x', x_i))
                if abs(slope) > 1e-8:
                    x_tangent = np.array([x_i - 0.5, x_i + 0.5])
                    y_tangent = y_i + slope * (x_tangent - x_i)
                    self.ax.plot(x_tangent, y_tangent, 'g--', linewidth=0.5)

            self.ax.plot(x_n, 0, 'bo', markersize=8, label='Root')
            self.ax.legend()
            self.ax.grid(True)
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('f(x)')
            self.ax.set_title(f"Newton-Raphson: ${latex_expr}$")
            self.canvas.draw()
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Graphing error: {str(e)}", fontsize=12, ha="center", va="center", color="red")
            self.ax.axis("off")
            self.canvas.draw()