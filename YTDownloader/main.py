from pytube import YouTube, Playlist
import tkinter
from tkinter import ttk as tk
from tkinter import messagebox
import ttkthemes as themes
import os
from html import unescape
import re
from werkzeug.utils import secure_filename as file
from moviepy.editor import VideoFileClip

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


def rundownload(link, soundonly=False, suffix="", safe=False):
    if isinstance(link, tuple):
        from youtube_search import YoutubeSearch

        results = YoutubeSearch(link[0]).to_dict()
        assert results, "Aucun résultats"
        result = results[0]
        link = "https://youtube.com/" + result["url_suffix"]
        rundownload(link, soundonly)
        return

    if link.startswith("https://www.youtube.com/playlist"):
        playlist = Playlist(link)
        for url in playlist.video_urls:
            rundownload(url, soundonly, unescape(playlist.title))
        return

    if soundonly:
        name, name_audio = rundownload(link, False, suffix, soundonly)
        with VideoFileClip(
            os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix, name),
        ) as video:
            video.audio.write_audiofile(
                os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix, name_audio)
            )
        os.remove(os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix, name))
        return

    if not os.path.exists(os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix)):
        os.makedirs(os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix))

    video = YouTube(link)

    name = video.title.replace("/", "")
    name_audio = name + ".mp3"

    if safe:
        name = file(name).replace(".", "")

    download_video = video.streams.get_highest_resolution()
    messagebox.showinfo(
        "",
        f"Let's download '{video.title}' with a resolution of '{download_video.resolution}'{' as an mp3' if safe else ''}",
    )
    download_video.download(
        os.path.join(f"/home/{user}/Desktop/YoutubeVideos", suffix), filename=name
    )
    name = name + ".mp4"
    return name, name_audio


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
