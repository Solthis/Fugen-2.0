# -*- coding: utf-8 -*

# Copyright 2017 Solthis.
#
# This file is part of Fugen 2.0.
#
# Fugen 2.0 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Fugen 2.0 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Fugen 2.0. If not, see <http://www.gnu.org/licenses/>.


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

setup(name="Fugen 2.0",
      version="2.0",
      description="Flexible HIV report generation from Fuchia database",
      options={"build_exe": options},
      executables=[cible_1, ])
