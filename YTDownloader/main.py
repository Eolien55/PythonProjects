from pytube import YouTube, Playlist
import tkinter
from tkinter import ttk as tk
from tkinter import messagebox
import ttkthemes as themes
import os
from html import unescape
import re

user = os.getlogin()


def run(event=None):
    link = entry.get()
    if "help" in link:
        if link.index("help") == 0:
            messagebox.showinfo(
                "YoutubeDownloader",
                "search:[query]   will replace search:[query] by the url of a video that matches with the query\n\nsoundonly:    download a mp3 instead of a mp4\n\nGlobally, it downloads videos that have the good URL",
            )
            st.set("")
            entry.update()
            return
    if event == "help":
        messagebox.showinfo(
            "YoutubeDownloader",
            "search:[query]   will replace search:[query] by the url of a video that matches with the query\n\nsoundonly:    download a mp3 instead of a mp4\n\nGlobally, it downloads videos that have the good URL",
        )
        st.set("")
        entry.update()
        return
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

    print(link)
    if not soundonly:
        if not isinstance(link, tuple):
            if not link.startswith("https://www.youtube.com/playlist"):
                yt = YouTube(link)
                messagebox.showinfo("", "Le téléchargement va démmarer...")
                ys = yt.streams.get_highest_resolution()
                try:
                    os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
                except FileExistsError:
                    pass
                finally:
                    print(
                        f"OK, let's download '{unescape(yt.title)}', with a resolution of {ys.resolution}"
                    )
                    ys.download(r"/home/elie/Desktop/YoutubeVideos")
            else:
                yt = Playlist(link)
                messagebox.showinfo("", "Le téléchargement va démmarer...")
                if not os.path.exists(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                ):
                    os.makedirs(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
                    )
                for ys in yt.videos:
                    print(
                        f"OK, let's download '{unescape(ys.title)}, with a resolution of {ys.streams.get_highest_resolution().resolution}"
                    )
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
                messagebox.showinfo("", "Le téléchargement va démmarer...")
                ys = yt.streams.get_highest_resolution()
                try:
                    os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
                except FileExistsError:
                    pass
                finally:
                    print(f"OK, let's download '{unescape(yt.title)}'")
                    ys.download(
                        r"/home/elie/Desktop/YoutubeVideos",
                        unescape(yt.title).replace(" ", "_"),
                    )
                    with VideoFileClip(
                        r"/home/elie/Desktop/YoutubeVideos/%s.mp4"
                        % (
                            unescape(yt.title)
                            .replace(" ", "_")
                            .replace(".", "")
                            .replace("'", "")
                            .replace('"', "")
                            .replace("/", "")
                            .replace(":", "")
                            .replace("|", "")
                        )
                    ) as video:
                        video.audio.write_audiofile(
                            r"/home/elie/Desktop/YoutubeVideos/%s.mp3"
                            % (unescape(yt.title))
                        )
                    os.remove(
                        r"/home/elie/Desktop/YoutubeVideos/%s.mp4"
                        % (
                            unescape(yt.title)
                            .replace(" ", "_")
                            .replace(".", "")
                            .replace("'", "")
                            .replace('"', "")
                            .replace("/", "")
                            .replace(":", "")
                            .replace("|", "")
                        )
                    )
            else:
                ytP = Playlist(link)
                messagebox.showinfo("", "Le téléchargement va démmarer...")
                if not os.path.exists(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title))
                ):
                    os.makedirs(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title))
                    )
                for yt in ytP.videos:
                    print(f"OK, let's download '{unescape(yt.title)}'")
                    yt.streams.get_highest_resolution().download(
                        r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title)),
                        unescape(yt.title).replace(" ", "_"),
                    )
                    with VideoFileClip(
                        r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4"
                        % (
                            unescape(ytP.title),
                            unescape(yt.title)
                            .replace(" ", "_")
                            .replace(".", "")
                            .replace("'", "")
                            .replace('"', "")
                            .replace("/", "")
                            .replace(":", "")
                            .replace("|", ""),
                        )
                    ) as video:
                        video.audio.write_audiofile(
                            r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp3"
                            % (unescape(ytP.title), unescape(yt.title))
                        )
                    os.remove(
                        r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4"
                        % (
                            unescape(ytP.title),
                            unescape(yt.title)
                            .replace(" ", "_")
                            .replace(".", "")
                            .replace("'", "")
                            .replace('"', "")
                            .replace("/", "")
                            .replace(":", "")
                            .replace("|", ""),
                        )
                    )
        else:
            from youtube_search import YoutubeSearch

            results = YoutubeSearch(link[0]).to_dict()
            assert results, "SOSSUR"
            result = results[0]
            link = "https://youtube.com/" + result["url_suffix"]
            rundownload(link, soundonly)


root = themes.ThemedTk(theme="arc")
icon = tkinter.PhotoImage(os.path.join(os.path.abspath("."), "YouTube-Emblem.png"))
root.wm_iconphoto(False, icon)
root.configure(background="#F6F4F2")
root.title("YoutubeDownloader")
root.resizable(False, False)
st = tkinter.StringVar()
label = tk.Label(root, text="Enter the URL")
label.grid(column=0, row=0)
entry = tk.Entry(root, width=50, text=st)
entry.bind("<Return>", run)
entry.grid(column=0, row=1)
bt = tk.Button(root, command=lambda: run("help"), text="Help")
bt.grid(column=0, row=2)
root.mainloop()
