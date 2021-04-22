from pytube import YouTube, Playlist
import tkinter
from tkinter import ttk as tk
from tkinter import messagebox
import os
from html import unescape

user = os.getlogin()


def run():
    link = entry.get()
    try:
        if not link.startswith("https://www.youtube.com/playlist"):
            yt = YouTube(link)
            ys = yt.streams.get_highest_resolution()
            messagebox.showinfo(
                "YoutubeDownloader", "Appuyez sur ok pour démarrer le téléchargement"
            )
            try:
                os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
            except FileExistsError:
                pass
            finally:
                ys.download(r"/home/elie/Desktop/YoutubeVideos")
                messagebox.showinfo("YoutubeDownloader",
                                    "Le téléchargement est fini")
        else:
            yt = Playlist(link)
            messagebox.showinfo(
                "YoutubeDownloader",
                "Appuyez sur ok pour démarrer le téléchargement de la playlist",
            )
            if not os.path.exists(
                r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(yt.title))
            ):
                os.makedirs(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (
                        unescape(yt.title))
                )
            for ys in yt.videos:
                ys.streams.get_highest_resolution().download(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (
                        unescape(yt.title))
                )
            messagebox.showinfo("YoutubeDownloader",
                                "Le téléchargement est fini")

    except Exception as e:
        messagebox.showinfo("YoutubeDownloader", e)
    finally:
        st.set("")
        entry.update()


root = tkinter.Tk()
root.title("YoutubeDownloader")
"""root.iconphoto(
    True, tkinter.PhotoImage(file="/home/Elie/Pictures/YouTube-Emblem.png")
)"""
root.resizable(False, False)
st = tkinter.StringVar()
label = tk.Label(root, text="Entrez l'URL")
label.grid(column=0, row=0)
entry = tk.Entry(root, width=50, text=st)
entry.grid(column=0, row=1)
bt = tk.Button(root, command=run, text="Télécharger")
bt.grid(column=0, row=2)
root.mainloop()
