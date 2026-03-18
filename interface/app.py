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
        self.confirmed = []  # list of (disease_name, info_dict)

        # Fonts
        self._setup_fonts()

        # Build permanent shell (header + content area)
        self._build_shell()

        # Show crop selection screen
        self._screen_crop_select()

    # ── FONTS ────────────────────────────────────────────────

    def _setup_fonts(self):
        self.f_title = tkfont.Font(family="Georgia", size=20, weight="bold")
        self.f_sub = tkfont.Font(family="Georgia", size=11, slant="italic")
        self.f_label = tkfont.Font(family="Courier New", size=10, weight="bold")
        self.f_disease = tkfont.Font(family="Georgia", size=16, weight="bold")
        self.f_symptom = tkfont.Font(family="Courier New", size=10)
        self.f_body = tkfont.Font(family="Georgia", size=11)
        self.f_btn = tkfont.Font(family="Georgia", size=12, weight="bold")
        self.f_small = tkfont.Font(family="Courier New", size=9)
        self.f_counter = tkfont.Font(family="Courier New", size=9)

    # ── SHELL ────────────────────────────────────────────────

    def _build_shell(self):
        # Header bar
        hdr = tk.Frame(self, bg=C["panel"], height=70)
        hdr.pack(fill="x", side="top")
        hdr.pack_propagate(False)

        tk.Label(
            hdr,
            text="🌿 CROP DISEASE EXPERT SYSTEM",
            font=self.f_title,
            bg=C["panel"],
            fg=C["accent"],
        ).pack(side="left", padx=24, pady=14)

        self.lbl_crop_badge = tk.Label(
            hdr, text="", font=self.f_small, bg=C["accent_dark"], fg=C["white"], padx=10, pady=4
        )
        self.lbl_crop_badge.pack(side="right", padx=20, pady=20)

        # Progress bar strip
        self.progress_frame = tk.Frame(self, bg=C["border"], height=3)
        self.progress_frame.pack(fill="x")
        self.progress_bar = tk.Frame(
            self.progress_frame, bg=C["accent"], height=3, width=0
        )
        self.progress_bar.place(x=0, y=0, relheight=1)

        # Main content frame (swapped per screen)
        self.content = tk.Frame(self, bg=C["bg"])
        self.content.pack(fill="both", expand=True, padx=0, pady=0)

    def _clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def _update_progress(self, fraction: float):
        self.update_idletasks()
        w = self.content.winfo_width() or self.winfo_width()
        self.progress_bar.config(width=int(w * fraction))

    # ── SCREEN: CROP SELECTION ──────────────────────────────

    def _screen_crop_select(self):
        self._clear_content()
        self.lbl_crop_badge.config(text="")
        self._update_progress(0)

        outer = tk.Frame(self.content, bg=C["bg"])
        outer.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            outer,
            text="Which crop are you diagnosing?",
            font=self.f_disease,
            bg=C["bg"],
            fg=C["text"],
        ).pack(pady=(0, 8))
        tk.Label(
            outer,
            text="Select a crop to begin the diagnostic session.",
            font=self.f_sub,
            bg=C["bg"],
            fg=C["text_dim"],
        ).pack(pady=(0, 36))

        btn_frame = tk.Frame(outer, bg=C["bg"])
        btn_frame.pack()

        for crop in CROPS:
            card = tk.Frame(
                btn_frame,
                bg=C["card"],
                bd=0,
                highlightthickness=2,
                highlightbackground=C["border"],
                cursor="hand2",
            )
            card.pack(side="left", padx=16, ipadx=20, ipady=20)

            tk.Label(card, font=tkfont.Font(size=42), bg=C["card"]).pack(
                pady=(12, 4)
            )
            tk.Label(
                card, text=crop.upper(), font=self.f_btn, bg=C["card"], fg=C["accent"]
            ).pack(pady=(0, 12))

            # Hover effect
            def _enter(e, c=card):
                c.config(highlightbackground=C["accent"])

            def _leave(e, c=card):
                c.config(highlightbackground=C["border"])

            def _click(e, cr=crop):
                self._start_diagnosis(cr)

            card.bind("<Enter>", _enter)
            card.bind("<Leave>", _leave)
            card.bind("<Button-1>", _click)
            for child in card.winfo_children():
                child.bind("<Button-1>", _click)

        tk.Label(
            outer,
            text=FOOTER_TEXT,
            font=self.f_small,
            bg=C["bg"],
            fg=C["border"],
        ).pack(pady=(48, 0))

    # ── START DIAGNOSIS ──────────────────────────────────────

    def _start_diagnosis(self, crop: str):
        self.crop = crop
        self.diseases = self.kb.get_diseases(crop)
        self.disease_idx = 0
        self.confirmed = []
        self.lbl_crop_badge.config(text=f"  {crop.upper()}  ")
        self._screen_question()

    # ── SCREEN: QUESTION ─────────────────────────────────────

    def _screen_question(self):
        self._clear_content()

        if self.disease_idx >= len(self.diseases):
            self._screen_results()
            return

        disease_name = self.diseases[self.disease_idx]
        info = self.kb.get_disease_info(self.crop, disease_name)
        total = len(self.diseases)
        current = self.disease_idx + 1

        self._update_progress(current / total)

        # Wrapper with padding
        wrapper = tk.Frame(self.content, bg=C["bg"])
        wrapper.pack(fill="both", expand=True, padx=40, pady=24)

        # Counter
        tk.Label(
            wrapper,
            text=f"Disease {current} of {total}",
            font=self.f_counter,
            bg=C["bg"],
            fg=C["text_dim"],
        ).pack(anchor="w")

        # Progress dots
        dot_row = tk.Frame(wrapper, bg=C["bg"])
        dot_row.pack(anchor="w", pady=(4, 18))
        for i in range(total):
            color = (
                C["accent"]
                if i < current
                else (C["border"] if i > self.disease_idx else C["gold"])
            )
            tk.Frame(
                dot_row,
                bg=color,
                width=18 if i == self.disease_idx else 8,
                height=8,
            ).pack(side="left", padx=1)

        # Question card
        card = tk.Frame(
            wrapper, bg=C["card"], highlightthickness=1, highlightbackground=C["border"]
        )
        card.pack(fill="x", pady=(0, 20))

        # Question prompt
        name_bar = tk.Frame(card, bg=C["accent_dark"])
        name_bar.pack(fill="x")
        tk.Label(
            name_bar,
            text=f"  Is your {self.crop} crop showing these symptoms?",
            font=self.f_label,
            bg=C["accent_dark"],
            fg=C["text_dim"],
            anchor="w",
        ).pack(fill="x", padx=16, pady=(10, 10))

        # Symptoms list
        sym_frame = tk.Frame(card, bg=C["card"])
        sym_frame.pack(fill="x", padx=20, pady=16)

        tk.Label(
            sym_frame,
            text="Presenting symptoms:",
            font=self.f_label,
            bg=C["card"],
            fg=C["text_dim"],
        ).pack(anchor="w", pady=(0, 10))

        for i, symptom in enumerate(info.get("symptoms", []), 1):
            row = tk.Frame(
                sym_frame,
                bg=C["symptom_bg"],
                highlightthickness=1,
                highlightbackground=C["border"],
            )
            row.pack(fill="x", pady=3)

            tk.Label(
                row, text=f" {i} ", font=self.f_label, bg=C["accent_dark"], fg=C["white"]
            ).pack(side="left")
            tk.Label(
                row,
                text=f"  {symptom}",
                font=self.f_body,
                bg=C["symptom_bg"],
                fg=C["symptom_txt"],
                anchor="w",
            ).pack(side="left", padx=8, pady=8)

        # Yes / No buttons
        btn_row = tk.Frame(wrapper, bg=C["bg"])
        btn_row.pack(pady=8)

        yes_btn = self._make_btn(
            btn_row,
            "✓  YES — Confirm These Symptoms",
            C["accent"],
            C["accent_dark"],
            lambda: self._answer(True, disease_name, info),
        )
        yes_btn.pack(side="left", padx=10, ipadx=12, ipady=8)

        no_btn = self._make_btn(
            btn_row,
            "✗  NO — Not These Symptoms",
            C["danger"],
            C["danger_dark"],
            lambda: self._answer(False, disease_name, info),
        )
        no_btn.pack(side="left", padx=10, ipadx=12, ipady=8)

        # Hint
        tk.Label(
            wrapper,
            text="Answer YES if the crop is showing at least these symptoms. Answer NO to check the next disease.",
            font=self.f_small,
            bg=C["bg"],
            fg=C["border"],
            wraplength=700,
            justify="center",
        ).pack(pady=(6, 0))

    def _make_btn(self, parent, text, bg, active_bg, cmd):
        btn = tk.Button(
            parent,
            text=text,
            font=self.f_btn,
            bg=bg,
            fg=C["white"],
            activebackground=active_bg,
            activeforeground=C["white"],
            relief="flat",
            cursor="hand2",
            bd=0,
            command=cmd,
        )

        def _enter(e):
            btn.config(bg=active_bg)

        def _leave(e):
            btn.config(bg=bg)

        btn.bind("<Enter>", _enter)
        btn.bind("<Leave>", _leave)
        return btn

    # ── ANSWER HANDLER ───────────────────────────────────────

    def _answer(self, confirmed: bool, disease_name: str, info: dict):
        if confirmed:
            self.confirmed.append((disease_name, info))
        self.disease_idx += 1
        self._screen_question()

    # ── SCREEN: RESULTS ──────────────────────────────────────

    def _screen_results(self):
        self._clear_content()
        self._update_progress(1.0)

        # Scrollable results area
        canvas = tk.Canvas(self.content, bg=C["bg"], bd=0, highlightthickness=0)
        scrollbar = tk.Scrollbar(
            self.content,
            orient="vertical",
            command=canvas.yview,
            bg=C["scrollbar"],
            troughcolor=C["bg"],
        )
        scroll_frame = tk.Frame(canvas, bg=C["bg"])

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Bind mousewheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Content inside scroll
        inner = tk.Frame(scroll_frame, bg=C["bg"])
        inner.pack(fill="both", expand=True, padx=40, pady=24)

        # Summary header
        total_checked = len(self.diseases)
        num_found = len(self.confirmed)

        if num_found > 0:
            headline = f"⚠  {num_found} Disease{'s' if num_found > 1 else ''} Identified"
            h_color = C["gold"]
        else:
            headline = "✅  No Diseases Matched"
            h_color = C["accent"]

        tk.Label(inner, text=headline, font=self.f_disease, bg=C["bg"], fg=h_color).pack(
            anchor="w", pady=(0, 4)
        )
        tk.Label(
            inner,
            text=f"{self.crop.capitalize()} crop  ·  {total_checked} diseases screened  ·  {num_found} confirmed",
            font=self.f_sub,
            bg=C["bg"],
            fg=C["text_dim"],
        ).pack(anchor="w", pady=(0, 20))

        if num_found == 0:
            no_card = tk.Frame(
                inner, bg=C["result_neg"], highlightthickness=1, highlightbackground=C["border"]
            )
            no_card.pack(fill="x", pady=8)
            tk.Label(
                no_card,
                text=(
                    "Your crop did not match any of the known disease patterns.\n"
                    "It may be healthy, or the symptoms may not yet be apparent.\n"
                    "Consider consulting a local agricultural extension officer."
                ),
                font=self.f_body,
                bg=C["result_neg"],
                fg=C["text"],
                justify="left",
                wraplength=680,
            ).pack(padx=24, pady=20)
        else:
            for i, (disease_name, info) in enumerate(self.confirmed, 1):
                self._render_result_card(inner, i, disease_name, info)

        # Disclaimer
        disc = tk.Frame(
            inner, bg=C["panel"], highlightthickness=1, highlightbackground=C["border"]
        )
        disc.pack(fill="x", pady=(20, 4))
        tk.Label(
            disc,
            text="⚠  DISCLAIMER: This system is a diagnostic aid only. "
            "Consult a certified agronomist for confirmation and treatment.",
            font=self.f_small,
            bg=C["panel"],
            fg=C["text_dim"],
            wraplength=680,
            justify="left",
        ).pack(padx=20, pady=12)

        # Restart button
        self._make_btn(
            inner, "← Start New Diagnosis", C["accent_dark"], C["accent"], self._restart
        ).pack(pady=16, ipadx=10, ipady=6)

    def _render_result_card(self, parent, idx, disease_name, info):
        card = tk.Frame(
            parent, bg=C["result_pos"], highlightthickness=1, highlightbackground=C["accent_dark"]
        )
        card.pack(fill="x", pady=8)

        # Disease title
        title_bar = tk.Frame(card, bg=C["accent_dark"])
        title_bar.pack(fill="x")
        tk.Label(
            title_bar,
            text=f"  [{idx}]  {disease_name}",
            font=self.f_disease,
            bg=C["accent_dark"],
            fg=C["gold"],
            anchor="w",
        ).pack(fill="x", padx=16, pady=10)

        body = tk.Frame(card, bg=C["result_pos"])
        body.pack(fill="x", padx=20, pady=14)

        # Confirmed symptoms
        tk.Label(
            body,
            text="CONFIRMED SYMPTOMS",
            font=self.f_label,
            bg=C["result_pos"],
            fg=C["text_dim"],
        ).pack(anchor="w")
        for s in info["symptoms"]:
            row = tk.Frame(body, bg=C["symptom_bg"])
            row.pack(fill="x", pady=2)
            tk.Label(
                row, text="  ✓  ", font=self.f_label, bg=C["accent"], fg=C["white"]
            ).pack(side="left")
            tk.Label(
                row,
                text=f" {s}",
                font=self.f_body,
                bg=C["symptom_bg"],
                fg=C["symptom_txt"],
                anchor="w",
            ).pack(side="left", pady=6)

        tk.Frame(body, bg=C["border"], height=1).pack(fill="x", pady=12)

        # Description
        tk.Label(
            body,
            text="ABOUT THIS DISEASE",
            font=self.f_label,
            bg=C["result_pos"],
            fg=C["text_dim"],
        ).pack(anchor="w")
        tk.Label(
            body,
            text=info["description"],
            font=self.f_body,
            bg=C["result_pos"],
            fg=C["text"],
            wraplength=680,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(4, 12))

        # Recommendation
        rec_frame = tk.Frame(
            body, bg="#1A2D10", highlightthickness=1, highlightbackground=C["accent_dark"]
        )
        rec_frame.pack(fill="x")
        tk.Label(
            rec_frame, text="  💊 RECOMMENDATION", font=self.f_label, bg="#1A2D10", fg=C["accent"]
        ).pack(anchor="w", padx=12, pady=(10, 4))
        tk.Label(
            rec_frame,
            text=info["recommendation"],
            font=self.f_body,
            bg="#1A2D10",
            fg=C["text"],
            wraplength=680,
            justify="left",
            anchor="w",
        ).pack(padx=16, pady=(0, 12))

    # ── RESTART ──────────────────────────────────────────────

    def _restart(self):
        self.crop = None
        self.diseases = []
        self.disease_idx = 0
        self.confirmed = []
        self._screen_crop_select()

    # ── FATAL ERROR ──────────────────────────────────────────

    def _fatal(self, msg):
        self._clear_content()
        tk.Label(
            self.content,
            text="❌  Failed to load Knowledge Base",
            font=self.f_disease,
            bg=C["bg"],
            fg=C["danger"],
        ).pack(pady=40)
        tk.Label(
            self.content,
            text=msg,
            font=self.f_body,
            bg=C["bg"],
            fg=C["text"],
            wraplength=600,
        ).pack(pady=10)
        tk.Label(
            self.content,
            text=f"Ensure SWI-Prolog is installed and kb.pl is at:\n{KB_PATH}",
            font=self.f_small,
            bg=C["bg"],
            fg=C["text_dim"],
        ).pack(pady=10)
