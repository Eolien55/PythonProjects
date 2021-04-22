import sys
from pytube import YouTube, Playlist
import os
from html import unescape
from moviepy.editor import VideoFileClip

user = os.getlogin()


def run(link, soundonly=False):
    if not soundonly:
        if not link.startswith("https://www.youtube.com/playlist"):
            yt = YouTube(link)
            ys = yt.streams.get_highest_resolution()
            try:
                os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
            except FileExistsError:
                pass
            finally:
                ys.download(r"/home/elie/Desktop/YoutubeVideos")
        else:
            yt = Playlist(link)
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
    else:
        if not link.startswith("https://www.youtube.com/playlist"):
            yt = YouTube(link)
            ys = yt.streams.get_highest_resolution()
            try:
                os.makedirs(r"/home/elie/Desktop/YoutubeVideos")
            except FileExistsError:
                pass
            finally:
                ys.download(r"/home/elie/Desktop/YoutubeVideos",
                            unescape(yt.title).replace(' ', '_'))
                video = VideoFileClip(r"/home/elie/Desktop/YoutubeVideos/%s.mp4" %
                                      (unescape(yt.title).replace(' ', '_').replace('.', '')))
                video.audio.write_audiofile(
                    r"/home/elie/Desktop/YoutubeVideos/%s.mp3" % (unescape(yt.title)))
        else:
            ytP = Playlist(link)
            if not os.path.exists(
                r"/home/elie/Desktop/YoutubeVideos/%s" % (unescape(ytP.title))
            ):
                os.makedirs(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (
                        unescape(ytP.title))
                )
            for yt in ytP.videos:
                yt.streams.get_highest_resolution().download(
                    r"/home/elie/Desktop/YoutubeVideos/%s" % (
                        unescape(ytP.title)), unescape(yt.title).replace(' ', '_')
                )
                video = VideoFileClip(r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4" % (
                    unescape(ytP.title), unescape(yt.title).replace(' ', '_').replace('.', '')))
                video.audio.write_audiofile(
                    r"/home/elie/Desktop/YoutubeVideos/%s/%s.mp4" % (unescape(ytP.title), unescape(yt.title)))


params = {i: True for i in sys.argv if i.startswith('-')}
if '-h' in params.keys() or '--help' in params.keys():
    print('Ok, so it downloads youtube videos and you can set --soundonly to have an mp4 without image.')
    exit()
run(sys.argv[1], soundonly=bool(params.get('--soundonly')))
