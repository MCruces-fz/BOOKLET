import tkinter as tk
from tkinter import ttk, filedialog
import os
from os.path import join as join_path

from bookbinder.machine import Booklet
from utils.const import INPDIR, OUTDIR


class BrowseIO(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.frm_choose_dirs = ttk.Frame(master=self, style="Booklet.TFrame")

        # INPUT
        # Label 'Directory of..."
        self.lbl_inp_dir = ttk.Label(self.frm_choose_dirs, text='Input file:', style="Regular.TLabel")
        # Path to Directory
        default_filename, *_ = [file for file in os.listdir(INPDIR) if file.endswith(".pdf")]
        self.var_inp_dir = tk.StringVar(value=join_path(INPDIR, default_filename))
        self.ent_inp_dir = ttk.Entry(self.frm_choose_dirs, textvariable=self.var_inp_dir, style="Browser.TEntry")
        self.btn_browse_inp = ttk.Button(
                self.frm_choose_dirs, 
                text="Browse", 
                command=lambda v = self.var_inp_dir: self.file_browser(v), 
                style="Regular.TButton"
                )

        # OUTPUT 
        # Label 'Directory of..."
        self.lbl_out_dir = ttk.Label(self.frm_choose_dirs, text='Output dir:', style="Regular.TLabel")
        # Path to Directory
        self.var_out_dir = tk.StringVar(value=OUTDIR)
        self.ent_out_dir = ttk.Entry(self.frm_choose_dirs, textvariable=self.var_out_dir, style="Browser.TEntry")
        self.btn_browse_out = ttk.Button(
                self.frm_choose_dirs, 
                text="Browse", 
                command=lambda v = self.var_out_dir: self.dir_browser(v), 
                style="Regular.TButton"
                )

        # MAKE BUTTON
        self.btn_make = ttk.Button(
                self.frm_choose_dirs, 
                text="MAKE", 
                command=lambda in_ = self.var_inp_dir.get(), out = self.var_out_dir.get(): Booklet.create_and_save(in_, out), 
                style="Regular.TButton"
                )

        # PACKS
        self.lbl_inp_dir.grid(row=1, column=1, sticky='news', padx=5, pady=5)  # Grided in Choose Dirs
        self.ent_inp_dir.grid(row=1, column=2, columnspan=4, sticky='news', padx=0, pady=5)  # Grided in Choose Dirs
        self.btn_browse_inp.grid(row=1, column=6, sticky='news', padx=5, pady=5)  # Grided in Choose Dirs

        self.lbl_out_dir.grid(row=2, column=1, sticky='news', padx=5, pady=5)  # Grided in Choose Dirs
        self.ent_out_dir.grid(row=2, column=2, columnspan=4, sticky='news', padx=0, pady=5)  # Grided in Choose Dirs
        self.btn_browse_out.grid(row=2, column=6, sticky='news', padx=5, pady=5)  # Grided in Choose Dirs

        self.btn_make.grid(row=3, column=3, columnspan=2, sticky='news', padx=5, pady=5)  # Grided in Choose Dirs

        self.frm_choose_dirs.pack(fill=tk.BOTH, expand=True)  # Packed in Options
        self.frm_choose_dirs.grid_rowconfigure(0, weight=1)
        self.frm_choose_dirs.grid_rowconfigure(4, weight=1)
        self.frm_choose_dirs.grid_columnconfigure(0, weight=1)
        self.frm_choose_dirs.grid_columnconfigure(7, weight=1)

    def file_browser(self, file: tk.StringVar):
        filename = filedialog.askopenfile(
                title="Choose input PDF file",
                filetypes = (
                    ("pdf files","*.pdf"),
                    ("all files","*.*"))
                )
        file.set(filename.name)

    def dir_browser(self, dir: tk.StringVar):
        filename = filedialog.askdirectory(title="Choose output directory")
        dir.set(filename)
