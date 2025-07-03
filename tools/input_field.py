import tkinter as tk


class InputField:
    def __init__(self, window: tk.Tk, label_text: str, row: int = 0, column: int = 0,
                 padx: int = 10, pady: int = 10, sticky: str = 'nsew'):
        self.label = tk.Label(window, text=label_text, font=("Arial", 12))
        self.label.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        self.entry = tk.Entry(window, font=("Arial", 14), width=45, relief="flat",
                              highlightthickness=1, highlightbackground="gray",
                              highlightcolor="blue")
        self.entry.grid(row=row, column=column + 1, padx=padx, pady=pady, sticky=sticky)

    def get_text(self) -> str:
        return self.entry.get().strip()
