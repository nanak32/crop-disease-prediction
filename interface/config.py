import os

# PATH SETUP

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(SCRIPT_DIR, "..", "knowledge_base", "kb.pl")

# COLOUR PALETTE

COLORS = {
    "bg":          "#1A1F14",   # deep forest black-green
    "panel":       "#242B1A",   # slightly lighter panel
    "card":        "#2D3622",   # question card
    "accent":      "#7FB347",   # fresh leaf green
    "accent_dark": "#5A8030",   # pressed state
    "danger":      "#C0392B",   # No button
    "danger_dark": "#922B21",
    "text":        "#E8F0DC",   # off-white
    "text_dim":    "#8FA67A",   # muted text
    "gold":        "#D4A843",   # disease name highlight
    "border":      "#3D4A2A",   # subtle border
    "white":       "#FFFFFF",
    "symptom_bg":  "#1F2918",   # symptom chip background
    "symptom_txt": "#B2D48A",   # symptom chip text
    "result_pos":  "#2A3D1A",   # positive result background
    "result_neg":  "#1E1E1E",   # no disease bg
    "scrollbar":   "#3A4528",
}

#  APP CONFIGURATION 

WINDOW_WIDTH = 820
WINDOW_HEIGHT = 680
MIN_WIDTH = 700
MIN_HEIGHT = 580

WINDOW_TITLE = "Crop Disease PredictionExpert System — DCIT 313"
FOOTER_TEXT = "DCIT 313  |  Knowledge-Based System  |  Prolog + Python"

# CROPS

CROPS = [
    ("maize"),
    ("tomato"),
]
