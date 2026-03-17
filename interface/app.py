"""
Expert System Application: Tkinter-based UI for crop disease diagnosis
"""

import tkinter as tk
from tkinter import font as tkfont

from config import COLORS as C, WINDOW_WIDTH, WINDOW_HEIGHT, MIN_WIDTH, MIN_HEIGHT, WINDOW_TITLE, FOOTER_TEXT, CROPS, KB_PATH
from knowledge_base import KnowledgeBase


class ExpertSystemApp(tk.Tk):
    """Main Tkinter application for the crop disease expert system."""

    def __init__(self):
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.configure(bg=C["bg"])
        self.resizable(True, True)

        # Load KB
        try:
            self.kb = KnowledgeBase()
        except Exception as e:
            self._fatal(str(e))
            return

        # State
        self.crop = None
        self.diseases = []
        self.disease_idx = 0
        self.confirmed = []

        # Fonts
        self.f_title = tkfont.Font(family="Arial", size=14, weight="bold")
        self.f_heading = tkfont.Font(family="Arial", size=12, weight="bold")
        self.f_normal = tkfont.Font(family="Arial", size=10)
        self.f_small = tkfont.Font(family="Arial", size=9)

        # Build UI
        self._build_shell()
        self._screen_crop_select()

    def _build_shell(self):
        """Build the header and content area."""
        # Header
        hdr = tk.Frame(self, bg=C["accent"], height=60)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="Crop Disease Expert System",
            font=self.f_title,
            bg=C["accent"],
            fg="white",
        ).pack(side="left", padx=20, pady=15)

        # Content area
        self.content = tk.Frame(self, bg=C["bg"])
        self.content.pack(fill="both", expand=True, padx=20, pady=20)

    def _clear_content(self):
        """Clear the content area."""
        for w in self.content.winfo_children():
            w.destroy()

    # ── SCREEN: CROP SELECTION ──────────────────────────────

    def _screen_crop_select(self):
        """Display crop selection screen."""
        self._clear_content()

        tk.Label(
            self.content,
            text="Select a Crop",
            font=self.f_heading,
            bg=C["bg"],
            fg=C["text"],
        ).pack(pady=(0, 10))

        tk.Label(
            self.content,
            text="Choose which crop to diagnose:",
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
        ).pack(pady=(0, 20))

        btn_frame = tk.Frame(self.content, bg=C["bg"])
        btn_frame.pack(pady=10)

        for crop, emoji in CROPS:
            btn = tk.Button(
                btn_frame,
                text=crop.upper(),
                font=self.f_normal,
                width=15,
                command=lambda c=crop: self._start_diagnosis(c),
            )
            btn.pack(pady=5)

    # ── START DIAGNOSIS ──────────────────────────────────────

    def _start_diagnosis(self, crop: str):
        """Start diagnosis for selected crop."""
        self.crop = crop
        self.diseases = self.kb.get_diseases(crop)
        self.disease_idx = 0
        self.confirmed = []
        self._screen_question()

    # ── SCREEN: QUESTION ─────────────────────────────────────

    def _screen_question(self):
        """Display symptom confirmation screen."""
        self._clear_content()

        if self.disease_idx >= len(self.diseases):
            self._screen_results()
            return

        disease_name = self.diseases[self.disease_idx]
        info = self.kb.get_disease_info(self.crop, disease_name)
        total = len(self.diseases)
        current = self.disease_idx + 1

        # Counter
        tk.Label(
            self.content,
            text=f"Disease {current} of {total}",
            font=self.f_small,
            bg=C["bg"],
            fg=C["text"],
        ).pack(anchor="w", pady=5)

        # Question
        tk.Label(
            self.content,
            text=f"Is your {self.crop} showing these symptoms?",
            font=self.f_heading,
            bg=C["bg"],
            fg=C["text"],
        ).pack(anchor="w", pady=(10, 15))

        # Symptoms list
        tk.Label(
            self.content,
            text="Symptoms:",
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
            weight="bold",
        ).pack(anchor="w")

        for symptom in info.get("symptoms", []):
            tk.Label(
                self.content,
                text=f"  • {symptom}",
                font=self.f_normal,
                bg=C["bg"],
                fg=C["text"],
                justify="left",
            ).pack(anchor="w", padx=20, pady=2)

        # Buttons
        btn_frame = tk.Frame(self.content, bg=C["bg"])
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="YES - Confirm",
            font=self.f_normal,
            width=15,
            bg=C["accent"],
            fg="white",
            command=lambda: self._answer(True, disease_name, info),
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="NO - Skip",
            font=self.f_normal,
            width=15,
            bg=C["danger"],
            fg="white",
            command=lambda: self._answer(False, disease_name, info),
        ).pack(side="left", padx=10)

    def _answer(self, confirmed: bool, disease_name: str, info: dict):
        """Handle answer to symptom confirmation."""
        if confirmed:
            self.confirmed.append((disease_name, info))
        self.disease_idx += 1
        self._screen_question()

    # ── SCREEN: RESULTS ──────────────────────────────────────

    def _screen_results(self):
        """Display diagnosis results."""
        self._clear_content()

        num_found = len(self.confirmed)
        total_checked = len(self.diseases)

        # Summary
        if num_found > 0:
            headline = f"RESULTS: {num_found} Disease(s) Identified"
        else:
            headline = "RESULTS: No Diseases Matched"

        tk.Label(
            self.content,
            text=headline,
            font=self.f_heading,
            bg=C["bg"],
            fg=C["text"],
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            self.content,
            text=f"Crop: {self.crop.upper()} | Diseases screened: {total_checked} | Confirmed: {num_found}",
            font=self.f_small,
            bg=C["bg"],
            fg=C["text"],
        ).pack(anchor="w", pady=(0, 20))

        if num_found == 0:
            tk.Label(
                self.content,
                text="Your crop did not match any known disease patterns.\nConsult a local agricultural expert if needed.",
                font=self.f_normal,
                bg=C["bg"],
                fg=C["text"],
                justify="left",
            ).pack(anchor="w", pady=10)
        else:
            for i, (disease_name, info) in enumerate(self.confirmed, 1):
                self._render_result_card(i, disease_name, info)

        # Disclaimer
        tk.Label(
            self.content,
            text="Disclaimer: This system is a diagnostic aid only. Consult a certified agronomist for confirmation.",
            font=self.f_small,
            bg=C["bg"],
            fg="#666666",
            justify="left",
            wraplength=600,
        ).pack(anchor="w", pady=(20, 10))

        # Restart button
        tk.Button(
            self.content,
            text="Start New Diagnosis",
            font=self.f_normal,
            command=self._restart,
        ).pack(pady=10)

    def _render_result_card(self, idx, disease_name, info):
        """Display individual disease result."""
        card = tk.Frame(self.content, bg=C["border"], relief="solid", bd=1)
        card.pack(fill="x", pady=10, padx=0)

        tk.Label(
            card,
            text=f"[{idx}] {disease_name.upper()}",
            font=self.f_heading,
            bg=C["border"],
            fg=C["accent"],
            anchor="w",
        ).pack(fill="x", padx=10, pady=(8, 4))

        inner = tk.Frame(card, bg=C["bg"])
        inner.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            inner,
            text="Confirmed Symptoms:",
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
            weight="bold",
        ).pack(anchor="w")

        for symptom in info["symptoms"]:
            tk.Label(
                inner,
                text=f"  • {symptom}",
                font=self.f_normal,
                bg=C["bg"],
                fg=C["text"],
            ).pack(anchor="w", padx=20)

        tk.Label(
            inner,
            text="\nDescription:",
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
            weight="bold",
        ).pack(anchor="w", pady=(10, 0))

        tk.Label(
            inner,
            text=info["description"],
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
            justify="left",
            wraplength=600,
        ).pack(anchor="w", padx=20, pady=(4, 10))

        tk.Label(
            inner,
            text="Recommendation:",
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
            weight="bold",
        ).pack(anchor="w")

        tk.Label(
            inner,
            text=info["recommendation"],
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
            justify="left",
            wraplength=600,
        ).pack(anchor="w", padx=20, pady=(4, 0))

    def _restart(self):
        """Restart the diagnosis process."""
        self.crop = None
        self.diseases = []
        self.disease_idx = 0
        self.confirmed = []
        self._screen_crop_select()

    def _fatal(self, msg):
        """Display fatal error."""
        self._clear_content()
        tk.Label(
            self.content,
            text="ERROR: Failed to load Knowledge Base",
            font=self.f_heading,
            bg=C["bg"],
            fg=C["danger"],
        ).pack(pady=20)
        tk.Label(
            self.content,
            text=msg,
            font=self.f_normal,
            bg=C["bg"],
            fg=C["text"],
            wraplength=500,
        ).pack(pady=10)
        tk.Label(
            self.content,
            text=f"Ensure SWI-Prolog is installed and kb.pl is at:\n{KB_PATH}",
            font=self.f_small,
            bg=C["bg"],
            fg=C["text"],
        ).pack(pady=10)
