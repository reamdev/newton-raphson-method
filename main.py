from interface.main_interface import NewtonRaphsonGUI
import tkinter as tk

def main():
    window = tk.Tk()
    app = NewtonRaphsonGUI(window)
    window.mainloop()

if __name__ == "__main__":
    main()