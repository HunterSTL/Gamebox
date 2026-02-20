import random
import tkinter as tk
from tkinter import colorchooser, messagebox
from colors import COLOR_DICTIONARY, BACKGROUND_COLOR, TEXT_COLOR, BUTTON_COLOR

def choose_random_color():
    choice = random.choice(list(COLOR_DICTIONARY.items()))
    return choice[0], choice[1]

def evaluate_guess(guessed_color: str, actual_color: str) -> int:
    actual_color_red = int(actual_color[1:3], 16)               #"#abcdef" → ab → 171
    actual_color_green = int(actual_color[3:5], 16)             #"#abcdef" → cd → 205
    actual_color_blue = int(actual_color[5:7], 16)              #"#abcdef" → ef → 239

    guessed_color_red = int(guessed_color[1:3], 16)
    guessed_color_green = int(guessed_color[3:5], 16)
    guessed_color_blue = int(guessed_color[5:7], 16)

    diff_red = abs(actual_color_red - guessed_color_red)
    diff_green = abs(actual_color_green - guessed_color_green)
    diff_blue = abs(actual_color_blue - guessed_color_blue)
    diff_total = diff_red + diff_green + diff_blue              #0 → perfect match; 765 → total opposite (3 x 0-255)

    score_percent = int((765 - diff_total) / 7.65)              #convert to percentage (0-100) and round down to nearest whole number
    return score_percent

def score_to_text(score_percent: int) -> str:
    if score_percent == 100:
        return "100 points\nPerfect guess! You're incredible!"
    elif score_percent >= 95:
        return "Insane guess!"
    elif score_percent >= 90:
        return "Fantastic guess!"
    elif score_percent >= 85:
        return "Great guess!"
    elif score_percent >= 80:
        return "Good guess!"
    elif score_percent >= 75:
        return "Decent guess!"
    elif score_percent >= 70:
        return "Respectable guess!"
    elif score_percent >= 65:
        return "Ok guess!"
    elif score_percent >= 60:
        return "Sub-par guess!"
    elif score_percent >= 50:
        return "Poor guess!"
    elif score_percent >= 40:
        return "Bad guess!"
    elif score_percent >= 30:
        return "Terrible guess!"
    elif score_percent >= 20:
        return "Horrendous guess!"
    elif score_percent >= 10:
        return "Horrible guess!"
    elif score_percent >= 1:
        return "Abysmal guess!"
    return "You could not have been any more wrong! You should be ashamed of yourself!"

class ColorGuesser:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.color_to_guess_name, self.color_to_guess = choose_random_color()
        self.guessed_color = None

        #UI
        self.color_label = None
        self.preview = None
        self.result_label = None
        self.result_preview = None
        self.build_guess_window()

    def build_guess_window(self):
        self.root.title("Color Guesser")
        self.root.geometry("500x400")
        self.root.configure(bg=BACKGROUND_COLOR)

        instruction_label = tk.Label(
            root,
            text="Guess what this color looks like:",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            font=("Segoe UI", 13, "bold")
        )
        instruction_label.pack(pady=(10, 5))

        self.color_label = tk.Label(
            root,
            text=self.color_to_guess_name,
            font=("Segoe UI", 11),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        self.color_label.pack()

        self.preview = tk.Frame(
            root,
            bg=BACKGROUND_COLOR,
            width=300,
            height=200,
            relief="solid",
            borderwidth=1
        )
        self.preview.pack(pady=15)

        button_frame = tk.Frame(root, bg=BACKGROUND_COLOR)
        button_frame.pack(pady=10)

        button_select = tk.Button(
            button_frame,
            text="Select Color",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.select_color
        )
        button_select.grid(row=0, column=0, padx=8)

        button_check = tk.Button(
            button_frame,
            text="Check Selection",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.check_selection
        )
        button_check.grid(row=0, column=1, padx=8)

    def build_result_window(self, score: int, result_text: str):
        self.top = tk.Toplevel(self.root)
        self.top.title("Result")
        self.top.geometry("500x400")
        self.top.configure(bg=BACKGROUND_COLOR)

        score_label = tk.Label(
            self.top,
            text=f"{score}/100 points",
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR,
            font=("Segoe UI", 13, "bold")
        )
        score_label.pack(pady=(10, 5))

        result_label = tk.Label(
            self.top,
            text=result_text,
            font=("Segoe UI", 11),
            bg=BACKGROUND_COLOR,
            fg=TEXT_COLOR
        )
        result_label.pack()

        result_preview = tk.Frame(
            self.top,
            bg=self.color_to_guess,
            width=300,
            height=200,
            relief="solid",
            borderwidth=1
        )
        result_preview.pack(pady=15)

        button_try_again = tk.Button(
            self.top,
            text="Try Again",
            bg=BUTTON_COLOR,
            fg=TEXT_COLOR,
            command=self.restart_game
        )
        button_try_again.pack(padx=8)

    def select_color(self):
        color = colorchooser.askcolor()[1]

        if color:
            self.preview.config(bg=color)
            self.guessed_color = color

    def check_selection(self):
        if not self.guessed_color:
            messagebox.showinfo("No color selected", "Please select a color first!")
            return

        score_percent = evaluate_guess(self.guessed_color, self.color_to_guess)
        result_text = score_to_text(score_percent)
        result_text += f"\nHere's what {self.color_to_guess_name} actually looks like:"
        self.build_result_window(score_percent, result_text)

    def restart_game(self):
        self.top.destroy()
        self.color_to_guess_name, self.color_to_guess = choose_random_color()
        self.color_label.config(text=self.color_to_guess_name)
        self.preview.config(bg=BACKGROUND_COLOR)
        self.guessed_color = None

if __name__ == "__main__":
    root = tk.Tk()
    ColorGuesser(root)
    root.mainloop()