# -*- coding: utf-8 -*

import sys
from cx_Freeze import setup, Executable

options = {
    "includes": [],
    "excludes": ["requests", "IPython", "jinja2", "matplotlib", "notebook",
                 "PyQt5", "sqlalchemy", "sphinx", "tkinter", "PIL",
                 "statsmodels", "tables", ""],
    "packages": ["pyodbc", "numpy", "openpyxl"],
    "replace_paths": [["*", ""]],
    "include_msvcr": True,
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cible_1 = Executable("main.py",
                     base=base,
                     icon='resources/icons/solthis.ico',)

setup(name="Fugen 2.0 BETA",
      version="2.0",
      description="HIV report generation from Fuchia database",
      options={"build_exe": options},
      executables=[cible_1, ])
