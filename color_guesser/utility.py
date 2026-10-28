import tkinter as tk
import sys
import ctypes

def color_hex_to_rgb(
    color_hex: str
) -> tuple[int, int, int]:
    """Convert a color hex code to RGB values."""
    r = int(color_hex[1:3], 16)     #"#abcdef" → ab → 171
    g = int(color_hex[3:5], 16)     #"#abcdef" → cd → 205
    b = int(color_hex[5:7], 16)     #"#abcdef" → ef → 239
    return r, g, b

def evaluate_color_similarity(
    color_hex_1: str,
    color_hex_2: str
) -> float:
    """Return the similarity score of the given colors (best: 1.0, worst: 0.0)."""
    r1, g1, b1 = color_hex_to_rgb(color_hex_1)
    r2, g2, b2 = color_hex_to_rgb(color_hex_2)
    diff = abs(r1 - r2) + abs(g1 - g2) + abs(b1 - b2)
    return 1 - diff / 765

def score_to_adjective(
    score: float
) -> str:
    """Return an adequate adjective for the given score (best: 1.0, worst: 0.0)."""
    adjectives_worst_to_best = [
        "Abysmal", "Terrible", "Very bad", "Bad",
        "Poor", "Weak", "Underwhelming", "Mediocre",
        "Acceptable", "Reasonable", "Decent", "Solid",
        "Good", "Strong", "Excellent", "Fantastic",
        "Outstanding", "Exceptional", "Perfect"
    ]
    max_index = len(adjectives_worst_to_best) - 1
    return adjectives_worst_to_best[int(max_index * score)]

def force_dark_title_bar(
    window: tk.Tk | tk.Toplevel
) -> None:
    """Force a dark title bar on windows."""
    window.update_idletasks()
    if sys.platform != "win32":
        return

    use_dark_mode = ctypes.c_int(1)

    try:
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            ctypes.windll.user32.GetParent(window.winfo_id()),
            20,
            ctypes.byref(use_dark_mode),
            ctypes.sizeof(use_dark_mode)
        )
    except Exception:
        pass
