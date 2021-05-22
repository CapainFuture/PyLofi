from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {
    "packages": ["pyglet", "re", "random", "pafy", "vlc", "youtube_dl", "pyglet.media"],
    "excludes": ["tkinter"],
    "includes": ["vlc"],
    "include_files": [
        r"res\Agave-Regular.ttf",
        "youtube.md",
        r"C:\Program Files\VideoLAN\VLC\libvlc.dll",
        r"C:\Program Files\VideoLAN\VLC\libvlccore.dll",
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",

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
