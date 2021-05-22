from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    "packages": ["pyglet", "re", "random", "pafy", "vlc", "youtube_dl", "mpv.py"],
    "excludes": ["tkinter"],
    "includes": ["vlc"],
    "include_files": [
        r"res\Agave-Regular.ttf",
        "youtube.md",
        "mpv-1.dll",
    ],
}

import sys

# base = "Win32GUI" if sys.platform == "win32" else None

executables = [Executable("pylofi.py", target_name="pylofi.exe")]

setup(
    name="pylofi",
    version="0.1",
    author="Anthony Kersten",
    description="lofi meta player",
    options={"build_exe": build_options},
    executables=executables,
)
