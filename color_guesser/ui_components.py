import tkinter as tk
from tkinter import ttk
from colors import BACKGROUND_COLOR

def define_style(root: tk.Tk):
    style = ttk.Style(root)
    style.theme_use("default")

    #frames
    style.configure(
        "TFrame",
        background=BACKGROUND_COLOR
    )
    style.configure(
        "GuessPreview.TFrame",
        background=BACKGROUND_COLOR,
        borderwidth=1,
        relief="solid"
    )
    style.configure(
        "ResultPreview.TFrame",
        background=BACKGROUND_COLOR,
        borderwidth=1,
        relief="solid"
    )

    #labels
    style.configure(
        "TLabel",
        font=("", 10, "normal"),
        foreground="#ffffff",
        background=BACKGROUND_COLOR
    )
    style.configure(
        "Heading.TLabel",
        font=("", 12, "bold"),
        foreground="#ffffff",
        background=BACKGROUND_COLOR
    )

    #buttons
    style.configure(
        "Custom.TButton",
        foreground="#ffffff",
        background="#505050"
    )
    style.map(
        "Custom.TButton",
        background=[("active", "#606060")],
        foreground=[("active", "#ffffff")]
    )

    return style

class MainWindow(ttk.Frame):
    def __init__(self, parent: tk.Tk, style: ttk.Style, select_color_callback, confirm_selection_callback):
        super().__init__(parent)

        self.parent = parent
        self.parent.title("Color Guesser")

        self.style = style

        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)  #guess panel grows
        self.columnconfigure(1, weight=0)  #history panel fixed width

        self.guess_panel = GuessPanel(self, self.style, select_color_callback, confirm_selection_callback)
        self.history_panel = HistoryPanel(self)

class GuessPanel(ttk.Frame):
    def __init__(self, parent: ttk.Frame, style: ttk.Style, select_color_callback, confirm_selection_callback):
        super().__init__(parent)

        self.grid(row=0, column=0, sticky="nsew")

        self.style = style
        self.confirm_selection_callback = confirm_selection_callback

        heading = ttk.Label(
            self,
            text=f"Guess what this color looks like:",
            style="Heading.TLabel"
        )
        heading.pack(pady=5)

        self.target_color_label = ttk.Label(self, style="TLabel")
        self.target_color_label.pack()

        self.preview_frame = ttk.Frame(
            self,
            style="GuessPreview.TFrame",
            width=350,
            height=350
        )
        self.preview_frame.pack(padx=15, pady=15)

        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.pack()

        self.select_button = ttk.Button(
            button_frame,
            text="Select Color",
            command=select_color_callback,
            style="Custom.TButton"
        )
        self.select_button.grid(row=0, column=0, padx=5, pady=5)

        self.confirm_button = ttk.Button(
            button_frame,
            text="Confirm Selection",
            command=self.confirm_selection_callback,
            style="Custom.TButton"
        )
        self.confirm_button.grid(row=0, column=1, padx=5, pady=5)

    def enable_buttons(self):
        self.select_button.state(["!disabled"])
        self.confirm_button.state(["!disabled"])

    def disable_buttons(self):
        self.select_button.state(["disabled"])
        self.confirm_button.state(["disabled"])

    def update_preview(self, color: str):
        self.style.configure("GuessPreview.TFrame", background=color, borderwidth=1, relief="solid")

class HistoryPanel(ttk.Frame):
    def __init__(self, parent: ttk.Frame):
        super().__init__(parent)

        self.grid(row=0, column=1, sticky="ns")

        history_label = ttk.Label(self, text="History:", style="Heading.TLabel")
        history_label.pack(pady=5)

        #create treeview (as a table)
        columns = ("number", "name", "target", "guess", "points", "average")
        self.history = ttk.Treeview(self, columns=columns, show="headings")
        self.history.tag_configure("ttk", background="#505050")

        #add headings
        self.history.heading("number", text="#")
        self.history.heading("name", text="Name")
        self.history.heading("target", text="Target")
        self.history.heading("guess", text="Guess")
        self.history.heading("points", text="Points")
        self.history.heading("average", text="Average")

        #configure columns
        self.history.column("number", width=40, minwidth=40)
        self.history.column("name", width=150, minwidth=150)
        self.history.column("target", width=70, minwidth=70)
        self.history.column("guess", width=70, minwidth=70)
        self.history.column("points", width=60, minwidth=60, anchor="e")
        self.history.column("average", width=60, minwidth=60, anchor="e")
        self.history.pack(side="left", fill="y", pady=5)

        #add a vertical scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.history.yview)
        scrollbar.pack(side="right", fill="y", padx=5, pady=5)
        self.history.configure(yscrollcommand=scrollbar.set)

    def append_entry(self, number: int, name: str, target: str, guess: str, points: int, average: int):
        self.history.insert("", "end", values=(number, name, target, guess, points, average))

class ResultWindow(ttk.Frame):
    def __init__(self, parent: tk.Toplevel, style: ttk.Style, reset_game_callback):
        super().__init__(parent)

        self.parent = parent
        self.parent.title("Result")

        self.style = style
        self.reset_game_callback = reset_game_callback

        self.pack(fill="both", expand=True)

        self.heading = ttk.Label(self, style="Heading.TLabel")
        self.heading.pack(pady=5)

        self.feedback_label = ttk.Label(self, style="TLabel")
        self.feedback_label.pack()

        self.target_color_label = ttk.Label(self, style="TLabel")
        self.target_color_label.pack(padx=5)

        self.preview_frame = ttk.Frame(self, style="ResultPreview.TFrame", width=350, height=350)
        self.preview_frame.pack(padx=15, pady=15)

        button_frame = ttk.Frame(self, style="TFrame")
        button_frame.pack()

        restart_game_button = ttk.Button(button_frame, text="Try Again", command=self.reset_game_callback, style="Custom.TButton")
        restart_game_button.grid(row=0, column=0, padx=5, pady=5)

    def update_preview(self, color: str):
        self.style.configure("ResultPreview.TFrame", background=color, borderwidth=1, relief="solid")