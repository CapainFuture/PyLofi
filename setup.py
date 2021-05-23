from glob import glob
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    "packages": ["pyglet", "re", "random", "youtube_dl", "mpv"],
    "excludes": ["tkinter"],
    "include_files": [
        "youtube.md",
        "mpv-1.dll",
        *glob("res\*"),
    ],
    "optimize": 2,
}

import sys

base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("pylofi.py", target_name="pylofi.exe")]

setup(
    name="pylofi",
    version="0.1",
    author="Anthony Kersten",
    description="lofi meta player",
    options={"build_exe": build_options},
    executables=executables,
    compress=True,
)
