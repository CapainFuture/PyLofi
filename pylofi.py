import os
import random
import re

import _thread as thread

os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]
import pyglet
import youtube_dl

import mpv


class Youtube:
    def __init__(self):
        self.path = "youtube.md"
        self.links = []
        self.video = {}
        self.is_fetching = False

        self.ydl = youtube_dl.YoutubeDL({})

        self.get_links()
        random.shuffle(self.links)

    def get_links(self):
        with open(self.path, "rb") as ytfile:
            txt = "".join(filter(str.isascii, ytfile.read().decode())).replace(")", "")
            self.links = re.findall(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                txt,
            )

    def get_random(self):
        self.is_fetching = True
        link = self.links.pop(0)
        self.links.append(link)
        try:
            self.video = self.ydl.extract_info(link, download=False)
        except youtube_dl.utils.DownloadError:
            print("bad link %s" % link)

        self.is_fetching = False


class Player:
    def __init__(self):
        self.player = mpv.MPV(ytdl=True)
        self.player.property_add("video", 0)

    def play(self, url):
        self.player.play(url)


class Gui:
    def __init__(self, window):
        self.window = window
        self.youtube = Youtube()
        self.player = Player()

        self.current = None
        self.is_new = True
        self.author = ""
        self.title = ""

        self.font = pyglet
        self.label_author = pyglet.text.Label(
            "",
            font_name="Agave",
            font_size=10,
            x=10,
            y=10,
        )

        self.label_title = pyglet.text.Label(
            "", font_name="Agave", font_size=12, x=10, y=40
        )

        self.random_lofi()

    def random_lofi(self):
        if not self.youtube.is_fetching:
            thread.start_new_thread(self.youtube.get_random, ())
            self.is_new = True

    def swap_info(self):
        if self.youtube.is_fetching:
            self.label_title.text = "..."
        else:
            self.current = self.youtube.video
            self.author = "".join(filter(str.isascii, self.current["uploader"]))
            self.title = "".join(filter(str.isascii, self.current["title"]))

            self.label_author.text = self.author
            self.label_title.text = self.title

            if self.is_new:
                self.player.play(self.current["formats"][0]["url"])
                self.is_new = False

    def draw(self):
        self.label_author.draw()
        self.label_title.draw()

    def scroll(self, dt):
        if self.label_title.content_width > self.window.width:
            text = str(self.label_title.text)
            self.label_title.text = text[1:] + text[0]


window = pyglet.window.Window(caption="pylofi")
BATCH = pyglet.graphics.Batch()

pyglet.resource.path.append("res")
pyglet.resource.add_font("Agave-Regular.ttf")
agave = pyglet.font.load("Agave")
pyglet.gl.glClearColor(0.2, 0.4, 0.5, 1.0)

gui = Gui(window)


@window.event
def on_draw():
    pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
    # window.clear()
    BATCH.draw()
    gui.swap_info()
    gui.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    gui.random_lofi()


pyglet.clock.schedule_interval(gui.scroll, 0.5)
pyglet.app.run()
