import json
import random
import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from utility import evaluate_color_similarity, score_to_adjective, force_dark_title_bar

BG_COLOR = "#404040"
BUTTON_COLOR = "#505050"
TEXT_COLOR = "#FFFFFF"
PREVIEW_BORDER_COLOR = "#AAAAAA"


class ColorGuesser:
    def __init__(
        self,
        root: tk.Tk
    ) -> None:
        self._root: tk.Tk = root
        self._root.title("Color Guesser")
        self._root.configure(bg=BG_COLOR)
        force_dark_title_bar(window=self._root)

        # Game state
        self._remaining_color_pool: dict[str, str] = {}
        self._target_color_name: str | None = None
        self._target_color_hex: str | None = None
        self._guess_color_hex: str | None = None
        self._guess_count: int = 0
        self._guess_points: int = 0
        self._total_points: int = 0
        self._guess_feedback: str = ""

        # UI
        self._result_window: tk.Toplevel | None = None
        self._target_color_label: tk.Label | None = None
        self._guess_color_preview: tk.Frame | None = None
        self._history_table: ttk.Treeview | None = None

        self._reset_color_pool()
        self._draw_target_color()
        self._build_user_interface()

    def _reset_color_pool(
        self
    ) -> None:
        with open("color_pool.json", "r") as file:
            self._remaining_color_pool = json.load(file)

    def _draw_target_color(
        self
    ) -> None:
        self._target_color_name = random.choice(list(self._remaining_color_pool.keys()))
        self._target_color_hex = self._remaining_color_pool.pop(self._target_color_name)

        if not self._remaining_color_pool:
            self._reset_color_pool()

    def _select_color(
        self
    ) -> None:
        _, color_hex = colorchooser.askcolor()

        if not color_hex:
            return

        self._guess_color_preview.config(bg=color_hex)
        self._guess_color_hex = color_hex

    def _reset_game(
        self
    ) -> None:
        if self._result_window:
            self._result_window.destroy()
            self._result_window = None

        self._guess_color_hex = None
        self._guess_color_preview.config(bg=BG_COLOR)
        self._draw_target_color()
        self._target_color_label.config(text="Target: " + self._target_color_name)

    def _build_user_interface(
        self
    ) -> None:
        self._target_color_label = tk.Label(
            master=self._root,
            text="Target: " + self._target_color_name,
            font=("Arial", 16),
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self._target_color_label.pack()

        self._guess_color_preview = tk.Frame(
            master=self._root,
            bg=BG_COLOR,
            height=200,
            highlightbackground=PREVIEW_BORDER_COLOR,
            highlightthickness=1
        )
        self._guess_color_preview.pack(padx=10, pady=5, fill="both")

        button_frame = tk.Frame(
            master=self._root,
            bg=BG_COLOR
        )
        button_frame.pack(pady=5)

        tk.Button(
            master=button_frame,
            text="Select",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self._select_color
        ).pack(side="left", padx=5)

        tk.Button(
            master=button_frame,
            text="Reveal",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self._reveal_target
        ).pack(side="left", padx=5)

        self._build_history()

        self._root.update_idletasks()
        self._root.minsize(self._root.winfo_reqwidth(), self._root.winfo_reqheight())

    def _build_history(
        self
    ) -> None:
        history_frame = tk.Frame(
            master=self._root,
            bg=BG_COLOR
        )
        history_frame.pack(padx=10, pady=5, expand=True, fill="both")

        self._history_table = ttk.Treeview(
            master=history_frame,
            columns=("number", "name", "target", "guess", "points", "average"),
            show="headings"
        )

        self._history_table.heading("number", text="#")
        self._history_table.heading("name", text="Name")
        self._history_table.heading("target", text="Target")
        self._history_table.heading("guess", text="Guess")
        self._history_table.heading("points", text="Points")
        self._history_table.heading("average", text="Average")

        self._history_table.column("number", width=40, minwidth=40, stretch=False)
        self._history_table.column("name", width=150, minwidth=150, stretch=True)
        self._history_table.column("target", width=70, minwidth=70, stretch=False)
        self._history_table.column("guess", width=70, minwidth=70, stretch=False)
        self._history_table.column("points", width=60, minwidth=60, stretch=False, anchor="e")
        self._history_table.column("average", width=60, minwidth=60, stretch=False, anchor="e")
        self._history_table.pack(side="left", expand=True, fill="both", pady=5)

        scrollbar = ttk.Scrollbar(
            master=history_frame,
            orient="vertical",
            command=self._history_table.yview,
        )
        scrollbar.pack(side="left", fill="y", padx=5, pady=5)
        self._history_table.configure(yscrollcommand=scrollbar.set)

    def _reveal_target(
        self
    ) -> None:
        if not self._guess_color_hex:
            messagebox.showinfo("Color", "No color selected. Select a color first.")
            return

        self._evaluate_guess()
        self._create_history_entry()
        self._show_result_window()

    def _evaluate_guess(
        self
    ) -> None:
        score = evaluate_color_similarity(self._target_color_hex, self._guess_color_hex)
        self._guess_feedback = score_to_adjective(score) + " guess!"
        self._guess_count += 1
        self._guess_points = int(score * 100)
        self._total_points += self._guess_points

    def _create_history_entry(
        self
    ) -> None:
        self._history_table.insert(
            "", "end",
            values=(
                self._guess_count,
                self._target_color_name,
                self._target_color_hex,
                self._guess_color_hex,
                self._guess_points,
                int(self._total_points / self._guess_count)
            )
        )

    def _show_result_window(
        self
    ) -> None:
        root_x, root_y = self._root.winfo_x(), self._root.winfo_y()
        x_offset, y_offset = 300, 0

        self._result_window = tk.Toplevel(
            master=self._root,
            bg=BG_COLOR
        )
        self._result_window.grab_set()
        self._result_window.geometry(f"+{root_x + x_offset}+{root_y + y_offset}")
        self._result_window.protocol("WM_DELETE_WINDOW", self._reset_game)
        force_dark_title_bar(window=self._result_window)

        tk.Label(
            master=self._result_window,
            text=f"{self._guess_points} / 100 points",
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(pady=5)

        tk.Label(
            master=self._result_window,
            text=self._guess_feedback,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack()

        tk.Label(
            master=self._result_window,
            text=f"Here's what the color \"{self._target_color_name}\" actually looks like:",
            bg=BG_COLOR,
            fg=TEXT_COLOR
        ).pack(padx=5)

        tk.Frame(
            master=self._result_window,
            width=350,
            height=350,
            bg=self._target_color_hex,
            highlightbackground=PREVIEW_BORDER_COLOR,
            highlightthickness=1
        ).pack(padx=15, pady=15)
