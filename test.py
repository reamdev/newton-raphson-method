import tkinter as tk

ventana = tk.Tk()
ventana.title("Ejemplo con grid")
ventana.geometry("400x300")

# Etiqueta y campo de texto en una cuadrícula
tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(ventana).grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Apellido:").grid(row=1, column=0)# sentencia: "Ejemplo con grid")
# ventana.geometry("400x300")

# Etiqueta y campo de texto en una cuadrícula
tk.Label(ventana, text="Nombre:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(ventana).grid(row=0, column=1, padx=10, pady=10)

tk.Label(ventana, text="Apellido:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(ventana).grid(row=1, column=1, padx=10, pady=10)

# Botón en la siguiente fila
tk.Button(ventana, text="Enviar").grid(row=2, column=0, columnspan=2, pady=10)

ventana.mainloop()