from pytube import YouTube, Playlist
import tkinter
from tkinter import ttk as tk
from tkinter import messagebox
import ttkthemes as themes
import os
from html import unescape
import re

user = os.getlogin()


def run():
    link = entry.get()
    soundonly = "soundonly:" in link
    if "search:" in link:
        link = (re.sub(r"(^|:).+\:", "", link),)
    else:
        link = re.sub(r"(^|:).+\:", "", link)

    try:
        rundownload(link, soundonly)
    except Exception as e:
        messagebox.showinfo("YoutubeDownloader", e)
    finally:
        st.set("")
        entry.update()


def rundownload(link, soundonly=False):
    from html import unescape
    from pytube import YouTube, Playlist

    if not soundonly:
        if not isinstance(link, tuple):
            if not link.startswith("https://www.youtube.com/playlist"):
                yt = YouTube(link)
                ys = yt.streams.get_highest_resolution()
                messagebox.showinfo(
                    "", "Appuyer sur ok pour d\u00e9mmarer le t\u00e9l\u00e9chargement"
                )
                try:
                    os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
                except FileExistsError:
                    pass
                finally:

                    ys.download(r"/home/elie/Desktop/YoutubeVideos")
            else:
                yt = Playlist(link)
                messagebox.showinfo(
                    "Appuyer sur ok pour d\u00e9mmarer le t\u00e9l\u00e9chargement de la playlist"
                )
                if not os.path.exists(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                ):
                    os.makedirs(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                    )
                for ys in yt.videos:

                    ys.streams.get_highest_resolution().download(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                    )
        else:
            from youtube_search import YoutubeSearch

            results = YoutubeSearch(link[0]).to_dict()
            assert results, "SOSSUR"
            result = results[0]
            link = "https://youtube.com/" + result["url_suffix"]
            rundownload(link, soundonly)
    else:
        from moviepy.editor import VideoFileClip

        if not isinstance(link, tuple):

            if not link.startswith("https://www.youtube.com/playlist"):
                yt = YouTube(link)
                ys = yt.streams.get_highest_resolution()
                messagebox.showinfo(
                    "", "Appuyer sur ok pour d\u00e9mmarer le t\u00e9l\u00e9chargement"
                )
                try:
                    os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
                except FileExistsError:
                    pass
                finally:

                    ys.download(
                        r"/home/elie/Desktop/YoutubeVideos",
                        unescape(yt.title).replace(" ", "_"),
                    )
                    with VideoFileClip(
                        r"/home/elie/Desktop/YoutubeVideos/%s.mp4"
                        % (unescape(yt.title).replace(" ", "_").replace(".", ""))
                    ) as video:
                        video.audio.write_audiofile(
                            r"/home/elie/Desktop/YoutubeVideos/%s.mp3"
                            % (unescape(yt.title))
                        )
                    os.remove(
                        r"/home/elie/Desktop/YoutubeVideos/%s.mp4"
                        % (unescape(yt.title).replace(" ", "_").replace(".", ""))
                    )
            else:
                ytP = Playlist(link)
                messagebox.showinfo(
                    "",
                    "Appuyer sur ok pour d\u00e9mmarer le t\u00e9l\u00e9chargement de la playlist",
                )
                if not os.path.exists(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title))
                ):
                    os.makedirs(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title))
                    )
                for yt in ytP.videos:

                    yt.streams.get_highest_resolution().download(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title)),
                        unescape(yt.title).replace(" ", "_"),
                    )
                    with VideoFileClip(
                        r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4"
                        % (
                            unescape(ytP.title),
                            unescape(yt.title).replace(" ", "_").replace(".", ""),
                        )
                    ) as video:
                        video.audio.write_audiofile(
                            r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4"
                            % (unescape(ytP.title), unescape(yt.title))
                        )
                    os.remove(
                        r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4"
                        % (unescape(ytP.title), unescape(yt.title))
                    )
        else:
            from youtube_search import YoutubeSearch

            results = YoutubeSearch(link[0]).to_dict()
            assert results, "SOSSUR"
            result = results[0]
            link = "https://youtube.com/" + result["url_suffix"]
            rundownload(link, soundonly)


root = themes.ThemedTk(theme="arc")
root.configure(background="#F6F4F2")
root.title("YoutubeDownloader")
root.resizable(False, False)
st = tkinter.StringVar()
label = tk.Label(root, text="Entrez l'URL")
label.grid(column=0, row=0)
entry = tk.Entry(root, width=50, text=st)
entry.grid(column=0, row=1)
bt = tk.Button(root, command=run, text="Télécharger")
bt.grid(column=0, row=2)
root.mainloop()
