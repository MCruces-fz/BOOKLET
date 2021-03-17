import tkinter as tk
from tkinter import ttk
from os.path import join as join_path

from bookbinder.machine import Booklet
from utils.const import STORE, INPDIR, OUTDIR
from gui.browse_io import BrowseIO


class Settings(ttk.Frame):
    def __init__(self, window_config, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window_config = window_config

        frm_settings = ttk.Frame(master=self, style="Booklet.TFrame")

        lbl_theme = ttk.Label(frm_settings, text='Theme: ', style="Regular.TLabel")
        
        # THEME
        option_list_theme = ["dark", "light"]
        self.combo_theme = ttk.Combobox(frm_settings, values=option_list_theme, state="readonly", style="Regular.TCombobox")
        self.combo_theme.set("dark")
        self.combo_theme.bind("<<ComboboxSelected>>", self.selection_changed)

        # SIGNATURE
        lbl_sgnature = ttk.Label(frm_settings, text='Write signature at the end\n of the output file.', style="Regular.TLabel")
        
        self.check_signature = tk.BooleanVar(frm_settings)
        self.check_signature.set(True)
        btn_signature = ttk.Checkbutton(frm_settings, variable=self.check_signature, style="Regular.TCheckbutton")

        btn_apply = ttk.Button(
                frm_settings, 
                text="APPLY", 
                command=lambda v = self.combo_theme.get(): None,
                style="Regular.TButton"
                )


        # GRIDS
        lbl_theme.grid(row=1, column=1, sticky='news', padx=5, pady=5)  # Grided in Settings
        self.combo_theme.grid(row=1, column=2, sticky='news', padx=5, pady=5)  # Grided in Settings
        btn_signature.grid(row=2, column=1, sticky='nes', padx=5, pady=5)  # Grided in Settings
        lbl_sgnature.grid(row=2, column=2, columnspan=3, sticky='nws', padx=5, pady=5)  # Grided in Settings

        btn_apply.grid(row=3, column=3, columnspan=2, sticky='news', padx=5, pady=5)  # Grided in Settings

        frm_settings.pack(fill=tk.BOTH, expand=True)  # Packed in Options
        frm_settings.grid_rowconfigure(0, weight=1)
        frm_settings.grid_rowconfigure(4, weight=1)
        frm_settings.grid_columnconfigure(0, weight=1)
        frm_settings.grid_columnconfigure(7, weight=1)

    def selection_changed(self, value):
        self.window_config(theme=self.combo_theme.get())
