import random
import re

import pafy
import pyglet
import vlc


class Youtube:
    def __init__(self):
        self.path = "youtube.md"
        self.links = []
        self.videos = {}

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
        link = self.links.pop(0)
        self.links.append(link)
        if link not in self.videos:
            self.videos[link] = pafy.new(link)

        return self.videos[link]


class Player:
    def __init__(self):
        self.instance = vlc.Instance("--no-video")
        self.player = self.instance.media_player_new()

    def play(self, url):
        media = self.instance.media_new(url)
        self.player.set_media(media)
        self.player.play()


class Gui:
    def __init__(self, window):
        self.window = window
        self.youtube = Youtube()
        self.player = Player()

        self.current_video = None
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
        self.current_video = self.youtube.get_random()
        self.author = "".join(filter(str.isascii, self.current_video.author))
        self.title = "".join(filter(str.isascii, self.current_video.title))

        self.label_author.text = self.author
        self.label_title.text = self.title

        self.player.play(self.current_video.streams[0].url)

    def draw(self):
        self.label_author.draw()
        self.label_title.draw()

    def scroll(self, dt):
        text = str(self.label_title.text)
        self.label_title.text = text[1:] + text[0]


window = pyglet.window.Window()
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
    gui.draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    gui.random_lofi()


pyglet.clock.schedule_interval(gui.scroll, 0.5)
pyglet.app.run()
