import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EquationField:
    # Clase para un campo de entrada que muestra y edita ecuaciones en formato LaTeX.

    def __init__(self, window: tk.Tk, row: int = 0, column: int = 0,
                 padx: int = 10, pady: int = 10, sticky: str = 'nsew'):
        self.window = window

        # Campo de entrada optimizado para edición
        self.entry = tk.Entry(
            window,
            font=("Arial", 14),
            width=30,
            relief="flat",
            highlightthickness=1,
            highlightbackground="gray",
            highlightcolor="blue"
        )
        self.entry.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        self.entry.insert(0, "x^3/6")  # Ecuación inicial: x^3/6

        # Configurar lienzo para vista previa de la ecuación
        self.fig = Figure(figsize=(3.5, 1.2))
        self.ax = self.fig.add_subplot(111)
        self.ax.axis('off')
        self.canvas = FigureCanvasTkAgg(self.fig, master=window)
        self.canvas.get_tk_widget().grid(row=row + 1, column=column, columnspan=2, padx=padx, pady=pady, sticky=sticky)

        # Frame para los botones de inserción
        button_frame = tk.Frame(window)
        button_frame.grid(row=row + 2, column=column, columnspan=2, padx=padx, pady=5, sticky=sticky)

        # Botones para insertar comandos LaTeX
        buttons = [
            ("x²", "^"),  # Potencia
            ("√", "\\sqrt{}"),  # Raíz
            ("frac", "\\frac{}{}"),  # Fracción
            ("·", "\\cdot"),  # Multiplicación
            ("sin", "\\sin()"),  # Seno
            ("cos", "\\cos()"),  # Coseno
        ]
        for idx, (text, command) in enumerate(buttons):
            tk.Button(
                button_frame,
                text=text,
                font=("Arial", 10),
                command=lambda cmd=command: self.insert_latex(cmd)
            ).grid(row=0, column=idx, padx=2)

        # Vincular eventos para actualización en tiempo real
        self.entry.bind("<KeyRelease>", self.update_preview)
        self.update_preview()

    def insert_latex(self, command: str):
        # Inserta un comando LaTeX en la posición actual del cursor.
        cursor_pos = self.entry.index(tk.INSERT)
        self.entry.insert(cursor_pos, command)
        if command in ["\\sqrt{}", "\\sin()", "\\cos()"]:
            self.entry.icursor(cursor_pos + len(command) - 1)
        elif command == "\\frac{}{}":
            self.entry.icursor(cursor_pos + len(command) - 4)
        self.update_preview()
        self.entry.focus_set()

    def update_preview(self, event=None):
        # Actualiza la vista previa de la ecuación en formato LaTeX.
        ecuacion = self.get_text_for_latex()
        if not ecuacion:
            ecuacion = "x^2"  # Ecuación por defecto
        try:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"${ecuacion}$", fontsize=16, ha="center", va="center")
            self.ax.axis("off")
            self.canvas.draw()
        except Exception:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "Invalid LaTeX", fontsize=12, ha="center", va="center", color="red")
            self.ax.axis("off")
            self.canvas.draw()

    def get_text(self) -> str:
        # Devuelve el texto de la ecuación para cálculos.
        raw_text = self.entry.get().strip()
        # Convertir entrada LaTeX a formato SymPy
        return raw_text.replace("\\cdot", "*").replace("\\frac{", "").replace("}{", "/").replace("}", "")

    def get_text_for_latex(self) -> str:
        #Convierte la entrada a formato LaTeX para la vista previa.
        raw_text = self.entry.get().strip()
        if not raw_text:
            return "x^2"
        # Si ya es LaTeX (contiene \frac, \sqrt, etc.), no modificar
        if raw_text.startswith("\\") or "\\" in raw_text[1:]:
            return raw_text
        # Convertir divisiones simples (x/2) a fracciones LaTeX
        if "/" in raw_text:
            parts = raw_text.split("/", 1)
            return f"\\frac{{{parts[0]}}}{{{parts[1]}}}"
        # Convertir multiplicaciones (*) a \cdot
        return raw_text.replace("*", "\\cdot")