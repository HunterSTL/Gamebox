import random
import tkinter as tk
from tkinter import colorchooser, ttk, messagebox


COLORS = {
    #white
    "white": "#ffffff",
    "snow": "#fffafa",
    "honeydew": "#f0fff0",
    "mintcream": "#f5fffa",
    "azure": "#f0ffff",
    "aliceblue": "#f0f8ff",
    "ghostwhite": "#f8f8ff",
    "whitesmoke": "#f5f5f5",
    "seashell": "#fff5ee",
    "beige": "#f5f5dc",
    "oldlace": "#fdf5e6",
    "floralwhite": "#fffaf0",
    "ivory": "#fffff0",
    "antiquewhite": "#faebd7",
    "linen": "#faf0e6",
    "lavenderblush": "#fff0f5",
    "mistyrose": "#ffe4e1",
    #yellow
    "gold": "#ffd700",
    "yellow": "#ffff00",
    "lightyellow": "#ffffe0",
    "lemonchiffon": "#fffacd",
    "lightgoldenrodyellow": "#fafad2",
    "papayawhip": "#ffefd5",
    "moccasin": "#ffe4b5",
    "peachpuff": "#ffdab9",
    "palegoldenrod": "#eee8aa",
    "khaki": "#f0e68c",
    "darkkhaki": "#bdb76b",
    #orange
    "coral": "#ff7f50",
    "tomato": "#ff6347",
    "orangered": "#ff4500",
    "darkorange": "#ff8c00",
    "orange": "#ffa500",
    #red
    "indianred": "#cd5c5c",
    "lightcoral": "#f08080",
    "salmon": "#fa8072",
    "darksalmon": "#e9967a",
    "lightsalmon": "#ffa07a",
    "crimson": "#dc143c",
    "red": "#ff0000",
    "firebrick": "#b22222",
    "darkred": "#8b0000",
    #pink
    "pink": "#ffc0cb",
    "lightpink": "#ffb6c1",
    "hotpink": "#ff69b4",
    "deeppink": "#ff1493",
    "mediumvioletred": "#c71585",
    "palevioletred": "#db7093",
    #purple
    "lavender": "#e6e6fa",
    "thistle": "#d8bfd8",
    "plum": "#dda0dd",
    "violet": "#ee82ee",
    "orchid": "#da70d6",
    "fuchsia": "#ff00ff",
    "magenta": "#ff00ff",
    "mediumorchid": "#ba55d3",
    "mediumpurple": "#9370db",
    "rebeccapurple": "#663399",
    "blueviolet": "#8a2be2",
    "darkviolet": "#9400d3",
    "darkorchid": "#9932cc",
    "darkmagenta": "#8b008b",
    "purple": "#800080",
    "indigo": "#4b0082",
    "slateblue": "#6a5acd",
    "darkslateblue": "#483d8b",
    "mediumslateblue": "#7b68ee",
    #blue
    "aqua": "#00ffff",
    "cyan": "#00ffff",
    "lightcyan": "#e0ffff",
    "paleturquoise": "#afeeee",
    "aquamarine": "#7fffd4",
    "turquoise": "#40e0d0",
    "mediumturquoise": "#48d1cc",
    "darkturquoise": "#00ced1",
    "cadetblue": "#5f9ea0",
    "steelblue": "#4682b4",
    "lightsteelblue": "#b0c4de",
    "powderblue": "#b0e0e6",
    "lightblue": "#add8e6",
    "skyblue": "#87ceeb",
    "lightskyblue": "#87cefa",
    "deepskyblue": "#00bfff",
    "dodgerblue": "#1e90ff",
    "cornflowerblue": "#6495ed",
    "royalblue": "#4169e1",
    "blue": "#0000ff",
    "mediumblue": "#0000cd",
    "darkblue": "#00008b",
    "navy": "#000080",
    "midnightblue": "#191970",
    #green
    "greenyellow": "#adff2f",
    "chartreuse": "#7fff00",
    "lawngreen": "#7cfc00",
    "lime": "#00ff00",
    "limegreen": "#32cd32",
    "palegreen": "#98fb98",
    "lightgreen": "#90ee90",
    "mediumspringgreen": "#00fa9a",
    "springgreen": "#00ff7f",
    "mediumseagreen": "#3cb371",
    "seagreen": "#2e8b57",
    "forestgreen": "#228b22",
    "green": "#008000",
    "darkgreen": "#006400",
    "yellowgreen": "#9acd32",
    "olivedrab": "#6b8e23",
    "olive": "#808000",
    "darkolivegreen": "#556b2f",
    "mediumaquamarine": "#66cdaa",
    "darkseagreen": "#8fbc8b",
    "lightseagreen": "#20b2aa",
    "darkcyan": "#008b8b",
    "teal": "#008080",
    #brown
    "cornsilk": "#fff8dc",
    "blanchedalmond": "#ffebcd",
    "bisque": "#ffe4c4",
    "navajowhite": "#ffdead",
    "wheat": "#f5deb3",
    "burlywood": "#deb887",
    "tan": "#d2b48c",
    "rosybrown": "#bc8f8f",
    "sandybrown": "#f4a460",
    "goldenrod": "#daa520",
    "darkgoldenrod": "#b8860b",
    "peru": "#cd853f",
    "chocolate": "#d2691e",
    "saddlebrown": "#8b4513",
    "sienna": "#a0522d",
    "brown": "#a52a2a",
    "maroon": "#800000",
    #gray
    "gainsboro": "#dcdcdc",
    "lightgray": "#d3d3d3",
    "silver": "#c0c0c0",
    "darkgray": "#a9a9a9",
    "gray": "#808080",
    "dimgray": "#696969",
    "lightslategray": "#778899",
    "slategray": "#708090",
    "darkslategray": "#2f4f4f",
    "black": "#000000",
}

INITIAL_COLOR = "#1199ff"

def choose_random_color():
    choice = random.choice(list(COLORS.items()))
    return choice[0], choice[1]

class ColorGuesser:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.color_to_guess_name, self.color_to_guess = choose_random_color()
        self.guessed_color = INITIAL_COLOR

        #UI
        self.color_label = None
        self.preview = None
        self.result_label = None
        self.result_preview = None
        self.build_ui()

    def build_ui(self):
        self.root.title("Color Guesser")
        self.root.geometry("450x450")
        self.root.configure(bg="#f3f3f3")

        instruction_label = tk.Label(
            root,
            text="Guess what this color looks like:",
            bg="#f3f3f3",
            font=("Segoe UI", 13, "bold")
        )
        instruction_label.pack(pady=(10, 5))

        self.color_label = tk.Label(
            root,
            text=self.color_to_guess_name,
            font=("Segoe UI", 11),
            bg="#f3f3f3"
        )
        self.color_label.pack()

        self.preview = tk.Frame(
            root,
            bg="#f3f3f3",
            width=260,
            height=80,
            relief="solid",
            borderwidth=1
        )
        self.preview.pack(pady=15)

        btn_frame = tk.Frame(root, bg="#f3f3f3")
        btn_frame.pack(pady=10)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 10))

        btn_select = ttk.Button(
            btn_frame,
            text="Select Color",
            command=self.select_color
        )
        btn_select.grid(row=0, column=0, padx=8)

        btn_check = ttk.Button(
            btn_frame,
            text="Check Selection",
            command=self.check_selection
        )
        btn_check.grid(row=0, column=1, padx=8)

        result_heading_label = tk.Label(
            root,
            text="Result:",
            bg="#f3f3f3",
            font=("Segoe UI", 13, "bold")
        )
        result_heading_label.pack(pady=(10, 5))

        self.result_label = tk.Label(
            root,
            text="Select a color then click \"Check Selection\" to see the result",
            font=("Segoe UI", 11),
            bg="#f3f3f3"
        )
        self.result_label.pack()

        self.result_preview = tk.Frame(
            root,
            bg="#f3f3f3",
            width=260,
            height=80,
            relief="solid",
            borderwidth=1
        )
        self.result_preview.pack(pady=15)

    def select_color(self):
        color = colorchooser.askcolor()[1]

        if color:
            self.preview.config(bg=color)
            self.guessed_color = color

    def check_selection(self):
        color_to_guess_red = int(self.color_to_guess[1:3], 16)               #"#abcdef" → ab → 171
        color_to_guess_green = int(self.color_to_guess[3:5], 16)             #"#abcdef" → cd → 205
        color_to_guess_blue = int(self.color_to_guess[5:7], 16)              #"#abcdef" → ef → 239

        guessed_color_red = int(self.guessed_color[1:3], 16)
        guessed_color_green = int(self.guessed_color[3:5], 16)
        guessed_color_blue = int(self.guessed_color[5:7], 16)

        diff_red = abs(color_to_guess_red - guessed_color_red)
        diff_green = abs(color_to_guess_green - guessed_color_green)
        diff_blue = abs(color_to_guess_blue - guessed_color_blue)

        diff_total = diff_red + diff_green + diff_blue              #0 → perfect match; 765 → total opposite (3 x 0-255)
        score = 765 - diff_total
        score_percent = int(score / 7.65)

        if score_percent == 100:
            result_text = "100 points\nPerfect guess! You're incredible!"
        elif score_percent >= 95:
            result_text = f"{score_percent} points\nInsane guess!"
        elif score_percent >= 90:
            result_text = f"{score_percent} points\nFantastic guess!"
        elif score_percent >= 85:
            result_text = f"{score_percent} points\nGreat guess!"
        elif score_percent >= 80:
            result_text = f"{score_percent} points\nGood guess!"
        elif score_percent >= 75:
            result_text = f"{score_percent} points\nDecent guess!"
        elif score_percent >= 70:
            result_text = f"{score_percent} points\nRespectable guess!"
        elif score_percent >= 65:
            result_text = f"{score_percent} points\nOk guess!"
        elif score_percent >= 60:
            result_text = f"{score_percent} points\nSub-par guess!"
        elif score_percent >= 50:
            result_text = f"{score_percent} points\nPoor guess!"
        elif score_percent >= 40:
            result_text = f"{score_percent} points\nBad guess!"
        elif score_percent >= 30:
            result_text = f"{score_percent} points\nTerrible guess!"
        elif score_percent >= 20:
            result_text = f"{score_percent} points\nHorrendous guess!"
        elif score_percent >= 10:
            result_text = f"{score_percent} points\nHorrible guess!"
        else:
            messagebox.showerror("You suck!", f"{score_percent} points\nThis guess was too ass! This session is terminated.")
            root.destroy()
            return

        self.result_label.config(text=result_text + "\nHere's what the color actually looks like:")
        self.result_preview.config(bg=self.color_to_guess)
        self.restart_game()

    def restart_game(self):
        self.color_to_guess_name, self.color_to_guess = choose_random_color()
        self.color_label.config(text=self.color_to_guess_name)

if __name__ == "__main__":
    root = tk.Tk()
    ColorGuesser(root)
    root.mainloop()