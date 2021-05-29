"""
PyLofi
Plays lofi from lofi lifestreams.
"""
import webbrowser
import os
import random
import re

import _thread as thread

os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]
import pyglet
import youtube_dl

import mpv


class Youtube:
    """
    Extract links from the youtube.md file
    """

    def __init__(self):
        self.path = "youtube.md"
        self.links = []
        self.video = {}
        self.last_videos = []
        self.is_fetching = False

        self.ydl = youtube_dl.YoutubeDL({})

        self.get_links()
        random.shuffle(self.links)

    def get_links(self):
        """
        uses regex to save all available links in self.links.
        """
        with open(self.path, "rb") as ytfile:
            txt = "".join(filter(str.isascii, ytfile.read().decode())).replace(")", "")
            self.links = re.findall(
                r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                txt,
            )

    def extract_all(self):
        """
        uses youtube_dl to extract all video-links from self.links
        """
        for link in self.links:
            try:
                v = self.ydl.extract_info(link, download=False)
                self.last_videos.append(v)
                if not self.video:
                    self.video = v
            except youtube_dl.utils.DownloadError:
                print("bad link %s" % link)

    def get_random(self):
        """
        sets self.video
        """
        if not self.last_videos:
            print("wait")
            return False

        self.video = self.last_videos.pop(0)
        self.last_videos.append(self.video)
        return True

        self.is_fetching = True
        link = self.links.pop(0)
        self.links.append(link)
        try:
            self.video = self.ydl.extract_info(link, download=False)
            self.last_videos.append(self.video)
        except youtube_dl.utils.DownloadError:
            print("bad link %s" % link)

        self.is_fetching = False


class Player:
    """
    uses mpv to play the lufi music.
    """

    def __init__(self):
        self.player = mpv.MPV(ytdl=True)
        self.player.property_add("video", 0)

    def play(self, url):
        self.player.play(url)


class Gui:
    """
    UI and stuff
    """

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
        thread.start_new_thread(self.youtube.extract_all, ())
        self.random_lofi()

    def random_lofi(self):
        """ event to play a new lofi """
        if self.youtube.last_videos:
            self.youtube.get_random()
            self.is_new = True

    def goback(self):
        """ go to the previous lofi stream """
        self.current = self.youtube.last_videos.pop(-1)
        self.youtube.last_videos.insert(0, self.current)
        self.youtube.video = self.current
        self.is_new = True

    def open_link(self):
        """ open the lofi stream link in the browser """
        webbrowser.open_new_tab(self.current["webpage_url"])

    def swap_info(self):
        """ update text labels """
        if not self.youtube.last_videos:
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
        """ draw labels """
        self.label_author.draw()
        self.label_title.draw()


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


depressed = pyglet.resource.image("random_notpressed.png")
pressed = pyglet.resource.image("random_pressed.png")
hover = pyglet.resource.image("random_hover.png")

back_depressed = pyglet.resource.image("back_notpressed.png")
back_pressed = pyglet.resource.image("back_pressed.png")
back_hover = pyglet.resource.image("back_hover.png")


link_depressed = pyglet.resource.image("link_notpressed.png")
link_pressed = pyglet.resource.image("link_pressed.png")
link_hover = pyglet.resource.image("link_hover.png")

frame = pyglet.gui.Frame(window, order=4)

playnext_button = pyglet.gui.PushButton(
    100, 300, pressed=pressed, depressed=depressed, hover=hover, batch=BATCH
)

back_button = pyglet.gui.PushButton(
    200,
    200,
    pressed=back_pressed,
    depressed=back_depressed,
    hover=back_hover,
    batch=BATCH,
)

link_button = pyglet.gui.PushButton(
    400,
    120,
    pressed=link_pressed,
    depressed=link_depressed,
    hover=link_hover,
    batch=BATCH,
)
playnext_button.set_handler("on_release", gui.random_lofi)
back_button.set_handler("on_release", gui.goback)
link_button.set_handler("on_release", gui.open_link)

frame.add_widget(playnext_button)
frame.add_widget(back_button)
frame.add_widget(link_button)

pyglet.app.run()
