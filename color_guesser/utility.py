import tkinter as tk
import sys
import ctypes

def color_hex_to_hsv(
    color_hex: str
) -> tuple[float, float, float]:
    """Convert a color hex code to HSV values."""
    r = int(color_hex[1:3], 16)     #"#abcdef" → ab → 171
    g = int(color_hex[3:5], 16)     #"#abcdef" → cd → 205
    b = int(color_hex[5:7], 16)     #"#abcdef" → ef → 239

    r_norm = r / 255
    g_norm = g / 255
    b_norm = b / 255

    m_max = max(r_norm, g_norm, b_norm)
    m_min = min(r_norm, g_norm, b_norm)
    delta = m_max - m_min

    if delta == 0:
        hue = 0.0
    elif m_max == r_norm:
        hue = 60 * (((g_norm - b_norm) / delta) % 6)
    elif m_max == g_norm:
        hue = 60 * (((b_norm - r_norm) / delta) + 2)
    else:
        hue = 60 * (((r_norm - g_norm) / delta) + 4)

    if m_max == 0:
        saturation = 0.0
    else:
        saturation = (delta / m_max) * 100

    value = m_max * 100

    return hue, saturation, value

def hue_similarity(
    hue_1: float,
    hue_2: float
) -> float:
    """
    Return the similarity score of two hue values (1.0 = identical, 0.0 = opposite).

    Hue is treated as circular (0° == 360°).
    The similarity is squared to penalize large hue differences more aggressively.
    """
    diff = abs(hue_1 - hue_2)
    diff_circular = min(diff, 360 - diff)
    return (1 - diff_circular / 180) ** 2

def evaluate_color_similarity(
    color_hex_1: str,
    color_hex_2: str
) -> float:
    """
    Return the similarity score of two colors using HSV components.

    Hue contributes 60% of the score, saturation 20%, and value 20%.
    """
    h1, s1, v1 = color_hex_to_hsv(color_hex_1)
    h2, s2, v2 = color_hex_to_hsv(color_hex_2)
    saturation_similarity = 1 - abs(s1 - s2) / 100
    value_similarity = 1 - abs(v1 - v2) / 100
    return (
        hue_similarity(h1, h2) * 0.6 +
        saturation_similarity * 0.2 +
        value_similarity * 0.2
    )

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
