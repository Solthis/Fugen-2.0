# -*- coding: utf-8 -*

import sys
from cx_Freeze import setup, Executable

options = {"includes": [],
           "excludes": [],
           "packages": ["pyodbc", "numpy", "openpyxl"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

cible_1 = Executable("main.py",
                     base=base,
                     icon='resources/icons/solthis.ico',)

setup(name="Fugen",
      version="2.0b",
      description="HIV report generation from Fuchia database",
      options={"build_exe": options},
      executables=[cible_1, ])
