import os

# PATH SETUP

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(SCRIPT_DIR, "..", "knowledge_base", "kb.pl")

# COLOUR PALETTE

COLORS = {
    "bg":          "#1A1F14",   
    "panel":       "#242B1A",   
    "card":        "#2D3622",   
    "accent":      "#7FB347",   
    "accent_dark": "#5A8030",   
    "danger":      "#C0392B",   
    "danger_dark": "#922B21",
    "text":        "#E8F0DC",   
    "text_dim":    "#8FA67A",   
    "gold":        "#D4A843",   
    "border":      "#3D4A2A",   
    "white":       "#FFFFFF",
    "symptom_bg":  "#1F2918",   
    "symptom_txt": "#B2D48A",   
    "result_pos":  "#2A3D1A",   
    "result_neg":  "#1E1E1E",   
    "scrollbar":   "#3A4528",
}

#  APP CONFIGURATION 

WINDOW_WIDTH = 820
WINDOW_HEIGHT = 680
MIN_WIDTH = 700
MIN_HEIGHT = 580

WINDOW_TITLE = "Crop Disease Prediction Expert System"
FOOTER_TEXT = "INNOVATIVE MINDS - GROUP 25"

# CROPS

CROPS = [
    ("maize"),
    ("tomato"),
]
