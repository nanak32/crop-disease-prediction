"""
UI Configuration: Colors, Fonts, and Constants
"""

import os

# ── PATH SETUP ────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(SCRIPT_DIR, "..", "knowledge_base", "kb.pl")

# ── COLOUR PALETTE (simple) ──────────────────────────────────

COLORS = {
    "bg":       "#FFFFFF",     # white background
    "text":     "#000000",     # black text
    "accent":   "#0066CC",     # blue accent
    "border":   "#CCCCCC",     # light gray border
    "danger":   "#CC0000",     # red for No button
}

# ── APP CONFIGURATION ─────────────────────────────────────────

WINDOW_WIDTH = 820
WINDOW_HEIGHT = 680
MIN_WIDTH = 700
MIN_HEIGHT = 580

WINDOW_TITLE = "Crop Disease Expert System — DCIT 313"
FOOTER_TEXT = "DCIT 313  |  Knowledge-Based System  |  Prolog + Python"

# ── CROPS ─────────────────────────────────────────────────────

CROPS = [
    ("maize", "🌽"),
    ("tomato", "🍅"),
]
