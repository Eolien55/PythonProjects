from pytube import YouTube, Playlist
import os
from html import unescape
import re
from werkzeug.utils import secure_filename as file
import ffmpeg
import gi

gi.require_version("Gtk", "3.0")

user = os.getlogin()

from gi.repository import Gtk


def show(title, text):
    title, text = str(title), str(text)
    dialog = Gtk.MessageDialog(
        transient_for=window,
        flags=0,
        message_type=Gtk.MessageType.INFO,
        buttons=Gtk.ButtonsType.OK,
        text=title,
    )
    dialog.format_secondary_text(text)
    dialog.run()

    dialog.destroy()


def help_me(event):
    show(
        "Help",
        "search:[query]   will replace search:[query] by the url of a video that matches with the query\n\nGlobally, it downloads videos that have the good URL",
    )


def make_format(name, name_second, path):
    try:
        ffmpeg.input(os.path.join(path, name)).output(
            os.path.join(path, name_second)
        ).run()
    except:
        pass
    os.remove(os.path.join(path, name))


def run(event=None):
    link = entry.get_text()
    format = entryformat.get_text()
    if not format:
        format = "mp4"
    soundonly = "soundonly:" in link
    if "search:" in link:
        link = (re.sub(r"(^|:).+\:", "", link),)
    else:
        link = re.sub(r"(^|:).+\:", "", link)
    try:
        rundownload(link, format=format)
    except Exception as e:
        show("Error", e)
    finally:
        entry.set_text("")


def rundownload(link, suffix="", format="mp4"):
    if isinstance(link, tuple):
        from youtube_search import YoutubeSearch

        results = YoutubeSearch(link[0]).to_dict()
        assert results, "Aucun résultats"
        result = results[0]
        link = "https://youtube.com/" + result["url_suffix"]
        rundownload(link, format=format)
        return

    if link.startswith("https://www.youtube.com/playlist"):
        playlist = Playlist(link)
        for url in playlist.video_urls:
            rundownload(url, unescape(playlist.title), format=format)
        return

    if not os.path.exists(os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix)):
        os.makedirs(os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix))

    video = YouTube(link)

    name = video.title.replace("/", "")
    name_second = name + "." + format

    if format != "mp4":
        name = file(name).replace(".", "")

    download_video = video.streams.get_highest_resolution()
    show(
        f"Let's download '{video.title}' with a resolution of '{download_video.resolution}'{' as a ' + format} !",
        "",
    )
    download_video.download(
        os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix), filename=name
    )
    name = name + ".mp4"
    make_format(
        name, name_second, os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix)
    )


window = Gtk.Window()
window.set_title("Youtube Downloader")
window.set_default_size(300, 0)
window.set_resizable(False)

box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
label = Gtk.Label(label="Entrez l'url puis la touche entrer")
button = Gtk.Button(label="help")
button.set_halign(Gtk.Align.CENTER)
entry = Gtk.Entry()
entry.set_halign(Gtk.Align.CENTER)
entryformat = Gtk.Entry()
entryformat.set_halign(Gtk.Align.CENTER)
labelformat = Gtk.Label(label="Choisissez un format (par défaut, mp4)")
labelformat.set_halign(Gtk.Align.CENTER)

box.pack_start(label, False, False, 0)
box.pack_start(entry, False, False, 0)
box.pack_start(labelformat, False, False, 0)
box.pack_start(entryformat, False, False, 0)
box.pack_start(button, False, False, 0)

window.add(box)

entry.connect("activate", run)
entryformat.connect("activate", run)
button.connect("clicked", help_me)
window.connect("delete-event", Gtk.main_quit)

window.show_all()

Gtk.main()
