import tkinter as tk
from tkinter import ttk
from os.path import join as join_path

from bookbinder.machine import Booklet
from utils.const import STORE, INPDIR, OUTDIR
from gui.browse_io import BrowseIO


class Settings(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        frm_settings = ttk.Frame(master=self, style="Booklet.TFrame")

        lbl_theme = ttk.Label(frm_settings, text='Theme: ', style="Regular.TLabel")
        
        option_list_theme = ["dark", "light"]
        self.combo_theme = ttk.Combobox(frm_settings, values=option_list_theme, state="readonly", style="Regular.TCombobox")
        self.combo_theme.set("dark")

        # GRIDS
        lbl_theme.grid(row=1, column=1, sticky='news', padx=5, pady=5)  # Grided in Settings
        self.combo_theme.grid(row=1, column=2, sticky='news', padx=5, pady=5)

        frm_settings.pack(fill=tk.BOTH, expand=True)  # Packed in Options
        frm_settings.grid_rowconfigure(0, weight=1)
        frm_settings.grid_rowconfigure(4, weight=1)
        frm_settings.grid_columnconfigure(0, weight=1)
        frm_settings.grid_columnconfigure(7, weight=1)


class BookletMachine:
    def __init__(self, window_title: str = None, theme: str = "dark"):
        """
        Constructor for the GUI

        :param window_title: (optional) Title in the upper bar of the window.
        :param theme: (optional) dark or light (default dark).
        """
        
        #  --- L A Y O U T ---
        # M A I N   W I N D O W
        self.window = tk.Tk()
        # Configuration:
        self.theme = theme
        self.bg_default = None
        self.fg_default = None
        self.window_config(window_title)


        # W I D G E T S
        # --- Frames:
        self.frm_image = ttk.Frame(master=self.window, style="Booklet.TFrame")  
        self.frm_notebook = ttk.Frame(master=self.window, style="Booklet.TFrame")
        self.frm_settings = ttk.Frame(master=self.frm_notebook, style="Booklet.TFrame")
        self.frm_colormap = ttk.Frame(master=self.frm_notebook, style="Booklet.TFrame")

        # --- Labels:
        # self.lbl_date = None

        # IMAGE
        header_image = tk.PhotoImage(file=join_path(STORE, "Fibonacci.png")).subsample(2, 2)
        self.img_head = ttk.Label(self.frm_image, image=header_image, style="Title.TLabel")

        # TITLE
        self.lbl_title= ttk.Label(self.window, text='Booklet Machine', style="Title.TLabel")

        # NOTEBOOK
        self.ntb_instance = ttk.Notebook(self.frm_notebook, style="NB.TNotebook")

        self.frm_browse = BrowseIO()
        self.ntb_instance.add(self.frm_browse, text="Home")

        self.frm_settings = Settings()
        self.ntb_instance.add(self.frm_settings, text="Settings")

        # P A K S 
        self.frm_image.pack(fill=tk.BOTH, expand=True)  # Packed in Window
        self.img_head.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Packed in image
        self.lbl_title.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Packed in window

        self.frm_notebook.pack(fill=tk.BOTH, expand=True)  # Packed in window
        self.ntb_instance.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Packed in Notebook

        # M A I N - L O O P
        self.main_loop()

    def window_config(self, window_title: str = None):
        """
        Configuration for the window.

        :param window_title: Title in the upper bar of the window.
        """

        if self.theme == "light":
            self.bg_default = "#ffffff"
            self.fg_default = "#303030"
        else:
            self.bg_default = "#303030"
            self.fg_default = "#ffffff"

        style = ttk.Style()
        font_name = "Courier"
        # Helvetica, Courier, Arial
        style.configure(
                "Title.TLabel", 
                font=(font_name, 20, "bold"),
                anchor="center",
                foreground=self.fg_default, 
                background=self.bg_default
                )
        style.configure(
                "NB.TNotebook", 
                font=(font_name, 12, "italic"),
                relief=tk.FLAT,
                foreground=self.fg_default, 
                background=self.bg_default,
                )
        style.configure(
                "NB.TNotebook.Tab", 
                font=(font_name, 12, "italic"),
                relief=tk.FLAT,
                foreground=self.fg_default, 
                background=self.bg_default,
                )
        style.map(
                "NB.TNotebook.Tab", 
                foreground=[("selected", self.fg_default), ("active", "#000000")],
                background=[("selected", self.bg_default), ("active", "#ad7fa8")], 
                )
        style.configure(
                "Regular.TLabel", 
                font=(font_name, 12, "italic"),
                foreground=self.fg_default, 
                background=self.bg_default
                )
        style.configure(
                "Regular.TButton", 
                font=(font_name, 12, "bold italic"),
                relief=tk.FLAT,
                foreground=self.fg_default, 
                background=self.bg_default
                )
        style.map(
                "Regular.TButton", 
                foreground=[("selected", self.fg_default), ("active", "#000000")],
                background=[("selected", self.bg_default), ("active", "#ad7fa8")], 
                )
        style.configure(
                "Booklet.TFrame", 
                foreground=self.fg_default, 
                background=self.bg_default
                )
        style.configure(
                "Regular.TCombobox", 
                foreground=self.fg_default, 
                background=self.bg_default
                )
        style.configure(
                "Browser.TEntry", 
                font=(font_name, 12, "italic"),
                relief=tk.FLAT,
                width=20,
                foreground=self.fg_default, 
                background=self.bg_default,
                filedforeground=self.fg_default, 
                fieldbackground=self.bg_default,
                selectforeground="#ad7fa8",
                selectbackground="#000000",
                justify=tk.RIGHT
                )

        self.window.configure(bg=self.bg_default)

        style = ttk.Style(self.window)

        if window_title is None:
            self.window.title("COOKLET")
        else:
            self.window.title(window_title)

    def main_loop(self):
        """
        Main loop
        """
        self.window.mainloop() 
