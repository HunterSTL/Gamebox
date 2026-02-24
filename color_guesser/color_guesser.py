import random
import tkinter as tk
from tkinter import colorchooser, messagebox
from colors import COLOR_DICTIONARY, BACKGROUND_COLOR
from ui_components import MainWindow, ResultWindow, define_style

def choose_random_color() -> tuple[str, str]:
    """return (color_name, hex_code)"""
    choice = random.choice(list(COLOR_DICTIONARY.items()))
    return choice[0], choice[1]

def color_hex_to_rgb(color_hex: str) -> tuple[int, int, int]:
    red = int(color_hex[1:3], 16)   #"#abcdef" → ab → 171
    green = int(color_hex[3:5], 16) #"#abcdef" → cd → 205
    blue = int(color_hex[5:7], 16)  #"#abcdef" → ef → 239
    return red, green, blue

def evaluate_similarity(color_to_guess_hex: str, guessed_color_hex: str) -> float:
    #convert hex value to RGB values (#abcdef → 171, 205, 239)
    target_red, target_green, target_blue = color_hex_to_rgb(color_to_guess_hex)
    guess_red, guess_green, guess_blue = color_hex_to_rgb(guessed_color_hex)

    #compute the absolute difference for each color chanel
    diff_red = abs(target_red - guess_red)
    diff_green = abs(target_green - guess_green)
    diff_blue = abs(target_blue - guess_blue)
    diff_total = diff_red + diff_green + diff_blue

    #convert the total difference (best: 0 - worst: 765) to points (best: 1.0 - worst: 0.0)
    return 1 - diff_total / 765

def score_to_adjective(score: float) -> str:
    adjectives = [
        "Perfect", "Exceptional", "Outstanding", "Fantastic",
        "Excellent", "Great", "Strong", "Good",
        "Solid", "Decent", "Reasonable", "Acceptable",
        "Mediocre", "Underwhelming", "Weak", "Poor",
        "Bad", "Very bad", "Terrible", "Abysmal"
    ]
    max_index = len(adjectives) - 1
    index = int(max_index * (1 - score))
    return adjectives[index]

class ColorGuesser:
    def __init__(self, root: tk.Tk):
        self.root = root

        #target color (name + hex) and guessed color (hex)
        self.target_color_name, self.target_color_hex = choose_random_color()
        self.guessed_color_hex = None

        #history of past guesses (points only)
        self.point_history = []

        #UI
        self.style = define_style(self.root)
        self.main_window = MainWindow(self.root, self.style, self.select_color, self.confirm_selection)
        self.main_window.guess_panel.target_color_label.config(text=self.target_color_name)

        #result window
        self.result_window_top = None

    def select_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.main_window.guess_panel.update_preview(color)
            self.guessed_color_hex = color

    def confirm_selection(self):
        if not self.guessed_color_hex:
            messagebox.showinfo("Color", "No color selected. Select a color first.")
            return

        #disable buttons
        self.main_window.guess_panel.disable_buttons()

        #evaluate similarity between the two colors
        similarity = evaluate_similarity(self.target_color_hex, self.guessed_color_hex)
        adjective = score_to_adjective(similarity)

        #convert score (0.0 - 1.0) to points (0 - 100)
        points = int(similarity * 100)

        #create entry to points history
        self.point_history.append(points)
        guess_count = len(self.point_history)
        guess_sum = sum(self.point_history)

        #add entry to history
        self.main_window.history_panel.append_entry(
            guess_count,
            self.target_color_name,
            self.target_color_hex,
            self.guessed_color_hex,
            points,
            int(guess_sum / guess_count)
        )

        #create a new result window
        self.result_window_top = tk.Toplevel()

        #reset game if result window is closed
        self.result_window_top.protocol("WM_DELETE_WINDOW", self.reset_game)

        #build UI
        result_window = ResultWindow(self.result_window_top, self.style, self.reset_game)
        result_window.heading.config(text=f"{int(similarity * 100)}/100 points")
        result_window.feedback_label.config(text=f"{adjective} guess!")
        result_window.target_color_label.config(text=f"Here's what the color \"{self.target_color_name}\" actually looks like:")
        result_window.update_preview(self.target_color_hex)

    def reset_game(self):
        #destroy result window
        self.result_window_top.destroy()
        self.result_window_top = None

        #reset model
        self.guessed_color_hex = None
        self.target_color_name, self.target_color_hex = choose_random_color()

        #reset UI
        self.main_window.guess_panel.target_color_label.config(text=self.target_color_name)
        self.main_window.guess_panel.update_preview(BACKGROUND_COLOR)
        self.main_window.guess_panel.enable_buttons()

if __name__ == "__main__":
    root = tk.Tk()
    ColorGuesser(root)
    root.mainloop()